import pygame
import sys
import random


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
        self.image = pygame.image.load("SCH_Modulescaled.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))  # Adjust size if needed
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
            self.vel_y = -12
            self.jump = True



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=None, height=None, is_ground=False):
        super().__init__()
        self.image = platform_img.copy()
        if width is None:
            width = self.image.get_width()
        if height is None:
            height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_ground = is_ground

# 5. Define and add platforms here — THIS IS WHERE YOUR CODE GOES
platforms = pygame.sprite.Group()

# Ground platform
ground = Platform(0, 0, width, 20, is_ground=True)
ground.rect.bottom = height
platforms.add(ground)

# Vertical platform from y=150 to ground
column_x = 0
column_y = 150
column_height = height - column_y
column = Platform(column_x, column_y, 50, column_height)
platforms.add(column)

# # Floating platform 1
# floating1 = Platform(300, 470, 100, 20)  # x=200, y=400, width=100, height=20
# platforms.add(floating1)
#
# # Floating platform 2
# floating2 = Platform(600, 470, 100, 20)
# platforms.add(floating2)
#
# # Floating platform 3
# floating3 = Platform(900, 470, 100, 20)
# platforms.add(floating3)
#
# # Floating platform 4
# floating4 = Platform(800, 350, 100, 20)
# platforms.add(floating4)
#
# # Floating platform 5
# floating5 = Platform(500, 300, 100, 20)
# platforms.add(floating5)
#
# # Floating platform 6
# floating6 = Platform(400, 200, 100, 20)
# platforms.add(floating6)
#
# # Floating platform 7
# floating7 = Platform(700, 150, 300, 20)
# platforms.add(floating7)

# Create player and place it on top of the ground
player_test = Player_test(0, 0)
player_test.rect.midbottom = column.rect.midtop

player_group = pygame.sprite.Group(player_test)

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
        self.jump_timer = random.randint(60, 180)  # frames until next jump

        # --- New attributes for staying-on-platform tracking ---
        self.platform_timer = 0               # How long on floating platform
        self.max_platform_time = 180          # Max allowed (in frames)

    def update(self, platforms):
        # Horizontal movement
        self.rect.x += self.speed
        if self.rect.x > self.start_x + self.distance:
            self.speed = -abs(self.speed)
        elif self.rect.x < self.start_x:
            self.speed = abs(self.speed)

        # Gravity
        self.vel_y += 0.5
        self.rect.y += self.vel_y

        on_platform = False
        standing_on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jump = False
                    on_platform = True

                    if platform.is_ground:
                        self.platform_timer = 0  # reset timer if on ground
                        standing_on_ground = True
                    else:
                        self.platform_timer += 1

        # Jump timer logic
        self.jump_timer -= 1
        if self.jump_timer <= 0 and not self.jump and on_platform:
            self.vel_y = -10
            self.jump = True
            self.jump_timer = random.randint(60, 180)

        # Drop-down if stuck on floating platform too long
        if on_platform and not standing_on_ground and self.platform_timer > self.max_platform_time:
            self.vel_y = 5  # force fall
            self.jump = True

# Ground platform

ground = Platform(0, 0, width, 20, is_ground=True)
ground.rect.bottom = height
platforms.add(ground)


# Add enemy on top of ground
enemy1 = Enemy(300, ground.rect.top - 40)  # 40 is the height of the enemy
enemy2 = Enemy(700, ground.rect.top - 40)  # 40 is the height of the enemy

enemies = pygame.sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)

def show_game_over():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Pause for 2 seconds


def run_game():
    global player_test, player_group, enemies, platforms

    # Recreate game objects
    platforms = pygame.sprite.Group()
    ground = Platform(0, 0, width, 20, is_ground=True)
    ground.rect.bottom = height
    platforms.add(ground)

    column = Platform(0, 150, 50, height - 150)
    platforms.add(column)

    floating_platforms = [
        (300, 470, 100, 20),
        (600, 470, 100, 20),
        (900, 470, 100, 20),
        (800, 350, 100, 20),
        (500, 300, 100, 20),
        (400, 200, 100, 20),
        (700, 150, 300, 20)  # <- fixed parenthesis
    ]

    for x, y, w, h in floating_platforms:
        platforms.add(Platform(x, y, w, h))

    player_test = Player_test(0, 0)
    player_test.rect.midbottom = column.rect.midtop
    player_group = pygame.sprite.Group(player_test)

    enemies = pygame.sprite.Group(
        Enemy(300, ground.rect.top - 40),
        Enemy(700, ground.rect.top - 40)
    )


    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        player_test.update(platforms)
        for enemy in enemies:
            enemy.update(platforms)

        # Collision detection
        if pygame.sprite.spritecollideany(player_test, enemies):
            show_game_over()
            return  # Exit and allow game to restart

        # Draw
        player_group.draw(screen)
        platforms.draw(screen)
        enemies.draw(screen)

        pygame.display.flip()
        clock.tick(60)

while True:
    run_game()
