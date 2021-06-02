import os
import sys

import pygame
from pygame.locals import *

from config import Config

os.chdir(sys.path[0])  # Change de CWD to the D where the program resides


def load_image(name, path=Config.pathsprites, transparent=True):
    try:
        img = pygame.image.load(os.path.join(path, name))
    except pygame.error:
        raise SystemExit("Error al cargar la imagen %s" % name)
    img = img.convert()
    if transparent:
        color = img.get_at((0, 0))
        img.set_colorkey(color, RLEACCEL)
    return img


def load_map(name, path=Config.pathlevels):
    try:
        with open(os.path.join(path, name), "rt") as f:
            return f.readlines()
    except IOError:
        raise SystemExit("Error al cargar el nivel %s" % name)
