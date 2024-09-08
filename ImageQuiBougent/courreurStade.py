import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Charger l'image de fond
def load_background_image():
    background_image = pygame.image.load('ImageQuiBougent/image/stade.png')  # Charger l'image du fichier
    return background_image

# Charger l'image du joueur
def load_player_image():
    player_image = pygame.image.load('ImageQuiBougent/image/courreur.jpg')  # Charger l'image du fichier
    return player_image

# Charger les images
background = load_background_image()
player = load_player_image()

# Obtenir les dimensions de l'image de fond
WIDTH, HEIGHT = background.get_size()

# Créer une fenêtre pygame avec les dimensions de l'image
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Obtenir un objet clock pour gérer la fréquence de rafraîchissement
clock = pygame.time.Clock()

# Position initiale du joueur
position = player.get_rect()

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
