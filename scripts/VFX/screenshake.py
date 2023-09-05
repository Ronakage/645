import random

import pygame


class Screenshake:
    def __init__(self, game):
        self.game = game
        self.shake_value = 0

    def update(self, minimum, maximum):
        self.shake_value = max(minimum, maximum)

    def render(self):
        screenshake_offset = (random.random() * self.shake_value - self.shake_value / 2,
                              random.random() * self.shake_value - self.shake_value / 2)
        self.game.screen.blit(pygame.transform.scale(self.game.display, self.game.screen.get_size()), screenshake_offset)
