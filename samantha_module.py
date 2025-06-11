import pygame
import sys
import random
import time


class Clouds:
    def __init__(self, screen, x, image_filename):
        self.screen = screen
        self.x = x
        self.image =pygame.image.load(image_filename)
    def move(self):
        self.x += -0.3
        if self.x < -self.image.get_width():
            self.x = 0

    def draw(self, screen, camera_x, camera_y):
        for k in range(3):
            screen.blit(self.image, (self.x - camera_x + self.image.get_width() * k, camera_y))
            # screen.blit(self.image, (self.x - camera_x + self.image.get_width() * k, camera_y + self.image.get_height()))
def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("samantha_module")
    cloud = Clouds(screen, 0, "Clouds.png")
    clock = pygame.time.Clock()

    background_image = pygame.image.load("Sky.png")
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))



    while True:
        clock.tick(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        #screen.fill(pygame.Color ("light blue"))
        screen.blit(background_image, (0,0))
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            cloud.x -= 10
        if pressed_keys[pygame.K_RIGHT]:
            cloud.x += 10

        cloud.draw(screen, 400, 200)
        pygame.display.update()


if __name__ == "__main__":
    main()
    print("samantha_module")
