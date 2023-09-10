import sys
import pygame

from scripts.map import Map
from scripts.utils import load_images


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Level Editor')

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.display = pygame.Surface((640, 360))
        self.diff_scale_x = self.screen.get_width() / self.display.get_width()
        self.diff_scale_y = self.screen.get_height() / self.display.get_height()
        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners')
        }

        self.tiles = list(self.assets.keys())
        self.selected_tile = self.tiles[1]
        self.selected_type = 0

        self.movement = [False, False, False, False]

        self.map = Map()
        try:
            self.map.load('data/maps/future.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while 1:
            self.display.fill((0,0,0))

            self.scroll[0] += (self.movement[1] - self.movement[0])
            self.scroll[1] += (self.movement[3] - self.movement[2])
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.map.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.selected_tile][self.selected_type].copy()
            current_tile_img.set_alpha(150)

            self.display.blit(current_tile_img, (5,5))

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0]/self.diff_scale_x, mpos[1]/self.diff_scale_y)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.map.tile_size), int((mpos[1] + self.scroll[1]) // self.map.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.map.tile_size - self.scroll[0], tile_pos[1] * self.map.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.map.grid[tile_pos[1]][tile_pos[0]] = str(self.selected_tile) + ";" + str(self.selected_type)

            if self.right_clicking:
                x,y = tile_pos[0] , tile_pos[1]
                if self.map.grid[y][x] != "":
                    self.map.grid[y][x] = ""
                # for tile in self.map.offgrid_tiles.copy():
                #     tile_img = self.assets[tile['type']][tile['variant']]
                #     tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                #     if tile_r.collidepoint(mpos):
                #         self.map.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5,5))


            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pass
                        self.clicking = True
                        # if not self.ongrid:
                        #     self.map.offgrid_tiles.append({'type':self.tile_list[self.tile_group], 'variant':self.tile_variant, 'pos':(mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        pass
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            pass
                            self.selected_type = (self.selected_type - 1) % len(self.assets[self.selected_tile])
                        if event.button == 5:
                            pass
                            self.selected_type = (self.selected_type + 1) % len(self.assets[self.selected_tile])
                    else:
                        if event.button == 4:
                            pass
                            self.selected_tile = self.tiles[(self.tiles.index(self.selected_tile) - 1) % len(self.tiles)]
                            self.selected_type = 0
                        if event.button == 5:
                            pass
                            self.selected_tile = self.tiles[(self.tiles.index(self.selected_tile)  + 1) % len(self.tiles)]
                            self.selected_type = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        pass
                        # self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.map.save('data/maps/future.json')
                    if event.key == pygame.K_t:
                        pass
                        # self.map.autotile()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

                if event.type == pygame.QUIT:
                    self.map.save('data/maps/future.json')
                    pygame.quit()
                    sys.exit()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()



# class Editor:
#     def __init__(self):
#         pygame.init()
#         pygame.display.set_caption('Level Editor')
#
#         self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#         self.display = pygame.Surface((640, 360))
#         self.clock = pygame.time.Clock()
#
#         self.assets = {
#             'decor': load_images('tiles/decor'),
#             'grass': load_images('tiles/grass'),
#             'large_decor': load_images('tiles/large_decor'),
#             'stone': load_images('tiles/stone'),
#             'spawners' : load_images('tiles/spawners')
#         }
#
#         self.movement = [False, False, False, False]
#
#         self.map = TileMap(self)
#         try:
#             self.map.load('data/maps/current.json')
#         except FileNotFoundError:
#             pass
#
#         self.scroll = [0, 0]
#
#         self.tile_list = list(self.assets)
#         self.tile_group = 0
#         self.tile_variant = 0
#
#         self.clicking = False
#         self.right_clicking = False
#         self.shift = False
#         self.ongrid = True
#
#     def run(self):
#         while True:
#             self.display.fill((0,0,0))
#
#             self.scroll[0] += (self.movement[1] - self.movement[0])
#             self.scroll[1] += (self.movement[3] - self.movement[2])
#             render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
#
#             self.map.render(self.display, offset=render_scroll)
#
#             current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
#             current_tile_img.set_alpha(150)
#
#             mpos = pygame.mouse.get_pos()
#             mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
#             tile_pos = (int((mpos[0] + self.scroll[0]) // self.map.tile_size), int((mpos[1] + self.scroll[1]) // self.map.tile_size))
#
#             if self.ongrid:
#                 self.display.blit(current_tile_img, (tile_pos[0] * self.map.tile_size - self.scroll[0], tile_pos[1] * self.map.tile_size - self.scroll[1]))
#             else:
#                 self.display.blit(current_tile_img, mpos)
#
#             if self.clicking and self.ongrid:
#                 self.map.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant':self.tile_variant, 'pos':tile_pos}
#
#             if self.right_clicking:
#                 tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
#                 if tile_loc in self.map.tilemap:
#                     del self.map.tilemap[tile_loc]
#                 for tile in self.map.offgrid_tiles.copy():
#                     tile_img = self.assets[tile['type']][tile['variant']]
#                     tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
#                     if tile_r.collidepoint(mpos):
#                         self.map.offgrid_tiles.remove(tile)
#
#             self.display.blit(current_tile_img, (5,5))
#
#             for event in pygame.event.get():
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if event.button == 1:
#                         self.clicking = True
#                         if not self.ongrid:
#                             self.map.offgrid_tiles.append({'type':self.tile_list[self.tile_group], 'variant':self.tile_variant, 'pos':(mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
#                     if event.button == 3:
#                         self.right_clicking = True
#                     if self.shift:
#                         if event.button == 4:
#                             self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
#                         if event.button == 5:
#                             self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
#                     else:
#                         if event.button == 4:
#                             self.tile_group = (self.tile_group - 1) % len(self.tile_list)
#                             self.tile_variant = 0
#                         if event.button == 5:
#                             self.tile_group = (self.tile_group + 1) % len(self.tile_list)
#                             self.tile_variant = 0
#                 if event.type == pygame.MOUSEBUTTONUP:
#                     if event.button == 1:
#                         self.clicking = False
#                     if event.button == 3:
#                         self.right_clicking = False
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_a:
#                         self.movement[0] = True
#                     if event.key == pygame.K_d:
#                         self.movement[1] = True
#                     if event.key == pygame.K_w:
#                         self.movement[2] = True
#                     if event.key == pygame.K_s:
#                         self.movement[3] = True
#                     if event.key == pygame.K_g:
#                         self.ongrid = not self.ongrid
#                     if event.key == pygame.K_o:
#                         self.map.save('data/maps/current.json')
#                     if event.key == pygame.K_t:
#                         self.map.autotile()
#                     if event.key == pygame.K_LSHIFT:
#                         self.shift = True
#                 if event.type == pygame.KEYUP:
#                     if event.key == pygame.K_a:
#                         self.movement[0] = False
#                     if event.key == pygame.K_d:
#                         self.movement[1] = False
#                     if event.key == pygame.K_w:
#                         self.movement[2] = False
#                     if event.key == pygame.K_s:
#                         self.movement[3] = False
#                     if event.key == pygame.K_LSHIFT:
#                         self.shift = False
#
#                 if event.type == pygame.QUIT:
#                     self.map.save('data/maps/current.json')
#                     pygame.quit()
#                     sys.exit()
#
#             self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
#             pygame.display.update()
#             self.clock.tick(60)
#
#
# Editor().run()
