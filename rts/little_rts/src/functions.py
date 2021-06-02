try:
    import os
    import time
    import pygame
    from pygame.locals import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


def execute_time(function):
    def new_function(*args):
        global LOG
        start = time.time()
        toret = function(*args)
        end = time.time()
        message = function.__name__ + " --> " + str(end - start) + " segundos\n"
        print(message)
        return toret

    return new_function


def write_log(cadena):
    global LOG
    if not LOG:
        with open("log.txt", "w") as f:
            f.write(cadena)
        LOG = True
    else:
        with open("log.txt", "a") as f:
            f.write(cadena)


def load_image(path, transparent=True):
    try:
        image = pygame.image.load(os.path.join(path))
    except pygame.error:
        print("Error al cargar la imagen" + path + "\n")
        write_log("Error al cargar la imagen" + path + "\n")
        raise SystemExit
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image


def distance(recta, rectb):
    return abs((recta.centerx - rectb.centerx) + (recta.centery - rectb.centery))


def path(path):
    return os.path.join(path)


def load_sprites(name, sizesprite, transparent=True):
    imagen = load_image(os.path.join(PATHS["sprites"] + name), transparent)
    rect = imagen.get_rect()
    base, altura = sizesprite
    col = rect.w // base
    fil = rect.h // altura
    sprites = []
    try:
        for f in range(fil):
            for c in range(col):
                sprite = imagen.subsurface((rect.left, rect.top, base, altura))
                sprites.append(sprite)
                rect.left += base
            rect.top += altura
            rect.left = 0
    except pygame.error:
        print("Error")
    return sprites


def terminate():
    pygame.quit()
    os.sys.exit(0)
