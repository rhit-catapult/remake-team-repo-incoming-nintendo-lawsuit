import pygame
import sys

class Player:
    def __init__(self, screen,x,y):
        self.image_temporary = pygame.image.load("SCH_Module.png")
        self.image_width = self.image_temporary.get_rect().width
        self.image_height = self.image_temporary.get_rect().height
        self.image = pygame.transform.scale(self.image_temporary, (self.image_width / 7.5, self.image_height / 7.5))
        self.rect = self.image.get_rect()
        self.screen = screen
        self.x = x
        self.y = y
        self.jump_power = -6
        self.gravity = .35
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = True
        self.jump_time = 0
        self.jump_timer = 0
        self.hitbox = (self.x,self.y,self.x+46,self.y+50)
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.hitbox = (self.x, self.y)
        if not self.on_ground:
            self.jump_timer += 1
            if self.jump_timer > 15:
                self.velocity_y += self.gravity
                if self.velocity_y > 5:
                    self.velocity_y = 5
        else:
            self.jump_timer = 0
        if self.jump_time + 200 > pygame.time.get_ticks() and self.on_ground: # 200ms since last jump input
            self.jump() # jumps when landing
    def collision(self):
        if self.y + 50 > self.screen.get_height() - 250:
            self.y = self.screen.get_height() - 300
            self.velocity_y = 0
            self.on_ground = True
    def jump(self):
        if self.on_ground:
            self.velocity_y += self.jump_power
            self.on_ground = False
def test():
    pygame.init()
    resolution = (1000,600)
    screen = pygame.display.set_mode(resolution)
    fps = pygame.time.Clock()
    player = Player(screen,500,300)
    player_speed = 5
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
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.velocity_x -= player_speed
                if event.key == pygame.K_LEFT:
                    player.velocity_x += player_speed
                if event.key == pygame.K_UP and not player.on_ground:
                    player.jump_timer = 16

        screen.fill((255,255,255))
        pygame.draw.rect(screen, (1, 50, 32), (0, screen.get_height() - 250, screen.get_width(), 250))
        player.draw(screen)
        player.move()
        player.collision()
        pygame.display.update()
        fps.tick(120)
test()
