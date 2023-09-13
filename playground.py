import math
import sys

import pygame

from scripts.Entities.enemy import Enemy
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

        self.background = load_image('background.png')

        self.clouds = Clouds(count=32)

        self.map = Map()
        self.player = Player(self, (50, -100))
        self.load_level()

        self.screenshake = Screenshake(self)

    def load_level(self):
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]
        self.leaf_particles = LeafParticles(self)
        self.transation = Transition(self)

        try:
            self.map.load('data/maps/future1.json')
        except:
            pass

        for coordinate in self.map.extract('spawners', 0):
                y,x = self.map.decode_tile_coordinates(coordinate)
                self.player.pos = [x,y]
        for coordinate in self.map.extract('spawners', 1):
                y, x = self.map.decode_tile_coordinates(coordinate)
                self.enemies.append(Enemy(self, (x,y)))


    def restart(self):
        self.player.dead = False
        self.player.dead_counter = 0
        self.load_level()

    def end(self):
        if self.player.dead:
            self.transation.transation_duration += 1
            if self.transation.transation_duration > 30:
                self.restart()
        if self.transation.transation_duration < 0:
            self.transation.transation_duration += 1

        if self.player.dead:
            self.player.dead_counter += 1
            if self.player.dead_counter >= 10:
                self.transation.update()
            if self.player.dead_counter > 40:
                self.load_level()

    def fps(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        fps_text = font.render(str(int(self.clock.get_fps())), False, (0, 0, 0))
        self.screen.blit(fps_text, (1, 1))

    def run(self):
        while 1:
            self.displays.refresh_background(self.background)

            self.screenshake.update(0, self.screenshake.shake_value - 1)

            self.end()

            self.scroll[0] += (self.player.rect().centerx - self.outline_display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.outline_display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.leaf_particles.render()

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.map.render(self.outline_display, offset=render_scroll)

            #Enemy Loop
            for enemy in self.enemies.copy():
                enemy.update()
                enemy.render(self.outline_display, offset=render_scroll)
                if enemy.dead:
                    self.enemies.remove(enemy)

            # Player Loop
            if not self.player.dead:
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

            self.fps()

            pygame.display.update()
            self.clock.tick(60)

Playground().run()

