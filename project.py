import pygame
import sys
import character
import parkourmaptiling as tilemap
import camera


def main():
    pygame.init()
    resolution = (1000, 600)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("work pls")
    fps = pygame.time.Clock()
    player = character.Player(screen, 50, 4700)
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
        #tilemap_screen = tilemap.map_display
       # tilemap_screen = pygame.transform.scale(tilemap.map_display, (2000,1200))
       # tilerects = tilemap.tile_rects
       # screen.blit(tilemap_screen, (0, 0)) # NONCAMERA
       # player.draw()
        #player.move(tilerects)
        camera_x, camera_y = camera.scroll_camera(player.hitbox, resolution[0], resolution[1], 7000, 7000)
        tilemap_screen = tilemap.map_display
        screen.blit(tilemap_screen, (-camera_x, -camera_y))  # <-- Use offset here!
        tilerects = tilemap.tile_rects
        player.move(tilerects)
        player.draw(camera_x, camera_y)
        pygame.display.update()
        fps.tick(90)
main()