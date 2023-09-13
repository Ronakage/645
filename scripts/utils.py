import os
import pygame

BASE_IMG_PATH = 'data/images/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img


def scaled_load_image(path, scale):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    bounding_rect = img.get_bounding_rect()
    cropped_image = pygame.Surface((bounding_rect.width, bounding_rect.height), pygame.SRCALPHA)
    cropped_image.blit(img, (0, 0), bounding_rect)
    if scale:
        scaled_image = pygame.transform.scale(cropped_image, scale)
        return scaled_image
    return  cropped_image


def load_images(path, is_scaled=False, scale=None):
    imgs = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if not is_scaled:
            imgs.append(load_image(path + '/' + img_name))
        else:
            imgs.append(scaled_load_image(path + '/' + img_name, scale))
    return imgs


class Animation:
    def __init__(self, imgs, img_dur=5, loop=True):
        self.imgs = imgs
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.imgs, self.img_dur, self.loop)

    def img(self):
        return self.imgs[int(self.frame / self.img_dur)]

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.imgs))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.imgs) - 1)
            if self.frame >= self.img_dur * len(self.imgs) - 1:
                self.done = True

    def duration(self):
        return self.img_dur * len(self.imgs)

    def reset(self):
        self.frame = 0
