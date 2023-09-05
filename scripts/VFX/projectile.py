import math
import random

from scripts.VFX.Particles.particle import Particle
from scripts.VFX.spark import Spark
from scripts.utils import load_image


class Projectile:
    def __init__(self, pos, direction, timer):
        self.pos = list(pos)
        self.direction = direction
        self.timer = timer
        self.assets = {
            'projectile': load_image('projectile.png')
        }

    def check_if_hit_wall(self, game):
        if game.map.solid_check(self.pos):
            game.projectiles.remove(self)
            for i in range(4):
                game.sparks.append(Spark(self.pos, random.random() - 0.5 + (math.pi if self.direction > 0 else 0),
                                         2 + random.random()))
    def check_if_fat(self, game):
        if self.timer > 360:
            game.projectiles.remove(self)

    def check_collision_with_player(self, game):
        if abs(game.player.dashing) < 50:
            if game.player.rect().collidepoint(self.pos):
                game.projectiles.remove(self)
                game.dead += 1
                game.screenshake.update(60, game.screenshake.shake_value)
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    game.sparks.append(Spark(game.player.rect().center, angle, 2 + random.random()))
                    game.particles.append(Particle(game, 'particle', game.player.rect().center, [
                        math.cos(angle + math.pi) * speed * 0.5,
                        math.sin(angle + math.pi) * speed * 0.5
                    ], frame=random.randint(0, 7)))

    def update(self):
        self.pos[0] += self.direction
        self.timer += 1

    def render(self, surf, offset=(0,0)):
        img = self.assets['projectile']
        surf.blit(img, (self.pos[0] - img.get_width() / 2 - offset[0],
                                self.pos[1] - img.get_height() / 2 - offset[1]))