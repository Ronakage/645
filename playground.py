import math
import sys

import pygame

from scripts.Entities.player import Player
from scripts.VFX.Particles.leaf_particle import LeafParticles
from scripts.VFX.display import Display
from scripts.VFX.screenshake import Screenshake
from scripts.VFX.transition import Transition
from scripts.Environment.clouds import Clouds
from scripts.Environment.map import Map
from scripts.utils import Animation, load_images, load_image


DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 360


class Playground:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('645')

        self.DISPLAY_WIDTH = 640
        self.DISPLAY_HEIGHT = 360

        self.screen = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.displays = Display(self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT)
        self.display, self.outline_display = self.displays.get_displays()
        self.clock = pygame.time.Clock()

        self.assets = {
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.clouds = Clouds(self.assets['clouds'], count=32)

        self.map = Map()
        self.player = Player(self, (50, -100))
        self.load_level()


        self.screenshake = Screenshake(self)

    def load_level(self):
        try:
            self.map.load('data/maps/future1.json')
        except:
            pass

        self.leaf_particles = LeafParticles(self)

        self.enemies = []
        for coordinate in self.map.extract('spawners', 0):
                y,x = self.map.decode_tile_coordinates(coordinate)
                self.player.pos = [x,y]
        for spawner  in self.map.extract('spawners', 1):
                # self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
                print("Enemy spawned!")

        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]

        self.dead = 0
        self.transation = Transition(self)

    def endgame(self):
        self.load_level()

    def run(self):
        while 1:
            self.displays.refresh_background(self.assets['background'])

            self.screenshake.update(0, self.screenshake.shake_value - 1)

            if self.dead:
                self.transation.transation_duration += 1
                if self.transation.transation_duration > 30:
                    self.endgame()
            if self.transation.transation_duration < 0:
                self.transation.transation_duration += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transation.update()
                if self.dead > 40:
                    self.load_level()

            self.scroll[0] += (self.player.rect().centerx - self.outline_display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.outline_display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.leaf_particles.render()

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.map.render(self.outline_display, offset=render_scroll)

            # Enemy Loop
            # for enemy in self.enemies.copy():
            #     kill = enemy.update(self.map)
            #     enemy.render(self.display, offset=render_scroll)
            #     if kill:
            #         self.enemies.remove(enemy)

            # Player Loop
            if not self.dead:
                self.player.update()
                self.player.render(self.outline_display, offset=render_scroll)

            # Projectile Loop
            for projectile in self.projectiles.copy():
                projectile.update()
                projectile.render(self.outline_display, offset=render_scroll)
                projectile.check_if_hit_wall(self)
                projectile.check_collision_with_player(self)

            # Spark Loop
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.outline_display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            self.displays.update()

            # Particle Loop
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.outline_display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation_frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            # Input Handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.going_left = True
                    if event.key == pygame.K_d:
                        self.player.going_right = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_h:
                        self.player.attack()
                    # if event.key == pygame.K_j:
                    #     self.player.defend()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.going_left = False
                    if event.key == pygame.K_d:
                        self.player.going_right = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.transation.render()
            self.displays.render()
            self.screenshake.render()

            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            fps_text = font.render(str(int(self.clock.get_fps())), False, (0, 0, 0))
            self.screen.blit(fps_text, (1, 1))

            pygame.display.update()
            self.clock.tick(60)

Playground().run()

