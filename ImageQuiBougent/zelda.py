import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Charger l'image de fond
def load_background_image():
    background_image = pygame.image.load('ImageQuiBougent/image/paysage.jpg')
    return background_image

# Charger l'image du joueur
def load_player_image(normal=True):
    image_path = 'ImageQuiBougent/image/sprite.png' if normal else 'ImageQuiBougent/image/sprite_saut.png'
    player_image = pygame.image.load(image_path)
    return player_image

# Charger les images
background = load_background_image()
player_normal = load_player_image(normal=True)
player_jump = load_player_image(normal=False)
player_back = pygame.image.load('ImageQuiBougent/image/sprite_arriere.png')
player_repos = pygame.image.load('ImageQuiBougent/image/sprite_repos.png')

# Obtenir les dimensions de l'image de fond
WIDTH, HEIGHT = background.get_size()

# Créer une fenêtre pygame avec les dimensions de l'image
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Obtenir un objet clock pour gérer la fréquence de rafraîchissement
clock = pygame.time.Clock()

# Position initiale du joueur
initial_position = (85, 660)
player_rect = player_normal.get_rect(topleft=(85, 660 - player_normal.get_height()))

# Variables de saut
is_jumping = False
jump_speed = 10
gravity = 0.5
jump_velocity = 0

# Fonction pour obtenir la hauteur du sol
def get_ground_height(x):
    return 660  # Fixer la hauteur du sol à 660 px

# Boucle principale du jeu
while True:
    # Gérer les événements (fermeture de la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Détecter les touches appuyées
    keys = pygame.key.get_pressed()

    # Gestion du saut
    if keys[pygame.K_UP] and not is_jumping:
        is_jumping = True
        jump_velocity = jump_speed

    if is_jumping:
        player_rect.top -= jump_velocity
        jump_velocity -= gravity
        if player_rect.bottom > 660:  # Si le joueur est en dessous du sol à 660 px
            player_rect.bottom = 660  # Fixer sa position à la hauteur du sol
            is_jumping = False
            jump_velocity = 0

    # Effacer l'écran (afficher le fond)
    screen.blit(background, (0, 0))

    # Gestion des mouvements et de l'affichage des sprites
    if keys[pygame.K_LEFT] and not is_jumping:
        player_rect.left -= 5  # Déplacement à gauche
        screen.blit(player_back, player_rect)  # Afficher le sprite arrière
    elif keys[pygame.K_RIGHT] and not is_jumping:
        player_rect.left += 5  # Déplacement à droite
        screen.blit(player_normal, player_rect)  # Afficher le sprite normal (vers l'avant)
    elif is_jumping:
        screen.blit(player_jump, player_rect)  # Afficher le sprite de saut
    else:
        screen.blit(player_repos, player_rect)  # Afficher le sprite normal si aucune touche n'est appuyée

    # Mettre à jour l'affichage
    pygame.display.update()

    # Limiter la vitesse à 60 FPS
    clock.tick(60)
