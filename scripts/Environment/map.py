"""
TODO:
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
        self.MAX_MAP_SIZE = 10

        self.tile_size = tile_size
        self.assets = {
            'decor': load_images('tiles/decor', ),
            'grass': load_images('tiles/grass', True, (self.tile_size, self.tile_size)),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone', True, (self.tile_size, self.tile_size)),
        }

        self.rows = self.DISPLAY_HEIGHT // self.tile_size
        self.columns = self.DISPLAY_WIDTH // self.tile_size

        """
            'type(assets(key));type(int)'
        """
        self.grid = [["" for _ in range(self.columns*self.MAX_MAP_SIZE)] for _ in range(self.rows*self.MAX_MAP_SIZE)]
        self.offgrid = {}
        self.rects = []


    def decode_tile_details(self, string):
        splits = string.split(";")
        return splits[0], int(splits[1])

    def render(self, surf, offset=(0,0)):
        for coordinate, details in self.offgrid.items():
            y, x = self.decode_tile_coordinates(coordinate)
            tile, type = self.decode_tile_details(details)
            img = self.assets[tile][type]
            surf.blit(img, (x-offset[0], y-offset[1]))
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != "":
                    tile, type = self.decode_tile_details(self.grid[y][x])
                    surf.blit(
                        self.assets[tile][type],
                        (x * self.tile_size - offset[0], y * self.tile_size - offset[1])
                    )
        # for rect in self.rects:
        #     pygame.draw.rect(surf, (255,0,0), rect,  2)

    def print(self, grid):
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                print("[" + grid[y][x] + "],", end="")
            print("")

    def autotile(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.tile_check(y,x):
                    if self.tile_check(y-1, x-1) and self.tile_check(y-1, x) and self.tile_check(y-1, x + 1) and self.tile_check(y, x - 1) and self.tile_check(y, x + 1) and self.tile_check(y + 1, x - 1) and self.tile_check(y + 1, x) and self.tile_check(y + 1, x + 1) :
                        self.grid[y][x] = self.grid[y][x][:-1] + "8"
                    elif self.tile_check(y-1, x) and self.tile_check(y-1, x+1) and self.tile_check(y,x+1) and self.tile_check(y+1, x) and self.tile_check(y+1, x+1):
                        self.grid[y][x] = self.grid[y][x][:-1] + "7"
                    elif self.tile_check(y-1, x) and self.tile_check(y-1, x+1) and self.tile_check(y, x+1) and not self.tile_check(y-1, x-1):
                        self.grid[y][x] = self.grid[y][x][:-1] + "6"
                    elif self.tile_check(y, x-1) and self.tile_check(y-1, x-1) and self.tile_check(y-1, x) and self.tile_check(y-1, x+1) and self.tile_check(y, x+1):
                        self.grid[y][x] = self.grid[y][x][:-1] + "5"
                    elif self.tile_check(y-1, x) and self.tile_check(y-1, x-1) and self.tile_check(y, x-1) and not self.tile_check(y,x+1):
                        self.grid[y][x] = self.grid[y][x][:-1] + "4"
                    elif self.tile_check(y-1, x) and self.tile_check(y-1, x-1) and self.tile_check(y,x-1) and self.tile_check(y+1, x-1) and self.tile_check(y+1, x):
                        self.grid[y][x] = self.grid[y][x][:-1] + "3"
                    elif self.tile_check(y+1, x) and self.tile_check(y+1, x-1) and self.tile_check(y, x-1) and not self.tile_check(y, x+1):
                        self.grid[y][x] = self.grid[y][x][:-1] + "2"
                    elif self.tile_check(y, x-1) and self.tile_check(y+1, x-1) and self.tile_check(y+1, x) and self.tile_check(y+1, x+1) and self.tile_check(y, x+1):
                        self.grid[y][x] = self.grid[y][x][:-1] + "1"
                    elif self.tile_check(y, x+1) and self.tile_check(y+1, x+1) and self.tile_check(y+1, x) and not self.tile_check(y, x-1):
                        self.grid[y][x] = self.grid[y][x][:-1] + "0"

    def tile_check(self, y, x):
        try:
            if self.grid[y][x] != "":
                return True
        except:
            return False

    def load(self, path):
        f = open(path, 'r')
        data = json.load(f)
        self.tile_size = int(data['tile_size'])
        self.columns = self.DISPLAY_WIDTH // self.tile_size
        self.rows = self.DISPLAY_HEIGHT // self.tile_size
        self.grid = self.retrieve_grid(data['grid'])
        self.offgrid = data['offgrid']
        self.assets = {
            'decor': load_images('tiles/decor', ),
            'grass': load_images('tiles/grass', True, (self.tile_size, self.tile_size)),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone', True, (self.tile_size, self.tile_size)),
        }
        self.rects = self.define_rects()

    def decode_tile_coordinates(self, string):
        splits = string.split(";")
        return int(splits[0]), int(splits[1])

    def retrieve_grid(self, grid_dict):
        grid = [["" for _ in range(self.columns*self.MAX_MAP_SIZE)] for _ in range(self.rows*self.MAX_MAP_SIZE)]
        for coordinates, details in grid_dict.items():
            y,x = self.decode_tile_coordinates(coordinates)
            grid[y][x] = details
        return grid

    def define_rects(self):
        rects = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != "":
                    tile, type = self.decode_tile_details(self.grid[y][x])
                    img = self.assets[tile][type]
                    rect = pygame.Rect(x*img.get_width(), y*img.get_height(), img.get_width(), img.get_height())
                    rects.append(rect)
        return rects

    def save(self, path):
        f = open(path, 'w')
        json.dump({'grid': self.dump_grid(self.grid), 'offgrid':self.offgrid ,'tile_size': self.tile_size}, f)
        f.close()

    def dump_grid(self, grid):
        new_grid = {}
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x]:
                    new_grid[str(y) + ";" + str(x)] = grid[y][x]
        return new_grid