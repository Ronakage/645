import pygame

from scripts.utils import load_image, Animation, load_images

ATTACK_COOLDOWN = 30
DEFEND_COOLDOWN = 30

MAX_VELOCITY = 3


class Character1:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = list(size)

        self.assets = {
            'idle': Animation(load_images('entities/character1/idle', True), img_dur=6),
            'run': Animation(load_images('entities/character1/run', True), img_dur=10),
            'jump': Animation(load_images('entities/character1/j_down', True), img_dur=10,loop=True),
            'attack': Animation(load_images('entities/character1/3_atk', True), img_dur=10, loop=True),
            'defend': Animation(load_images('entities/character1/defend', True), img_dur=10, loop=False),
        }
        self.current_animation = 'idle'
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())

        self.going_right = False
        self.going_left = False
        self.facing_left = False
        self.acc = [0.2, 0]
        self.velocity = [0, 0]
        self.air_time = 0
        self.can_jump = False

        self.is_collidable = True

        self.attack_cooldown = 0
        self.is_attacking = False
        self.defend_cooldown = 0
        self.is_defending = False
        self.ult_cooldown = 0
        self.is_ulting = False
        self.ult_duration = 1 * 60
        self.is_fighting = False

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def move_right(self):
        self.going_right = not self.going_right

    def move_left(self):
        self.going_left = not self.going_left

    def __move__(self):
        if self.going_right and abs(self.velocity[0]) < MAX_VELOCITY:
            self.velocity[0] += self.acc[0]
            self.facing_left = False
            self.current_animation = 'run'
        if self.going_left and abs(self.velocity[0]) < MAX_VELOCITY:
            self.velocity[0] += -self.acc[0]
            self.facing_left = True
            self.current_animation = 'run'

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        if self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        if not self.going_left and not self.going_right:
            self.current_animation = 'idle'

    def jump(self):
        if self.can_jump:
            self.can_jump = False
            self.current_animation = 'jump'
            self.velocity[1] = -3
            self.air_time = 5

    def check_collision(self, other_mask, other_rect):
        """
           In the mask_collision function, the offset parameter represents the relative position of rect2 (the second object) with respect to rect1 (the first object). It's a tuple (x_offset, y_offset) that describes how much rect2 is shifted horizontally and vertically relative to rect1. This offset is used when checking for collisions between the two masks.

           Here's how the offset is calculated:

           offset[0]: The horizontal (X-axis) difference between the left edge of rect2 and the left edge of rect1. If rect2 is to the left of rect1, this value will be negative. If rect2 is to the right, it will be positive.

           offset[1]: The vertical (Y-axis) difference between the top edge of rect2 and the top edge of rect1. If rect2 is above rect1, this value will be negative. If rect2 is below, it will be positive.

           The offset is used to calculate the position of the overlap (if any) between the two masks, allowing you to determine where the collision occurs relative to rect1.
           """
        offset = (int(other_rect.x - self.rect().x), int(other_rect.y - self.rect().y))
        overlap = self.mask.overlap(other_mask, offset)
        if overlap:
            collision_x = overlap[0] - offset[0]
            collision_y = overlap[1] - offset[1]
            if offset[1] > 0:
                print('top collision')
            elif offset[1] < 0:
                print('bottom collision')
            elif offset[0] > 0:
                print('left collision')
            else:
                print('right collision')
            print(collision_x, collision_y)
            print(other_rect, self.rect())
        return bool(overlap)

    def __check_collisions__(self):
        pass
        # for key,(mask,rect) in self.game.map.masks_and_rects.items():
        #     # print((mask, rect))
        #     self.check_collision(other_mask=mask, other_rect=rect)


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

    def update(self):
        self.__move__()
        self.__check_collisions__()

    def render(self, surf, offset=(0, 0)):
        self.assets[self.current_animation].update()
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())
        surf.blit(pygame.transform.flip(self.assets[self.current_animation].img(), self.facing_left, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        # surf.blit(pygame.transform.flip(self.mask.to_surface(unsetcolor=(0,0,0,0)), self.facing_left, False),
        #           (self.pos[0] - offset[0], self.pos[1] - offset[1]))
