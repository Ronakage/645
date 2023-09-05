import pygame

from scripts.Entities.entities import PhysicsEntity
from scripts.Entities.player import Player

ATTACK_COOLDOWN = 30
DEFEND_COOLDOWN = 30


class Character1(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game=game, pos=pos, size=size, e_type='character1')
        self.air_time = 0
        self.jumps = 1
        self.attack_cooldown = 0
        self.is_attacking = False
        self.defend_cooldown = 0
        self.is_defending = False
        self.ult_cooldown = 0
        self.is_ulting = False
        self.ult_duration = 1 * 60
        self.is_fighting = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        self.update_attack()
        self.update_defend()

        if not self.is_fighting:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        else:
            if self.is_attacking:
                self.set_action('attack')
            if self.is_defending:
                self.set_action('defend')

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    def passive(self):
        pass

    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = -ATTACK_COOLDOWN
            self.is_attacking = True
            self.is_fighting = True

    def update_attack(self):
        if self.attack_cooldown < 0:
            self.attack_cooldown = min(0, self.attack_cooldown + 1)
            print(self.rect().size)
            if self.attack_cooldown == 0:
                self.is_attacking = False
                self.is_fighting = False

    def defend(self):
        if self.defend_cooldown == 0:
            self.defend_cooldown = -DEFEND_COOLDOWN
            self.is_defending = True
            self.is_fighting = True

    def update_defend(self):
        if self.defend_cooldown < 0:
            self.defend_cooldown = min(0, self.defend_cooldown + 1)
            if self.defend_cooldown == 0:
                self.is_defending = False
                self.is_fighting = False

    def ultimate(self):
        self.set_action('ultimate')
        pass
