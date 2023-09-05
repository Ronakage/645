import math
import random
import sys

import pygame

from scripts.Entities.Characters.character1 import Character1
from scripts.Entities.enemy import Enemy
from scripts.VFX.Particles.leaf_particle import LeafParticles
from scripts.VFX.screenshake import Screenshake
from scripts.VFX.transition import Transition
from scripts.clouds import Clouds
from scripts.tilemap import TileMap
from scripts.utils import Animation, load_images, load_image


class Playground:
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
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            'character1/idle': Animation(load_images('entities/character1/idle', True, scale=(24, 34)), img_dur=6),
            'character1/run': Animation(load_images('entities/character1/run', True, scale=(24, 34)), img_dur=10),
            'character1/jump': Animation(load_images('entities/character1/jump', True, scale=(24, 34)), img_dur=10,loop=True),
            'character1/attack': Animation(load_images('entities/character1/3_atk', True), img_dur=10, loop=True),
            'character1/defend': Animation(load_images('entities/character1/defend', True), img_dur=10, loop=False),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Character1(self, (0,0), self.assets['character1/idle'].img().get_size())

        self.map = TileMap(self)
        self.load_level()

        self.screenshake = Screenshake(self)

    def load_level(self):
        self.map.load('data/maps/current.json')

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
        self.load_level()

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

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

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.leaf_particles.AppendAndSpawnLeafs()

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.map.render(self.display, offset=render_scroll)

            # Enemy Loop
            for enemy in self.enemies.copy():
                kill = enemy.update(self.map)
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            # Player Loop
            if not self.dead:
                self.player.update(self.map, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            # Projectile Loop
            for projectile in self.projectiles.copy():
                projectile.update()
                projectile.render(self.display, offset=render_scroll)
                projectile.check_if_hit_wall(self)
                projectile.check_collision_with_player(self)

            # Spark Loop
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            # Particle Loop
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation_frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            # Input Handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_h:
                        self.player.attack()
                    if event.key == pygame.K_j:
                        self.player.defend()
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
            self.clock.tick(60)

Playground().run()

