import pygame

class Background:
    def __init__(self, image_path):
        # Charger l'image de fond
        self.image = pygame.image.load(image_path)
        self.width, self.height = self.image.get_size()

    def draw(self, screen):
        # Afficher l'image de fond à la position (0, 0)
        screen.blit(self.image, (0, 0))
