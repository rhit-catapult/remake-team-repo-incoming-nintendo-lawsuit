import pygame
import sys
import time

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
        self.gravity = .25
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = True
        self.jump_time = 0
        self.hitbox = (self.x,self.y,self.x+46,self.y+50)
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
        #pygame.rect(self.hitbox)
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.hitbox = (self.x, self.y)
    def collision(self):
        if self.y + 50 > self.screen.get_height() - 50:
            self.y = self.screen.get_height() - 100
            self.velocity_y = 0
            self.on_ground = True
    def jump(self, jump_power):
        if self.on_ground:
            self.velocity_y += jump_power
            self.on_ground = False

def test():
    pygame.init()
    resolution = (1000,600)
    screen = pygame.display.set_mode(resolution)
    fps = pygame.time.Clock()

    player = Player(screen,500,300)
    player_speed = 5
    player_jump_power = 6
    jump_timer = 0
    jump_premature = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.velocity_x += player_speed
                if event.key == pygame.K_LEFT:
                    player.velocity_x += -player_speed
                if event.key == pygame.K_UP:
                    player.jump_time = pygame.time.get_ticks()
                    player.jump(-player_jump_power)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.velocity_x -= player_speed
                if event.key == pygame.K_LEFT:
                    player.velocity_x += player_speed

        screen.fill((255,255,255))
        if not player.on_ground:
            jump_timer += 1
            if jump_timer > 15:
                player.velocity_y += player.gravity
                if player.velocity_y > 5:
                    player.velocity_y = 5
        else:
            jump_timer = 0
        if player.jump_time + 200 > pygame.time.get_ticks() and player.on_ground:
            player.jump(-player_jump_power)
        print(jump_timer)
        pygame.draw.rect(screen, (1, 50, 32), (0, screen.get_height() - 50, screen.get_width(), 50))
        player.draw(screen)
        player.move()
        player.collision()
        pygame.display.update()
        fps.tick(120)
test()
