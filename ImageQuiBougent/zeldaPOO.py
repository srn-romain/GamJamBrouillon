import pygame
import sys

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.width, self.height = self.image.get_size()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Player:
    def __init__(self, normal_path, jump_path, back_path, repos_path, initial_position):
        self.normal_image = pygame.image.load(normal_path)
        self.jump_image = pygame.image.load(jump_path)
        self.back_image = pygame.image.load(back_path)
        self.repos_image = pygame.image.load(repos_path)
        self.rect = self.normal_image.get_rect(midbottom=(initial_position[0], initial_position[1]))
        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 0.5
        self.jump_velocity = 0

    def handle_movement(self, keys):
        if keys[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = self.jump_speed

        if self.is_jumping:
            self.rect.top -= self.jump_velocity
            self.jump_velocity -= self.gravity
            if self.rect.bottom > 660:  # Fixe la hauteur du sol
                self.rect.bottom = 660
                self.is_jumping = False
                self.jump_velocity = 0

        if keys[pygame.K_LEFT] and not self.is_jumping:
            self.rect.left -= 5
            return self.back_image
        elif keys[pygame.K_RIGHT] and not self.is_jumping:
            self.rect.left += 5
            return self.normal_image
        elif self.is_jumping:
            return self.jump_image
        else:
            return self.repos_image

class Game:
    def __init__(self):
        pygame.init()
        self.background = Background('ImageQuiBougent/image/paysage.jpg')
        self.player = Player(
            'ImageQuiBougent/image/sprite.png',
            'ImageQuiBougent/image/sprite_saut.png',
            'ImageQuiBougent/image/sprite_arriere.png',
            'ImageQuiBougent/image/sprite_repos.png',
            (85, 660)
        )
        self.screen = pygame.display.set_mode((self.background.width, self.background.height))
        self.clock = pygame.time.Clock()

        # Variable pour l'écran d'accueil
        self.ecran_du_debut = True

        self.image_accueil = pygame.image.load('ImageQuiBougent/image/accueil_image.jpg')
        self.image_accueil = pygame.transform.scale(self.image_accueil, (400, 200))

    def afficher_ecran_d_accueil(self):
        """Affiche l'écran d'accueil principal avec un message."""
        while self.ecran_du_debut:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Passer au deuxième écran d'accueil
                        self.ecran_du_debut = False
                        self.ecran_accueil_deux()

            # Remplir l'écran de noir
            self.screen.fill((0, 0, 0))

            # Afficher l'image d'accueil
            self.screen.blit(self.image_accueil, (self.background.width // 2 - 200, 100))  # Centrer l'image

            # Afficher les messages
            self.creer_message('grande', 'Bienvenue au Jeu', (self.background.width // 2 - 150, 350, 300, 50), (255, 255, 255))
            self.creer_message('moyenne', 'Appuyez sur Entrée pour continuer', (self.background.width // 2 - 200, 450, 400, 50), (255, 255, 255))

            pygame.display.update()
            self.clock.tick(30)


    def ecran_accueil_deux(self):
        """Affiche le deuxième écran d'accueil où les joueurs peuvent entrer leurs noms."""
        joueur_1_nom = ""
        joueur_2_nom = ""
        saisie_joueur_1 = True
        saisie_joueur_2 = False

        while self.ecran_du_debut == False:  # Deuxième écran actif
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if saisie_joueur_1:
                            saisie_joueur_1 = False
                            saisie_joueur_2 = True
                        elif saisie_joueur_2 and joueur_2_nom != "":
                            # Conserver les noms des joueurs
                            self.nom_joueur_1 = joueur_1_nom
                            self.nom_joueur_2 = joueur_2_nom
                            self.ecran_du_debut = None  # Terminer l'écran d'accueil 2
                    elif event.key == pygame.K_BACKSPACE:
                        if saisie_joueur_1:
                            joueur_1_nom = joueur_1_nom[:-1]
                        elif saisie_joueur_2:
                            joueur_2_nom = joueur_2_nom[:-1]
                    else:
                        if saisie_joueur_1:
                            joueur_1_nom += event.unicode
                        elif saisie_joueur_2:
                            joueur_2_nom += event.unicode

            # Remplir l'écran de noir
            self.screen.fill((0, 0, 0))

            # Afficher les messages d'instructions et champs de texte
            self.creer_message('moyenne', 'Entrer le nom des joueurs', (self.background.width // 2 - 150, 250, 300, 50), (255, 255, 255))

            # Champs de texte pour joueur 1 et joueur 2
            self.creer_message('moyenne', f"Joueur 1: {joueur_1_nom}", (self.background.width // 2 - 150, 350, 300, 50), (255, 255, 255))
            self.creer_message('moyenne', f"Joueur 2: {joueur_2_nom}", (self.background.width // 2 - 150, 400, 300, 50), (255, 255, 255))

            # Si les noms sont remplis, indiquer que l'utilisateur peut commencer le jeu
            if saisie_joueur_2 and joueur_2_nom != "":
                self.creer_message('moyenne', 'Appuyez sur Entrée pour commencer', (self.background.width // 2 - 200, 500, 400, 50), (255, 255, 255))

            pygame.display.update()
            self.clock.tick(30)

    def creer_message(self, font, message, message_rectangle, couleur):
        """Affiche un message à l'écran."""
        if font == 'petite':
            font = pygame.font.SysFont('Lato', 20, False)
        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato', 30, False)
        elif font == 'grande':
            font = pygame.font.SysFont('Lato', 40, True)

        texte = font.render(message, True, couleur)
        self.screen.blit(texte, message_rectangle)

    def run(self):
        # Appeler l'écran d'accueil avant de démarrer le jeu
        self.afficher_ecran_d_accueil()
        

        # Boucle principale du jeu
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            self.background.draw(self.screen)
            self.screen.blit(self.player.handle_movement(keys), self.player.rect)
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
