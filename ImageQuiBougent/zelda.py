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

# Obtenir les dimensions de l'image de fond
WIDTH, HEIGHT = background.get_size()

# Créer une fenêtre pygame avec les dimensions de l'image
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Obtenir un objet clock pour gérer la fréquence de rafraîchissement
clock = pygame.time.Clock()

# Position initiale du joueur
initial_position = (85, 543)  # Coordonnées de départ du joueur
player_rect = player_normal.get_rect(topleft=initial_position)

# Variables de saut
is_jumping = False
jump_speed = 10
gravity = 0.5
jump_velocity = 0

# Fonction pour obtenir la hauteur du sol à une position x donnée
def get_ground_height(x):
    if x < 0 or x >= WIDTH:
        return HEIGHT
    for y in range(HEIGHT - 1, -1, -1):
        color = background.get_at((x, y))
        if color[3] != 0:
            return y
    return HEIGHT

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
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        jump_velocity = jump_speed
    
    if is_jumping:
        player_rect.top -= jump_velocity
        jump_velocity -= gravity
        if player_rect.bottom > get_ground_height(player_rect.centerx):
            player_rect.bottom = get_ground_height(player_rect.centerx)
            is_jumping = False
            jump_velocity = 0

    # Déplacement horizontal
    if keys[pygame.K_LEFT]:
        player_rect.left -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.left += 5

    # Mettre à jour la position verticale du joueur pour qu'il reste sur le sol
    if not is_jumping:
        ground_height = get_ground_height(player_rect.centerx)
        if player_rect.bottom > ground_height:
            player_rect.bottom = ground_height

    # Effacer l'écran (afficher le fond)
    screen.blit(background, (0, 0))

    # Dessiner le joueur à la nouvelle position
    if is_jumping:
        screen.blit(player_jump, player_rect)
    else:
        screen.blit(player_normal, player_rect)

    # Mettre à jour l'affichage
    pygame.display.update()

    # Limiter la vitesse à 60 FPS
    clock.tick(60)
