import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = ""
        if type == 0:
            self.image = pygame.transform.scale(
                pygame.image.load("Gumba_Enemy.png").convert_alpha(), (40, 50)
            )
            self.type = "Gumba"
        elif type == 1:
            self.image = pygame.transform.scale(
                pygame.image.load("Glumbas_Enemy.png").convert_alpha(), (50, 50)
            )
            self.type = "Glumbas"
        elif type == 2:
            self.image = pygame.transform.scale(
                pygame.image.load("Eggumbo.png").convert_alpha(), (65, 65)
            )
            self.type = "Eggumbo"

        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.vel_x = random.choice([-2, 2])
        self.vel_y = 0
        self.flattened = False
        self.remove_timer = 0

    def update(self, platforms, enemies):
        if not self.flattened:
            # Horizontal movement
            self.rect.x += self.vel_x
            for platform in platforms:
                if self.rect.colliderect(platform):
                    if self.vel_x > 0:
                        self.rect.right = platform.left
                    else:
                        self.rect.left = platform.right
                    self.vel_x *= -1
                    break

            # Gravity
            self.vel_y += 0.5

            # Ledge detection
            ahead_x = self.rect.midbottom[0] + (self.vel_x * 5)
            ahead_y = self.rect.midbottom[1] + 1
            ahead_rect = pygame.Rect(ahead_x, ahead_y, 5, 5)

            if not any(ahead_rect.colliderect(p) for p in platforms) and self.type != "Gumba":
                self.vel_x *= -1

            # Vertical movement with collision
            dy = int(self.vel_y)
            step = 1 if dy > 0 else -1

            for _ in range(abs(dy)):
                self.rect.y += step
                for platform in platforms:
                    if self.rect.colliderect(platform):
                        if step > 0:
                            self.rect.bottom = platform.top
                            self.vel_y = 0
                        else:
                            self.rect.top = platform.bottom
                            self.vel_y = 0
                        break

        else:
            # Flattened logic
            self.remove_timer += 1
            self.vel_y += 0.5
            dy = int(self.vel_y)
            step = 1 if dy > 0 else -1

            for _ in range(abs(dy)):
                self.rect.y += step
                for platform in platforms:
                    if self.rect.colliderect(platform):
                        if step > 0:
                            self.rect.top = platform.top - 3
                            self.vel_y = 0
                        break

            if self.remove_timer >= 500:
                enemies.remove(self)
