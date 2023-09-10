"""
TODO:
    1 - render the map \n
    2 - save a map \n
    3 - load a map \n
    4 - extract objects from map \n
    5 - handle enemies/spawners \n
"""
import json

import pygame

from scripts.utils import load_images


class Map:
    def __init__(self, tile_size=16):
        self.DISPLAY_WIDTH = 640
        self.DISPLAY_HEIGHT = 360

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
        }

        self.tile_size = tile_size
        self.rows = self.DISPLAY_HEIGHT // self.tile_size
        self.columns = self.DISPLAY_WIDTH // self.tile_size

        """
            'type(assets(key));type(int)'
        """
        self.grid = [["" for _ in range(self.columns)] for _ in range(self.rows)]
        self.rects = []

        self.init_fake_map()

    def init_fake_map(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if y == self.rows // 2:
                    self.grid[y][x] = "grass;0"
                    self.rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

    def decode_tile_details(self, string):
        splits = string.split(";")
        return splits[0], int(splits[1])

    def render(self, surf, offset=(0,0)):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != "":
                    tile, type = self.decode_tile_details(self.grid[y][x])
                    surf.blit(
                        self.assets[tile][type],
                        (x * self.tile_size - offset[0], y * self.tile_size - offset[1])
                    )

    def print(self, grid):
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                print("[" + grid[y][x] + "],", end="")
            print("")

    def load(self, path):
        f = open(path, 'r')
        data = json.load(f)
        self.tile_size = int(data['tile_size'])
        self.columns = self.DISPLAY_WIDTH // self.tile_size
        self.rows = self.DISPLAY_HEIGHT // self.tile_size
        self.grid = self.retrieve_grid(data['grid'])

    def decode_tile_coordinates(self, string):
        splits = string.split(";")
        return int(splits[0]), int(splits[1])

    def retrieve_grid(self, grid_dict):
        grid = [["" for _ in range(self.columns)] for _ in range(self.rows)]
        for coordinates, details in grid_dict.items():
            y,x = self.decode_tile_coordinates(coordinates)
            grid[y][x] = details
        return grid

    def save(self, path):
        f = open(path, 'w')
        json.dump({'grid': self.dump_grid(self.grid), 'tile_size': self.tile_size}, f)
        f.close()

    def dump_grid(self, grid):
        new_grid = {}
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x]:
                    new_grid[str(y) + ";" + str(x)] = grid[y][x]
        return new_grid