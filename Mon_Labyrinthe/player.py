import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, initial_position):
        super().__init__()
        
        # Chargement des différentes images du joueur
        self.image_origin = pygame.image.load('Mon_Labyrinthe/images/player.png').convert_alpha()
        self.image_up = pygame.image.load('Mon_Labyrinthe/images/link_up.png').convert_alpha()
        self.image_left = pygame.image.load('Mon_Labyrinthe/images/link_left.png').convert_alpha()
        self.image_right = pygame.image.load('Mon_Labyrinthe/images/link_right.png').convert_alpha()

        # Image initiale du joueur
        self.image = self.image_origin
        
        # Rectangle qui entoure l'image du joueur pour gérer les positions
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position  # Position initiale du joueur
        
        # Vitesse de déplacement (en pixels)
        self.velocity = 5
    
    def update(self, keys):
        """Met à jour la position du joueur en fonction des touches pressées."""
        
        # Gérer le mouvement et l'image associée
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity  # Déplace à gauche
            self.image = self.image_left  # Change l'image vers la gauche
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity  # Déplace à droite
            self.image = self.image_right  # Change l'image vers la droite
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity  # Déplace vers le haut
            self.image = self.image_up  # Change l'image vers le haut
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity  # Déplace vers le bas
            self.image = self.image_origin  # Change l'image vers le bas ou par défaut
