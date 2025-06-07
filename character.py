import pygame
import sys

class Player:
    def __init__(self, screen,x,y):
        self.screen = screen
        self.x = x
        self.y = y
        self.gravity = .02
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
    def draw(self):
        pygame.draw.rect(self.screen, (0,0,255), (self.x, self.y, 30, 50))
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y



def test():
    pygame.init()
    resolution = (1000,600)
    screen = pygame.display.set_mode(resolution)
    fps = pygame.time.Clock()
    fps.tick(60)
    player = Player(screen,10,10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((255,255,255))
        if player.on_ground != True:
            player.velocity_y += player.gravity
            if player.velocity_y > 0.3:
                player.velocity_y = 0.3
        player.draw()
        player.move()
        pygame.display.update()
test()