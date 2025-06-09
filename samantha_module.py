import pygame.transform
from pygame.examples.scrap_clipboard import screen
from pygame.examples.sprite_texture import running

BG = pygame.transform.scale(BG, (200, 200))

x = 1000
y = 740

while running:
    for event in pygame.event.get():
        if event.type == pygame QUIT:
            running = False
    screen.fill((0,0,0))
    screen.blit(BG, x, y))
    pygame.display.update()
pygame.quit()
    print("End -->")