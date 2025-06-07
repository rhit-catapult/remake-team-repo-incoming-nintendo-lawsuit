import pygame
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)

# Player
player = pygame.Rect(100, 400, 50, 50)
velocity_y = 0
gravity = 0.8
jump_power = -15
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(150, 350, 150, 20),
    pygame.Rect(500, 300, 200, 20),
    pygame.Rect(0, 0, 20, 20),
]

def move_player():
    global velocity_y, on_ground

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = jump_power
        on_ground = False

    velocity_y += gravity
    player.y += velocity_y

    # Platform collision
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and velocity_y > 0:
            player.bottom = plat.top
            velocity_y = 0
            on_ground = True

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    move_player()

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    pygame.display.flip()
    clock.tick(60)
