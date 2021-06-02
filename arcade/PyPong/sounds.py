import pygame

from config import Config

pygame.mixer.init()

hit = pygame.mixer.Sound(Config.path_hitsound)
goal = pygame.mixer.Sound(Config.path_goalsound)
