import pygame

from scripts.utils import load_image, load_images, Animation


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.air_time = 0
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up':False, 'down':False, 'right':False, 'left':False}

        self.action = ''
        self.animation = None
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

        self.last_movement = [0,0]

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.animation.img().get_width(), self.animation.img().get_height() - 5)

    def update(self, tilemap, movement=(0,0)):
        self.collisions = {'up':False, 'down':False, 'right':False, 'left':False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around((entity_rect.centerx, entity_rect.bottom)):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around((entity_rect.centerx, entity_rect.bottom)):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0 :
            self.flip = False
        if movement[0] < 0 :
            self.flip = True

        self.last_movement = movement

        self.air_time += 1

        if self.air_time > 60 * 3:
            self.game.dead += 1
            self.game.screenshake.update(60, self.game.screenshake.shake_value)

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0
            
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        if self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        self.animation.update()
        
    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))










