import pygame
import sys
from player import Player
from background import Background

class Game():
    def __init__(self):
        pygame.init()

        # Initialisation de l'écran et de l'horloge
        self.background = Background('Mon_Labyrinthe/images/paysage.png')
        self.screen = pygame.display.set_mode((self.background.width, self.background.height))
        pygame.display.set_caption("Mon Jeu")

        self.clock = pygame.time.Clock()

        # Initialiser le joueur avec une position de départ (par exemple (100, 100))
        self.player = Player((100, 100))

    def run(self):
        # Boucle principale du jeu
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            # Mettre à jour les mouvements du joueur
            self.player.update(keys)

            # Dessiner le fond d'écran
            self.background.draw(self.screen)
            
            # Afficher le joueur à sa nouvelle position
            self.screen.blit(self.player.image, self.player.rect)

            # Mettre à jour l'affichage
            pygame.display.update()
            
            # Limiter le nombre de FPS à 60
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
