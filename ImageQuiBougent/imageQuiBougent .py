import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Créer une fenêtre pygame
screen = pygame.display.set_mode((800, 600))  # Fenêtre de 800x600

# Obtenir un objet clock pour gérer la fréquence de rafraîchissement
clock = pygame.time.Clock()

# Charger les images (tu peux remplacer par des images réelles)
def load_player_image():
    player_image = pygame.Surface((50, 50))  # Crée un carré rouge
    player_image.fill((255, 0, 0))           # Remplit le carré avec du rouge
    return player_image

def load_background_image():
    background_image = pygame.Surface((800, 600))  # Crée un fond de 800x600
    background_image.fill((0, 255, 0))             # Remplit le fond avec du vert
    return background_image

# Charger les images
player = load_player_image()
background = load_background_image()

# Position initiale du joueur
position = player.get_rect()

# Ajouter les constantes de largeur et de hauteur
WIDTH, HEIGHT = 800, 600
SPRITE_WIDTH, SPRITE_HEIGHT = 50, 50  # Dimensions du joueur

# Boucle principale du jeu
while True:
    # Gérer les événements (fermeture de la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Détecter les touches appuyées
    keys = pygame.key.get_pressed()

    # Déplacer le joueur selon les touches fléchées appuyées
    if keys[pygame.K_UP]:
        position.top -= 5  # Déplace le joueur vers le haut
    if keys[pygame.K_DOWN]:
        position.top += 5  # Déplace le joueur vers le bas
    if keys[pygame.K_LEFT]:
        position.left -= 5  # Déplace le joueur vers la gauche
    if keys[pygame.K_RIGHT]:
        position.left += 5  # Déplace le joueur vers la droite

    # Assurer que le joueur reste dans les limites de l'écran
    if position.left < 0:
        position.left = 0
    if position.right > WIDTH:
        position.right = WIDTH
    if position.top < 0:
        position.top = 0
    if position.bottom > HEIGHT:
        position.bottom = HEIGHT

    # Effacer l'écran (afficher le fond)
    screen.blit(background, (0, 0))

    # Dessiner le joueur à la nouvelle position
    screen.blit(player, position)

    # Mettre à jour l'affichage
    pygame.display.update()

    # Limiter la vitesse à 60 FPS
    clock.tick(60)
