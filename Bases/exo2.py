import pygame

pygame.init()

ecran = pygame.display.set_mode((640, 480))
clem = pygame.image.load("./image/langue.png").convert_alpha()
pos_clem = (0, 0)

continuer = True

while continuer:
    pygame.draw.rect(ecran, (255, 255, 255), (0, 0, 640, 480))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            pos_clem = event.pos
        if event.type == pygame.QUIT:
            continuer = False
    ecran.blit(clem, pos_clem)
    pygame.display.flip()
pygame.quit()