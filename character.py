import pygame
import sys

class Player:
    def __init__(self, screen,x,y):
        self.imagetemp = pygame.image.load("SCH_Module.png")
        self.imagewidth = self.imagetemp.get_rect().width
        self.imageheight = self.imagetemp.get_rect().height
        self.image = pygame.transform.scale(self.imagetemp, (self.imagewidth / 7.5, self.imageheight / 7.5))
        self.rect = self.image.get_rect()
        self.screen = screen
        self.x = x
        self.y = y
        self.gravity = .002
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = True
        self.hitbox = (self.x,self.y,self.x+46,self.y+50)
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
       # pygame.draw.rect(self.screen, (0,0,255), (self.x, self.y, 30, 50))
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

def test():
    pygame.init()
    resolution = (1000,600)
    screen = pygame.display.set_mode(resolution)
    fps = pygame.time.Clock()
    fps.tick(60)
    player = Player(screen,500,300)
    player_speed = .5
    player_jump_power = .5
    jump_timer = 0
    jump_debounce = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.velocity_x += player_speed
                if event.key == pygame.K_LEFT:
                    player.velocity_x += -player_speed
                if event.key == pygame.K_UP and player.on_ground:
                    player.velocity_y = -player_jump_power
                    player.on_ground = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.velocity_x -= player_speed
                if event.key == pygame.K_LEFT:
                    player.velocity_x += player_speed

        screen.fill((255,255,255))
        if player.on_ground != True:
            if jump_debounce == False:
                jump_timer = 0
                jump_debounce = True
            else:
                jump_timer += 1
            if jump_timer > 45:
                player.velocity_y += player.gravity
                if player.velocity_y > 0.3:
                    player.velocity_y = 0.3
        player.draw(screen)
        player.move()
        pygame.display.update()
test()