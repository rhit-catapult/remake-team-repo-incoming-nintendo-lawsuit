import pygame
import sys
import character
import parkourmaptiling as tilemap
import camera
import coin
from enemy import Enemy


def game_over(screen, resolution):
    font = pygame.font.SysFont("segoeuiemoji", 80)
    text = font.render("🐒", True, (255, 0, 0))
    text_rect = text.get_rect(center=(resolution[0] // 2, resolution[1] // 2))

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(500)
    pygame.event.clear()  # Clear input events# Wait 3 seconds

def main():
    pygame.init()
    resolution = (1000, 600)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("work pls")
    enemy_smash_jump = -500000
    while True:  # Restart loop
        fps = pygame.time.Clock()
        player = character.Player(screen, 300, 4500)
        player_speed = 5

        tilemap.rendermap()
        tilerects = tilemap.tile_rects

        enemy_list = [Enemy(1315, 5500),Enemy(1415, 5500), Enemy(1615, 5500),Enemy(1815, 5500), Enemy(1915,5500),Enemy(2215, 5500)]
        enemies = pygame.sprite.Group(*enemy_list)
        running = True
        score = 0
        font = pygame.font.SysFont(None, 40)

        coin_list = [
                     coin.Coin(650, 5350),
                     coin.Coin(650, 5510),
                     coin.Coin(0, 0)
                     ]
        coins = pygame.sprite.Group(*coin_list)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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
            camera_x, camera_y = camera.scroll_camera(player.hitbox, resolution[0], resolution[1], 7000, 7000)
            screen.blit(tilemap.map_display, (-camera_x, -camera_y))
            tilerects = tilemap.tile_rects
            lavarects = tilemap.lava_rects
            player.move(tilerects,lavarects)
            player.draw(camera_x, camera_y)
            if enemy_smash_jump > pygame.time.get_ticks() - 800:
                player_invincible = True
            else:
                player_invincible = False
            if enemy_smash_jump < pygame.time.get_ticks() - 1:
                player.enemy_bounce = False
            for enemy in enemies:
                enemy.update(tilerects,enemies)
                screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y - camera_y))
            if player.y > 6000 or player.touching_lava:
                game_over(screen, resolution)
                running = False
                break
            for enemy in enemies:
                if player.hitbox.colliderect(enemy.rect):
                    if player.velocity_y > 0 and enemy.flattened == False:
                        enemy.image = pygame.transform.scale(enemy.image.convert_alpha(),(60, 7))
                        enemy.flattened = True
                        enemy_smash_jump = pygame.time.get_ticks()
                        player.enemy_bounce = True
                        player.jump()
                        score += 100

                    if player.velocity_y <= 0 and enemy.flattened == False and player_invincible == False:
                        game_over(screen, resolution)
                        running = False
                        break

            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))
            for c in coins:
                c.draw(screen, camera_x, camera_y)

            for c in coins.copy():
                if player.hitbox.colliderect(c.rect):
                    score += 50
                    coins.remove(c)
            pygame.display.update()
            fps.tick(90)
            print(player.x,player.y)
main()