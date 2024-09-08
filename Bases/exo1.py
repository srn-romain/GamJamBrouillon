import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDHT = 1024
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDHT,SCREEN_HEIGHT))
pygame.display.set_caption("Exo1")

run = True

while run:

    for event in pygame.event.get():
        #exit condition (si la croix est cliqué OU (si une touche est cliqué ET que cette touche est ECHAP))
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_f):
            run = False

pygame.quit()