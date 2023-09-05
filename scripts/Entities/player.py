import math
import random

from scripts.Entities.entities import PhysicsEntity
from scripts.VFX.Particles.particle import Particle

class Player(PhysicsEntity):
    def __init__(self, game, pos, size, type='player', can_wall_slide=True, can_dash=True):
        super().__init__(game, type, pos, size)
        self.air_time = 0
        self.jumps = 1
        self.can_wall_slide = can_wall_slide
        self.wall_slide = False
        self.can_dash = can_dash
        self.dashing = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        self.update_wall_slide()

        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        self.update_dash()


    def render(self, surf, offset=(0, 0)):
        if not self.can_dash or abs(self.dashing) <= 50:
            super().render(surf, offset=offset)

    def jump(self):
        if self.can_wall_slide:
            if self.wall_slide:
                if self.flip and self.last_movement[0] < 0:
                    self.velocity[0] = 3.5
                    self.velocity[1] = -2.5
                    self.air_time = 5
                    self.jumps = max(0, self.jumps - 1)
                    return
                elif not self.flip and self.last_movement[0] > 0:
                    self.velocity[0] = -3.5
                    self.velocity[1] = -2.5
                    self.air_time = 5
                    self.jumps = max(0, self.jumps - 1)
                    return
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    def dash(self):
        if self.can_dash:
            if not self.dashing:
                if self.flip:
                    self.dashing = -60
                else:
                    self.dashing = 60

    def update_dash(self):
        if self.can_dash:
            if abs(self.dashing) in {60, 50}:
                for i in range(20):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 0.5 + 0.5
                    pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                    self.game.particles.append(
                        Particle(self.game, 'particle', self.rect().center, pvelocity, frame=random.randint(0, 7)))
            if self.dashing > 0:
                self.dashing = max(0, self.dashing - 1)
            if self.dashing < 0:
                self.dashing = min(0, self.dashing + 1)
            if abs(self.dashing) > 50:
                self.velocity[0] = abs(self.dashing) / self.dashing * 8
                if abs(self.dashing) == 51:
                    self.velocity[0] *= 0.1
                pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
                self.game.particles.append(
                    Particle(self.game, 'particle', self.rect().center, pvelocity, frame=random.randint(0, 7)))

    def update_wall_slide(self):
        if self.can_wall_slide:
            self.wall_slide = False
            if (self.collisions['left'] or self.collisions['right']) and self.air_time > 4:
                self.wall_slide = True
                self.velocity[1] = min(self.velocity[1], 0.5)
                if self.collisions['right']:
                    self.flip = False
                else:
                    self.flip = True
                self.set_action('wall_slide')

