import pygame

from scripts.utils import Animation, load_images

ATTACK_COOLDOWN = 30
DEFEND_COOLDOWN = 30

MAX_VELOCITY = 3
MAX_GRAVITY = 9


class Character1:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = list(size)
        self.collisions = [False, False, False, False]  # left,top,right,bottom

        self.assets = {
            'idle': Animation(load_images('entities/character1/idle', True), img_dur=5),
            'run': Animation(load_images('entities/character1/run', True), img_dur=7),
            'jump': Animation(load_images('entities/character1/j_down', True), img_dur=10, loop=True),
            'attack': Animation(load_images('entities/character1/3_atk', True), img_dur=10, loop=True),
            'defend': Animation(load_images('entities/character1/defend', True), img_dur=10, loop=False),
        }
        self.current_animation = 'idle'
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())

        self.going_right = False
        self.going_left = False
        self.facing_left = False

        self.acc = [0.2, 1]
        self.velocity = [0, 0]

        self.air_time = 0
        self.can_jump = False
        self.is_jumping = None

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
        return pygame.Rect(self.pos[0], self.pos[1], self.assets[self.current_animation].img().get_width(), self.assets[self.current_animation].img().get_height())

    def __apply_gravity__(self):
        if self.velocity[1] < MAX_GRAVITY:
            self.velocity[1] += self.acc[1]
        self.pos[1] += self.velocity[1]

    def move_right(self):
        self.going_right = not self.going_right

    def move_left(self):
        self.going_left = not self.going_left

    def __move__(self):
        if self.going_right and abs(self.velocity[0]) < MAX_VELOCITY:
            self.velocity[0] += self.acc[0]
            self.facing_left = False
            if not self.is_jumping:
                self.current_animation = 'run'
        if self.going_left and abs(self.velocity[0]) < MAX_VELOCITY:
            self.velocity[0] += -self.acc[0]
            self.facing_left = True
            if not self.is_jumping:
                self.current_animation = 'run'

        self.pos[0] += self.velocity[0]

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        if self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        if not self.going_left and not self.going_right and self.velocity[0] == 0 and self.velocity[1] == 0:
            self.current_animation = 'idle'
        if not self.going_left and not self.going_right and self.velocity[0] != 0:
            self.current_animation = 'run'

    def jump(self):
        if self.can_jump:
            self.is_jumping = True
            self.can_jump = False
            self.current_animation = 'jump'
            self.velocity[1] = -3
            self.acc[1] = 0.1
            self.air_time = 5

    def check_collision(self, other_mask, other_rect):
        left, top, right, bottom = False, False, False, False
        offset = (int(other_rect.x - self.rect().x), int(other_rect.y - self.rect().y))
        overlap = self.mask.overlap(other_mask, offset)
        if overlap:
            collision_x = overlap[0] - offset[0]
            collision_y = overlap[1] - offset[1]
            if offset[1] > 0:
                top = True
            elif offset[1] < 0:
                bottom = True
            elif offset[0] > 0:
                left = True
            else:
                right = True
            # print(collision_x, collision_y)
            # print(other_rect, self.rect())
        return [left, top, right, bottom], overlap

    def __check_collisions__(self):
        # self.collisions = [False, False, False, False]
        self.__check_collisions_with_tiles__()

    def __check_collisions_with_tiles__(self):
        collisions = [False, False, False, False]
        # player_rect = self.rect()
        # for rect in self.game.map.rects:
        #     if player_rect.colliderect(rect):
        #         if self.velocity[1] > 0:
        #             # self.acc[1] = 0
        #             # self.velocity[1] = 0
        #             # self.can_jump = True
        #             # self.is_jumping = False
        #             player_rect.bottom = rect.top
        #         self.pos[1] = rect.y
        # print(self.rect().collidelist(self.game.map.rects))

        # for y in range(len(self.game.map.grid)):
        #     for x in range(len(self.game.map.grid[y])):
        #         if self.game.map.rects[y][x] != None:
        #             mask = self.game.map.masks[y][x]
        #             rect = self.game.map.rects[y][x]
        #             new_collisions, overlap = self.check_collision(other_mask=mask, other_rect=rect)
        #             collisions = [collisions[i] + new_collisions[i] for i in range(len(collisions))]
        #             # print(collisions)
        #             if collisions[1]:
        #                 self.acc[1] = 0
        #                 self.velocity[1] = 0
        #                 self.can_jump = True
        #                 self.is_jumping = False
        #                 self.rect().bottom = rect.top
        #                 self.pos[1] = self.rect().y

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
        # self.set_action('ultimate')
        pass

    def update(self):
        self.__apply_gravity__()
        self.__move__()
        self.__check_collisions__()

    def render(self, surf, offset=(0, 0)):
        self.assets[self.current_animation].update()
        self.mask = pygame.mask.from_surface(self.assets[self.current_animation].img())
        surf.blit(pygame.transform.flip(self.assets[self.current_animation].img(), self.facing_left, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))
