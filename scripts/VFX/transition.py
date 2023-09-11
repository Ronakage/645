import os

import pygame


class Transition:
    def __init__(self, game):
        self.game = game
        self.transation_duration = -30

    def check_level_end(self):
        if not len(self.game.enemies):
            self.transation_duration += 1
            if self.transation_duration > 30:
                self.game.endgame()
        if self.transation_duration < 0:
            self.transation_duration += 1

    def update(self):
        self.transation_duration = min(self.transation_duration + 1, 30)

    def render(self):
        if self.transation_duration:
            transition_surf = pygame.Surface(self.game.outline_display.get_size())
            pygame.draw.circle(transition_surf, (255, 255, 255),
                               (self.game.outline_display.get_width() / 2, self.game.outline_display.get_height() / 2),
                               (30 - abs(self.transation_duration)) * 8)
            transition_surf.set_colorkey((255, 255, 255))
            self.game.outline_display.blit(transition_surf, (0, 0))