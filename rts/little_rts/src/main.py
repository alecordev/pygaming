import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
os.chdir(here)


try:
    import sys
    import time
    import random
    import pygame
    import map
    import team
    import interface
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


def main():
    main_clock = pygame.time.Clock()
    gui = interface.Interface()
    teama = team.Team("a", gui.map)
    teamb = team.Team("b", gui.map)
    teamc = team.Team("c", gui.map)
    teams = [teamc, teama, teamb]
    gui.linkteams((teama, teamb, teamc))
    while True:
        gui.map.clean()
        for i in teams:
            i.draw(gui.map.image)
            i.update()
        gui.draw()
        gui.map.scroll(pygame.mouse.get_pos())
        teama.collisions(teamb, teamc)
        teamb.collisions(teama, teamc)
        teama.conquest(teamc)
        teamb.conquest(teamc)
        gui.help(pygame.mouse.get_pos())
        if gui.map.cameraistopleft():
            teams = [teamc, teama, teamb]
        else:
            teams = [teamc, teamb, teama]
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                terminate()
            elif eventos.type == MOUSEBUTTONDOWN:
                if eventos.button == 1:
                    gui.managementclick(pygame.mouse.get_pos(), 1)
                elif eventos.button == 3:
                    gui.managementclick(pygame.mouse.get_pos(), 2)
            elif eventos.type == KEYDOWN:
                print(eventos.key)
                if eventos.key == 127:
                    teama.supr()
                elif eventos.key == 282:
                    gui.revealmap()
        # teama.automata(teamb, teamc)
        teamb.automata(teama, teamc)
        pygame.display.flip()
        main_clock.tick(60)


if __name__ == "__main__":
    main()
