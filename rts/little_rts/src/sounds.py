try:
    import pygame
    from pygame.locals import *
    from functions import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


pygame.mixer.init()
SOUNDS = {
    "attack": pygame.mixer.Sound(PATHS["sounds"] + "attack.wav"),
    "deadunit": pygame.mixer.Sound(PATHS["sounds"] + "deadunit.wav"),
    "landing": pygame.mixer.Sound(PATHS["sounds"] + "landing.wav"),
}


def playsound(sound):
    SOUNDS[sound].play()
