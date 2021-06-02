import os
import pygame
from pygame.locals import *


def load_image(path, transparent=True):
    try:
        img = pygame.image.load(os.path.join(path))
    except pygame.error:
        raise SystemExit("Error al cargar la imagen" + path)
    img = img.convert()
    if transparent:
        color = img.get_at((0, 0))
        img.set_colorkey(color, RLEACCEL)
    return img
