import pygame
import sys
import character


def main():
    pygame.init()
    resolution = (960, 640)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("work pls")
    fps = pygame.time.Clock()
    player = character.Player(screen, 500, 300)
    player_speed = 5
    move_left = False
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

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (1, 50, 32), (0, screen.get_height() - 250, screen.get_width(), 250))
        player.draw()
        player.move()
        player.collision()
        pygame.display.update()
        fps.tick(120)
main()