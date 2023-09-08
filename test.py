import sys

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))

player_image = pygame.image.load("data/images/entities/player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (100, 100))
tile_image = pygame.image.load("data/images/tiles/grass/0.png").convert_alpha()
tile_image = pygame.transform.scale(tile_image, (100, 100))

player_mask = pygame.mask.from_surface(player_image)
tile_mask = pygame.mask.from_surface(tile_image)

player_x = 200
player_y = 200

tile_x = 100
tile_y = 100


def mask_collision(rect, mask, other_rect, other_mask):
    """
    In the mask_collision function, the offset parameter represents the relative position of rect2 (the second object) with respect to rect1 (the first object). It's a tuple (x_offset, y_offset) that describes how much rect2 is shifted horizontally and vertically relative to rect1. This offset is used when checking for collisions between the two masks.

    Here's how the offset is calculated:

    offset[0]: The horizontal (X-axis) difference between the left edge of rect2 and the left edge of rect1. If rect2 is to the left of rect1, this value will be negative. If rect2 is to the right, it will be positive.

    offset[1]: The vertical (Y-axis) difference between the top edge of rect2 and the top edge of rect1. If rect2 is above rect1, this value will be negative. If rect2 is below, it will be positive.

    The offset is used to calculate the position of the overlap (if any) between the two masks, allowing you to determine where the collision occurs relative to rect1.
    """

    offset = (int(other_rect.x - rect.x), int(other_rect.y - rect.y))
    overlap = mask.overlap(other_mask, offset)
    if overlap:
        collision_x = overlap[0] - offset[0]
        collision_y = overlap[1] - offset[1]
        # Check if there's an overlap from the top
        if offset[1] > 0:
            # top_collision = True
            print('top collision')
        # Check if there's an overlap from the bottom
        elif offset[1] < 0:
            # bottom_collision = True
            print('bottom collision')
        elif offset[0] > 0:
            print('left collision')
        # elif offset[0] < 0:
        else:
            print('right collision')

        # Create a collision point tuple
        print(overlap)

    return bool(overlap)


while True:

    mx, my = pygame.mouse.get_pos()
    player_x, player_y = mx, my
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                tile_x += -10
            if event.key == pygame.K_d:
                tile_x += 10
            if event.key == pygame.K_w:
                tile_y += -10
            if event.key == pygame.K_s:
                tile_y += 10

    # Create rectangles for the player and tiles
    player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
    tile_rect = pygame.Rect(tile_x, tile_y, tile_image.get_width(), tile_image.get_height())

    # Check for collision using masks
    if mask_collision(player_rect, player_mask, tile_rect, tile_mask):
        print(player_mask.get_rect().y)

    screen.fill((0, 0, 0))
    screen.blit(player_mask.to_surface(unsetcolor=(0,0,0,0)), (player_x, player_y))
    screen.blit(tile_image, (tile_x, tile_y))
    pygame.display.update()
