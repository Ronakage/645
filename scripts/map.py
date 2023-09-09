"""
TODO:
    1 - render the map \n
    2 - save a map \n
    3 - load a map \n
    4 - extract objects from map \n
    5 - handle enemies/spawners \n
"""
import pygame

from scripts.utils import load_images


class Map:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
        }
        self.tile_size = tile_size
        self.rows = self.game.DISPLAY_HEIGHT // self.tile_size
        self.columns = self.game.DISPLAY_WIDTH // self.tile_size
        """
            'type(assets(key));type(int)'
        """
        self.grid = [["" for _ in range(self.columns)] for _ in range(self.rows)]
        self.rects = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.masks = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.spawners = []
        self.init_fake_map()
        # self.print()

    def init_fake_map(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if y == self.rows // 2:
                    self.grid[y][x] = "grass;0"
                    self.rects[y][x] = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    self.masks[y][x] = pygame.mask.from_surface(self.assets["grass"][0])

    def decode(self, string):
        splits = string.split(";")
        return splits[0], int(splits[1])

    def render(self, offset=(0,0)):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != "":
                    tile, type = self.decode(self.grid[y][x])
                    self.game.display.blit(
                        self.assets[tile][type],
                        (x * self.tile_size - offset[0], y * self.tile_size - offset[1])
                    )

    def print(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                print("[" + self.grid[y][x] + "],", end="")
            print("")
        for y in range(len(self.rects)):
            for x in range(len(self.rects[y])):
                print("[" + str(self.rects[y][x]) + "],", end="")
            print("")
        for y in range(len(self.masks)):
            for x in range(len(self.masks[y])):
                print("[" + str(self.masks[y][x]) + "],", end="")
            print("")






