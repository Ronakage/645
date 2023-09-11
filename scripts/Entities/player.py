import pygame

from scripts.Entities.entity import Entity
from scripts.utils import load_images, Animation


class Player(Entity):
    def __init__(self, game, pos):
        self.game= game
        self.pos = pos
        self.assets = {
            'idle': Animation(load_images('entities/character1/idle', True), img_dur=5),
            'run': Animation(load_images('entities/character1/run', True), img_dur=7),
            'jump': Animation(load_images('entities/character1/j_down', True), img_dur=10, loop=True),
            'attack': Animation(load_images('entities/character1/3_atk', True), img_dur=10, loop=True),
            'defend': Animation(load_images('entities/character1/defend', True), img_dur=10, loop=False),
        }
        self.current_animation = 'idle'
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())
        self.size = (self.assets[self.current_animation].img().get_width(), self.assets[self.current_animation].img().get_height())
        super().__init__(self.game, self.pos, self.size, self.assets, self.current_animation)

    def passive(self):
        pass

    def attack(self):
        pass

    def defend(self):
        pass

    def ultimate(self):
        pass

    def handle_animations(self):
        if self.move[0] != 0:
            if self.move[0] < 0:
                self.facing_left = True
            else:
                self.facing_left = False
            self.current_animation = "run"
        else:
            self.current_animation = "idle"

        if self.is_collidable:
            if self.is_jumping or abs(self.velocity[1]) > 1:
                self.current_animation = "jump"

    def update(self):
        super().update()

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)

