import math
import random

import pygame

from scripts.Entities.entity import Entity
from scripts.VFX.Particles.particle import Particle
from scripts.VFX.spark import Spark
from scripts.utils import load_images, Animation


class Player(Entity):

    def __init__(self, game, pos):
        self.game= game
        self.pos = list(pos)
        self.assets = {
            'idle': Animation(load_images('entities/character1/idle', True), img_dur=5),
            'run': Animation(load_images('entities/character1/run', True), img_dur=7),
            'jump': Animation(load_images('entities/character1/j_down', True), img_dur=10, loop=True),
            'attack_1': Animation(load_images('entities/character1/1_atk', True), img_dur=3, loop=True),
            'attack_2': Animation(load_images('entities/character1/2_atk', True), img_dur=5, loop=True),
            'attack_3': Animation(load_images('entities/character1/3_atk', True), img_dur=5, loop=True),
            'attack_air' : Animation(load_images('entities/character1/air_atk', True), img_dur=5, loop=True),
            'defend': Animation(load_images('entities/character1/defend', True), img_dur=10, loop=False),
        }
        self.current_animation = 'idle'
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())
        self.size = (self.assets[self.current_animation].img().get_width(), self.assets[self.current_animation].img().get_height())
        super().__init__(self.game, self.pos, self.size, self.assets, self.current_animation)

        self.is_fighting = False

        self.is_attacking = False
        self.attacks = [1,2,3]
        self.attack_index = 0
        self.current_attack = self.attacks[self.attack_index]
        self.attack_cooldown_counter = 0
        self.ATTACK_COOLDOWN_TIMER = self.assets["attack_"+str(self.current_attack)].duration()

        self.dead = False
        self.dead_counter = 0

    def passive(self):
        pass

    def attack(self):
        if not self.is_jumping and self.attack_cooldown_counter == 0:
            self.ATTACK_COOLDOWN_TIMER = self.assets["attack_" + str(self.current_attack)].duration()
        if  self.is_jumping and self.attack_cooldown_counter == 0:
            self.ATTACK_COOLDOWN_TIMER = self.assets["attack_air"].duration()
        self.attack_cooldown_counter = -self.ATTACK_COOLDOWN_TIMER
        self.is_attacking = True
        self.is_fighting = True

    def update_attack(self):
        if self.attack_cooldown_counter <= 0:
            self.attack_cooldown_counter = min(0, self.attack_cooldown_counter + 1)
            self.handle_attack_collisions()
            if self.attack_cooldown_counter == 0:
                self.is_attacking = False
                self.is_fighting = False
                self.assets["attack_air"].reset()
                self.assets["attack_"+str(self.current_attack)].reset()

    def handle_attack_collisions(self):
        for enemy in self.game.enemies:
            collision_pos = self.check_collision(enemy, enemy.mask)
            if (collision_pos[0] or collision_pos[1]) and self.is_attacking:
                self.game.screenshake.update(0, 7)
                # enemy.take_hit(self.facing_left)
                for i in range(10):
                    collision_pos[0] = self.pos[0] + collision_pos[0]
                    collision_pos[1] = self.pos[1] + collision_pos[1]
                    angle = math.pi * (random.uniform(0.75, 1.25) if self.facing_left else random.uniform(1.75, 2.25))
                    speed = random.random() + 10
                    self.game.sparks.append(Spark(collision_pos, angle, speed, (204,102,0)))
    def defend(self):
        pass

    def ultimate(self):
        pass

    def take_hit(self, from_left):
        pass
        # super().take_hit(from_left)

    def handle_animations(self):
        if self.move[0] != 0:
            if self.move[0] < 0:
                self.facing_left = True
            else:
                self.facing_left = False
            self.current_animation = "run"
        else:
            self.current_animation = "idle"

        if self.is_jumping or abs(self.velocity[1]) > 1:
            self.current_animation = "jump"

        if self.is_fighting and self.is_attacking:
            if not self.is_jumping:
                self.current_animation = "attack_" + str(self.current_attack)
            else:
                self.current_animation = "attack_air"

    def update(self):
        #handle_animations get called here!
        self.update_attack()
        super().update()

    def render(self, surf, offset=(0, 0)):
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())
        super().render(surf, offset)

        # surf.blit(pygame.transform.flip(self.mask.to_surface(), self.facing_left, False),
        #           (self.pos[0] - offset[0] ,
        #            self.pos[1] - offset[1]))



