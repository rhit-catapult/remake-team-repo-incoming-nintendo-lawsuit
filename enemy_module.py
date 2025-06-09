#enemy.py

import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance=100, speed=2):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_x = x
        self.distance = distance
        self.speed = speed

        self.vel_y = 0
        self.jump = False
        self.jump_timer = random.randint(60, 180)

        self.platform_timer = 0
        self.max_platform_time = 180

    def update(self, platforms):
        self.rect.x += self.speed
        if self.rect.x > self.start_x + self.distance:
            self.speed = -abs(self.speed)
        elif self.rect.x < self.start_x:
            self.speed = abs(self.speed)

        # self.vel_y += 0.5
        self.rect.y += self.vel_y

        on_platform = False
        standing_on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0 and self.rect.bottom <= platform.top:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.jump = False
                    on_platform = True

                    if getattr(platform, "is_ground", False):
                        self.platform_timer = 0
                        standing_on_ground = True
                    else:
                        self.platform_timer += 1

        self.jump_timer -= 1
        if self.jump_timer <= 0 and not self.jump and on_platform:
            self.vel_y = -10
            self.jump = True
            self.jump_timer = random.randint(60, 180)

        if on_platform and not standing_on_ground and self.platform_timer > self.max_platform_time:
            self.vel_y = 5
            self.jump = True
