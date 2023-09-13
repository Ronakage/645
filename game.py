import os
import math
import sys
import pygame

from scripts.Entities.player import Player
from scripts.VFX.Particles.leaf_particle import LeafParticles
from scripts.VFX.screenshake import Screenshake
from scripts.VFX.transition import Transition
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.Entities.enemy import Enemy
from scripts.Environment.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('645')

        self.screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.display = pygame.Surface((320, 180))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle' : Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))
        # self.player = Character1(self, (0,0), self.assets['character1/idle'].img().get_size())

        self.map = TileMap(self)
        self.level = 0
        self.load_level(self.level)

        self.screenshake = Screenshake(self)

    def load_level(self, map_id):
        self.map.load('data/maps/' + str(map_id) + '.json')

        self.leaf_particles = LeafParticles(self)

        self.enemies = []
        for spawner in self.map.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]

        self.dead = 0
        self.transation = Transition(self)

    def endgame(self):
        self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
        self.load_level(self.level)

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))


            self.screenshake.update(0, self.screenshake.shake_value - 1)
            self.transation.check_level_end()

            if self.dead :
                self.dead += 1
                if self.dead >= 10:
                    self.transation.update()
                if self.dead > 40:
                    self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.leaf_particles.render()

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.map.render(self.display, offset=render_scroll)

            #Enemy Loop
            for enemy in self.enemies.copy():
                kill = enemy.update(self.map)
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            #Player Loop
            if not self.dead:
                self.player.update(self.map, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            #Projectile Loop
            for projectile in self.projectiles.copy():
                projectile.update()
                projectile.render(self.display, offset=render_scroll)
                projectile.check_if_hit_wall(self)
                projectile.check_collision_with_player(self)

            #Spark Loop
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            #Particle Loop
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation_frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            #Input Handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_SPACE:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.transation.render()
            self.screenshake.render()

            font = pygame.font.Font(pygame.font.get_default_font(), 32)
            fps_text = font.render(str(int(self.clock.get_fps())), True, (0, 0, 0))
            self.screen.blit(fps_text, (1, 1))

            pygame.display.update()
            self.clock.tick(63)


Game().run()
