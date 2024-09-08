import pygame

pygame.init()


# Remplacez create_screen() par la création d'une fenêtre pygame
screen = pygame.display.set_mode((800, 600))  # Par exemple, une fenêtre 800x600

clock = pygame.time.Clock()                   # get a pygame clock object

# Supposons que vous ayez ces fonctions pour charger des images
def load_player_image():
    # Remplacez cela par le chemin réel de votre image
    player_image = pygame.Surface((50, 50))
    player_image.fill((255, 0, 0))  # remplir le joueur d'une couleur rouge par exemple
    return player_image

def load_background_image():
    # Crée un fond simple ou charge une image si nécessaire
    background_image = pygame.Surface((800, 600))
    background_image.fill((0, 255, 0))  # fond vert par exemple
    return background_image

# Charger les images
player = load_player_image()
background = load_background_image()

# Afficher le fond et le joueur
screen.blit(background, (0, 0))        # draw the background
position = player.get_rect()           # position initiale du joueur
screen.blit(player, position)          # draw the player
pygame.display.update()                # and show it all

for x in range(100):                   #animate 100 frames
    screen.blit(background, position, position) #erase
    position = position.move(2, 0)     #move player
    screen.blit(player, position)      #draw new player
    pygame.display.update()            #and show it all
    clock.tick(60)                     #update 60 times per second

pygame.quit()
