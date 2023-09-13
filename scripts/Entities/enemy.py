import math
import random

import pygame.transform

from scripts.VFX.Particles.particle import Particle
from scripts.VFX.projectile import Projectile
from scripts.VFX.spark import Spark

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        self.walking = 0

    def update(self, tilemap, movement=(0,0)):
        if self.walking:
            # if there's a tile on the ground where the enemy is heading, it can continue moving.
            # else, it should move in the other direction.
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                # if the enemy met a wall, it should move in the other direction
                if self.collisions['left'] or self.collisions['right']:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if abs(dis[1]) < 16:
                    if self.flip and dis[0] < 0:
                        self.game.projectiles.append(Projectile([self.rect().centerx - 7 , self.rect().centery ], -2.5, 0))
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1].pos, random.random() - 0.5 + math.pi, 2 + random.random()))
                    if not self.flip and dis[0] > 0:
                        self.game.projectiles.append(Projectile([self.rect().centerx + 7, self.rect().centery], 2.5, 0))
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1].pos, random.random() - 0.5 , 2 + random.random()))
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        if abs(self.game.player.dashing) > 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake.update(16, self.game.screenshake.shake_value)
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, [
                        math.cos(angle + math.pi) * speed * 0.5,
                        math.sin(angle + math.pi) * speed * 0.5
                    ], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True


    def render(self, surf, offset=(0,0)):
        super().render(surf, offset)
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))