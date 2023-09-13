import random
import pygame

from scripts.VFX.Particles.particle import Particle

class LeafParticles:
    def __init__(self, game):
        self.game = game
        self.leaf_spawners = []
        for tree in self.game.map.extract('large_decor', 2, True):
            y,x = self.game.map.decode_tile_coordinates(tree)
            self.leaf_spawners.append(pygame.Rect(4 + x, 4 + y, 23, 13))

    def render(self):
        for rect in self.leaf_spawners:
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                self.game.particles.append(
                    Particle(self.game, p_type='leaf', pos=pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20))
        )
