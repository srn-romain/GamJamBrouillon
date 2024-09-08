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
        self.rect = self.normal_image.get_rect(topleft=initial_position)
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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys)

            self.background.draw(self.screen)
            self.screen.blit(self.player.handle_movement(keys), self.player.rect)
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
