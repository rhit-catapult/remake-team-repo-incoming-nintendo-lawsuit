import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = ""
        if type == 0:

            self.image = pygame.transform.scale(
                pygame.image.load("Gumba_Enemy.png").convert_alpha(),
                (40, 50)
            )
            self.type = "Gumba"
        elif type== 1:
            self.image = pygame.transform.scale(
                pygame.image.load("Glumbas_Enemy.png").convert_alpha(),
                (50, 50)
            )
            self.type = "Glumbas"
        elif type==2:
            self.image = pygame.transform.scale(pygame.image.load("Eggumbo.png").convert_alpha(),
            (65,65))
            self.type = "Eggumbo"
        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_x = x
        self.vel_x = random.choice([-2, 2])

        self.vel_y = 0
        self.Ejump = False
        self.Ejump_timer = 0
        self.flattened = False
        self.platform_timer = 0
        self.max_platform_time = 180
        self.remove_timer = 0

    def update(self, platforms,enemies):
        # Horizontal movement & boundaries
        if not self.flattened:
            self.rect.x += self.vel_x
            for platform in platforms:
                if self.rect.colliderect(platform):
                    if self.vel_x > 0:  # Moving right, hit wall
                        self.rect.right = platform.left
                    elif self.vel_x < 0:  # Moving left, hit wall
                        self.rect.left = platform.right
                    self.vel_x *= -1  # Reverse direction
                    break  # Stop checking after first wall hit
            # Apply gravity velocity
            self.vel_y += 0.5

            # Ledge detection
            ahead_x = self.rect.midbottom[0] + (self.vel_x * 5)
            ahead_y = self.rect.midbottom[1] + 1  # Just below the bottom of the enemy
            ahead_rect = pygame.Rect(ahead_x, ahead_y, 5, 5)

            ground_ahead = False
            for platform in platforms:
                if ahead_rect.colliderect(platform):
                    ground_ahead = True
                    break

            if not ground_ahead and not self.type == "Gumba":
                self.vel_x *= -1  # Turn around if there's no ground ahead

            # Vertical movement with collision stepwise resolution
            dy = self.vel_y
            step = 1 if dy > 0 else -1

            for _ in range(abs(int(dy))):
                self.rect.y += step
                for platform in platforms:
                    if self.rect.colliderect(platform):
                        if step > 0:  # Moving down, landed on platform
                            self.rect.bottom = platform.top
                            self.vel_y = 0
                            self.jump = False
                        elif step < 0:  # Moving up, hit ceiling
                            self.rect.top = platform.bottom
                            self.vel_y = 0
                        break  # No need to check other platforms this pixel move

            # After moving pixel by pixel vertically, check if on platform:
            on_platform = False
            standing_on_ground = False
            for platform in platforms:
                if self.rect.bottom == platform.top and self.rect.right > platform.left and self.rect.left < platform.right:
                    on_platform = True
                    if hasattr(platform, "is_ground") and platform.is_ground:
                        standing_on_ground = True

            # Jump timer and jump logic remain the same
            self.Ejump_timer -= 1
            if self.Ejump_timer <= 0 and not self.Ejump and on_platform:
                self.vel_y = -1
                self.Ejump = True
                self.Ejump_timer = random.randint(1, 3)

            if on_platform and not standing_on_ground and self.platform_timer > self.max_platform_time:
                self.vel_y = 5
                self.Ejump = True
        else:
            self.remove_timer += 1
            self.vel_y += 0.5
            dy = self.vel_y
            step = 1 if dy > 0 else -1

            for _ in range(abs(int(dy))):
                self.rect.y += step

                for platform in platforms:
                    if self.rect.colliderect(platform):
                        if step > 0: #a
                            self.rect.top = platform.top - 3
                            self.vel_y = 0
                        break
            if self.remove_timer >= 500:
                enemies.remove(self)
