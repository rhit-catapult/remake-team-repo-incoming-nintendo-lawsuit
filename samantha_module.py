import pygame
import sys
import time
import random

class Clouds:
    def __init__(self, screen, x, image_filename):
        self.screen = screen
        self.x = x
        self.image =pygame.image.load(image_filename)

    def draw(self):
        self.screen.blit(self.image, (self.x, 2725))



def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("samantha_module")
    cloud = Clouds(screen, 0, "Clouds.png")
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        cloud.x -= 10
    if pressed_keys[pygame.K_RIGHT]:
        cloud.x += 10

if __name__ == "__main__":
    main()