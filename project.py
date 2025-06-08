import pygame
import sys
import character
import tiletest as tilemap


def main():
    pygame.init()
    resolution = (1000, 600)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("work pls")
    fps = pygame.time.Clock()
    player = character.Player(screen, 10, 10)
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

        screen.fill((146, 244, 255))
        tilemap.rendermap()
        tilemap_screen = tilemap.map_display
       # tilemap_screen = pygame.transform.scale(tilemap.map_display, (2000,1200))
        tilerects = tilemap.tile_rects
        screen.blit(tilemap_screen, (0, 0))
        player.draw()
        player.move(tilerects)
        pygame.display.update()
        fps.tick(120)
main()