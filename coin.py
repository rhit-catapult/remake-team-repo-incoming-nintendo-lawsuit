import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("Coin.png").convert_alpha(), (25, 25)
        )
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
