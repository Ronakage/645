from abc import abstractmethod

import pygame


class Entity:
    def __init__(self, game, pos, size=(0, 0), assets=None, current_animation="idle", is_collidable=True):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.assets = assets
        self.current_animation = current_animation
        self.is_collidable = is_collidable

        self.collisions = [False, False, False, False]  # left,top,right,bottom

        self.going_right = False
        self.going_left = False
        self.facing_left = False

        self.move = [0, 0]
        self.velocity = [0, 0]

        self.air_time = 0
        self.can_jump = False
        self.is_jumping = True

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

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
        return [left, top, right, bottom], overlap

    def jump(self):
        if not self.is_jumping and self.can_jump:
            self.is_jumping = True
            self.can_jump = False
            self.velocity[1] = -3

    @abstractmethod
    def update(self):
        self.collisions = [False, False, False, False]
        self.move = (self.going_right - self.going_left, 0)
        frame_movement = (self.move[0] * 3 + self.velocity[0], self.move[1] + self.velocity[1])

        self.handle_animations()

        if self.is_collidable:
            self.pos[0] += frame_movement[0]
            entity_rect = self.rect()
            for rect in self.game.map.rects:
                if entity_rect.colliderect(rect):
                    if frame_movement[0] > 0:
                        self.collisions[2] = True
                        entity_rect.right = rect.left
                    if frame_movement[0] < 0:
                        self.collisions[0] = True
                        entity_rect.left = rect.right
                    self.pos[0] = entity_rect.x

            self.pos[1] += frame_movement[1]
            entity_rect = self.rect()
            for rect in self.game.map.rects:
                if entity_rect.colliderect(rect):
                    if frame_movement[1] > 0:
                        self.collisions[3] = True
                        entity_rect.bottom = rect.top
                        self.can_jump = True
                        self.is_jumping = False
                    if frame_movement[1] < 0:
                        self.collisions[1] = True
                        entity_rect.top = rect.bottom
                    self.pos[1] = entity_rect.y

            self.velocity[1] = min(5, self.velocity[1] + 0.1)

            if self.collisions[1] or self.collisions[3]:
                self.velocity[1] = 0

    @abstractmethod
    def render(self, surf, offset=(0, 0)):
        self.assets[self.current_animation].update()
        surf.blit(pygame.transform.flip(self.assets[self.current_animation].img(), self.facing_left, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    @abstractmethod
    def passive(self):
        pass

    @abstractmethod
    def attack(self):
        pass
        # if self.attack_cooldown == 0:
        #     self.attack_cooldown = -ATTACK_COOLDOWN
        #     self.is_attacking = True
        #     self.is_fighting = True

    # def update_attack(self):
    #     if self.attack_cooldown < 0:
    #         self.attack_cooldown = min(0, self.attack_cooldown + 1)
    #         print(self.rect().size)
    #         if self.attack_cooldown == 0:
    #             self.is_attacking = False
    #             self.is_fighting = False

    @abstractmethod
    def defend(self):
        pass
        # if self.defend_cooldown == 0:
        #     self.defend_cooldown = -DEFEND_COOLDOWN
        #     self.is_defending = True
        #     self.is_fighting = True

    # def update_defend(self):
    #     if self.defend_cooldown < 0:
    #         self.defend_cooldown = min(0, self.defend_cooldown + 1)
    #         if self.defend_cooldown == 0:
    #             self.is_defending = False
    #             self.is_fighting = False

    @abstractmethod
    def ultimate(self):
        pass

    @abstractmethod
    def handle_animations(self):
        pass
