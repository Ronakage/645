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

        self.file = 'data/maps/future1.json'
        self.map = Map(tile_size=24)
        try:
            self.map.load(self.file)
        except FileNotFoundError:
            pass

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass', True, (self.map.tile_size, self.map.tile_size)),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone', True, (self.map.tile_size, self.map.tile_size)),
            'spawners': load_images('tiles/spawners')
        }

        self.tiles = list(self.assets.keys())
        self.selected_tile = self.tiles[1]
        self.selected_type = 0

        self.movement = [False, False, False, False]

        self.scroll = [0, 0]

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)

        self.need_help = False

    def display_text(self, txt, pos):
        txt = self.font.render(txt, True, (255, 255, 255))
        self.screen.blit(txt, pos)

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
            mpos = (int(mpos[0]/self.diff_scale_x), int(mpos[1]/self.diff_scale_y))
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
                for coordinates, details in self.map.offgrid.copy().items():
                    y,x = int(coordinates.split(";")[0]),  int(coordinates.split(";")[1])
                    tile, type = details.split(";")[0], int(details.split(";")[1])
                    img = self.assets[tile][type]
                    rect = pygame.Rect(x - self.scroll[0], y - self.scroll[1], img.get_width(), img.get_height())
                    if rect.collidepoint(mpos):
                        self.map.offgrid.pop(coordinates)

            self.display.blit(current_tile_img, (5,5))


            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.map.offgrid[str(mpos[1]) + ";" + str(mpos[0])] = str(self.selected_tile) + ";" + str(self.selected_type)
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.selected_type = (self.selected_type - 1) % len(self.assets[self.selected_tile])
                        if event.button == 5:
                            self.selected_type = (self.selected_type + 1) % len(self.assets[self.selected_tile])
                    else:
                        if event.button == 4:
                            self.selected_tile = self.tiles[(self.tiles.index(self.selected_tile) - 1) % len(self.tiles)]
                            self.selected_type = 0
                        if event.button == 5:
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
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.map.save(self.file)
                    if event.key == pygame.K_t:
                        self.map.autotile()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_h:
                        self.need_help = not self.need_help
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
                    self.map.save(self.file)
                    pygame.quit()
                    sys.exit()


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            self.display_text("M_POS : " + str(mpos), (self.screen.get_width() - 170, 0))
            self.display_text("TILE_POS : " + str(tile_pos), (self.screen.get_width() - 170, 20))
            self.display_text("TILE_SIZE : " + str(self.map.tile_size), (self.screen.get_width() - 170, 40))
            self.display_text("ON GRID : " + str(self.ongrid),(self.screen.get_width() - 170, 60))
            self.display_text("TILE : " + str(self.selected_tile), (self.screen.get_width() - 170, 80))
            self.display_text("TYPE : " + str(self.selected_type), (self.screen.get_width() - 170, 100))
            self.display_text("OUTPUT : " + str(self.file), (0, self.screen.get_height() - 30))

            if self.need_help:
                self.display_text("WASD : Move Camera",
                                  (self.screen.get_width()//2, self.screen.get_height() - 170))
                self.display_text("Scroll : Tile Switch" , (self.screen.get_width() //2, self.screen.get_height() - 150))
                self.display_text("Shift & Scroll : Type Switch",
                                  (self.screen.get_width()//2, self.screen.get_height() - 130))
                self.display_text("Left Click : Place Tile",
                                  (self.screen.get_width()//2, self.screen.get_height() - 110))
                self.display_text("Right Click : Remove Tile",
                                  (self.screen.get_width()//2, self.screen.get_height() - 90))
                self.display_text("G : Switch ON/OFF Grid",
                                  (self.screen.get_width()//2, self.screen.get_height() - 70))
                self.display_text("T : Autotile",
                                  (self.screen.get_width()//2, self.screen.get_height() - 50))
                self.display_text("O : Save File",
                                  (self.screen.get_width()//2, self.screen.get_height() - 30))
            else:
                self.display_text("H : Need Help?",
                                  (self.screen.get_width() - 120, self.screen.get_height() - 15))

            pygame.display.update()
            self.clock.tick(60)


Editor().run()




