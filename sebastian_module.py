import pygame
import sys


#initialize
pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
white = (255, 255, 255)
pygame.display.set_caption('Game')

clock = pygame.time.Clock()
platform_img = pygame.image.load("grass-pl.png").convert_alpha()
platform_img = pygame.transform.scale(platform_img, (100, 30))

class Player_test(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.jump = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = self.vel_y

        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5

        # --- Horizontal collision ---
        self.rect.x += dx
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if dx > 0:  # Moving right
                self.rect.right = platform.rect.left
            elif dx < 0:  # Moving left
                self.rect.left = platform.rect.right

        # --- Vertical movement ---
        self.vel_y += 0.5  # gravity
        self.rect.y += self.vel_y

        # --- Vertical collision ---
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.vel_y > 0:  # Falling
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.jump = False
            elif self.vel_y < 0:  # Jumping up
                self.rect.top = platform.rect.bottom
                self.vel_y = 0

        if keys[pygame.K_SPACE] and not self.jump:
            self.vel_y = -10
            self.jump = True


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=None, height=None):
        super().__init__()
        self.image = platform_img.copy()
        if width is None:
            width = self.image.get_width()
        if height is None:
            height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

# 5. Define and add platforms here — THIS IS WHERE YOUR CODE GOES
platforms = pygame.sprite.Group()

# Ground platform
ground = Platform(0, 0, width)
ground.rect.bottom = height
platforms.add(ground)

# Vertical platform from y=150 to ground
column_x = 0
column_y = 150
column_height = height - column_y
column = Platform(column_x, column_y, 50, column_height)
platforms.add(column)

# Select a specific platform (e.g. the vertical column or the ground)
# For example, let's spawn the player on top of the ground:
ground = Platform(0, 0, width)
ground.rect.bottom = height
platforms.add(ground)

# Create player and place it on top of the ground
player_test = Player_test(0, 0)
player_test.rect.midbottom = column.rect.midtop

player_group = pygame.sprite.Group(player_test)

running = True
while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    player_test.update(platforms)


    player_group.draw(screen)
    platforms.draw(screen)

    pygame.display.flip()
    clock.tick(60)








