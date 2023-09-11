import pygame


class Display:
    def __init__(self, width, height):
        self.display = pygame.Surface((width, height))
        self.outline_display = pygame.Surface((width, height), pygame.SRCALPHA)

    def get_displays(self):
        return self.display, self.outline_display

    def refresh_background(self, background_img):
        self.outline_display.fill((0, 0, 0, 0))
        self.display.blit(pygame.transform.scale(background_img, self.outline_display.get_size()), (0, 0))

    def update(self):
        display_mask = pygame.mask.from_surface(self.outline_display)
        display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.display.blit(display_sillhouette, offset)

    def render(self):
        self.display.blit(self.outline_display, (0, 0))
