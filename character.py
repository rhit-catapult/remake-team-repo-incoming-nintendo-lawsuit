import pygame
import random
import time
import sys




class Character:
    def __init__(self, screen,x,y,x_velocity,y_velocity):
        self.screen = screen
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
    def move(self):
        print(pygame.math.Vector2(, ))
    def draw(self):
        pygame.draw.rect(self.screen, (100,100,100),(self.x,self.y,20,20))
def test_character():
    # TODO: change this function to test your class
    screen = pygame.display.set_mode((640, 480))
    character = Character(screen, 20, 20, 0, 0)
    fps = pygame.time.Clock()
    fps.tick(60)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_RIGHT:
                     pass
                if event.key == pygame.K_UP:
                 pass
                if event.key == pygame.K_DOWN:
                 pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass
        screen.fill("white")
        character.draw()
        character.move()
        pygame.display.update()
test_character()