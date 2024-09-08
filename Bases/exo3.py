import pygame

pygame.init()

ecran = pygame.display.set_mode((640, 480))

largeur = 100
hauteur = 10
couleur = (20, 180, 20)
continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            pygame.draw.rect(ecran, couleur, (x, y, largeur, hauteur))
        if event.type == pygame.QUIT:
            continuer = False
    pygame.display.flip()

pygame.quit()