import pygame
import sys
import character
import parkourmaptiling as tilemap
import camera
import coin
from enemy import Enemy
from parkourmaptiling import pipebottom_rects


def game_over(screen, resolution):
    font = pygame.font.SysFont("segoeuiemoji", 80)
    text = font.render("🐒", True, (255, 0, 0))
    text_rect = text.get_rect(center=(resolution[0] // 2, resolution[1] // 2))

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(500)
    pygame.event.clear()  # Clear input events# Wait 3 seconds
def start_screen(screen):
    pygame.font.init()
    font_title = pygame.font.SysFont("segoeuiemoji", 80)
    font_msg = pygame.font.SysFont("segoeuiemoji", 40)

    title_text = font_title.render("🐵 Super Monkey Jump!", True, (0, 0, 0))
    msg_text = font_msg.render("Press any key to start...", True, (0, 0, 0))

    screen.fill((146, 244, 255))
    screen.blit(title_text, title_text.get_rect(center=(screen.get_width() // 2, 200)))
    screen.blit(msg_text, msg_text.get_rect(center=(screen.get_width() // 2, 400)))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def main():
    last_death = 0
    left_pressed = False
    right_pressed = False
    pygame.init()
    resolution = (1000, 600)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("work pls")
    start_screen(screen)
    enemy_smash_jump = -500000
    death_cooldown = 0
    time = 0
    while True:  # Restart loop
        fps = pygame.time.Clock()
        player = character.Player(screen, 50, 5500)
        player_speed = 5

        tilemap.rendermap()
        tilerects = tilemap.tile_rects
        smash_counter = 0
        enemy_list = [
            Enemy(650, 5350,2),
            Enemy(1615, 5500,2),
            Enemy(1615, 5900, 1),
            Enemy(1850, 5800, 1),
            Enemy(1850, 5350,2),
            Enemy(1400, 6000, 0),
            Enemy(1500, 6000, 0),
            Enemy(1600, 6000, 0),
            Enemy(1700, 6000, 0),
            Enemy(1800, 6000, 0),
            Enemy(1900, 6000, 0),
            Enemy(2000, 6000, 0),
            Enemy(2100, 6000, 0),
            Enemy(2200, 6000, 0),
            Enemy(2300, 6000, 0)


        ]
        enemies = pygame.sprite.Group(*enemy_list)
        running = True
        score = 0
        font = pygame.font.SysFont("segoeuiemoji", 28)
        coin_list = [
                     coin.Coin(650, 5950),
                     coin.Coin(650, 6100),
                     coin.Coin(1590, 6050),
                     coin.Coin(1840, 5600),
                     coin.Coin(1590, 5700),
                     coin.Coin(1840, 5900),
                     coin.Coin(2010, 5600),
                     coin.Coin(2410, 5600),
                     coin.Coin(2610, 5750),
                     coin.Coin(2710, 5800),
                     coin.Coin(2710, 5550),
                     coin.Coin(3060, 5450),
                     coin.Coin(3360, 5350),
                     coin.Coin(3660, 5250)
                     ]
        coins = pygame.sprite.Group(*coin_list)
        if left_pressed:
            player.velocity_x = -5
        elif right_pressed:
            player.velocity_x = 5
        k = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if not right_pressed == True:
                         player.velocity_x += player_speed
                        right_pressed = True
                    if event.key == pygame.K_LEFT:
                        if not left_pressed == True:
                            player.velocity_x += -player_speed
                        left_pressed = True
                    if event.key == pygame.K_UP:
                        player.jump_time = pygame.time.get_ticks()
                        player.jump()
                    if event.key == pygame.K_SPACE:
                        print(player.x, player.y)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        if right_pressed:
                            player.velocity_x -= player_speed
                        right_pressed = False
                    if event.key == pygame.K_LEFT:
                        if left_pressed:
                         player.velocity_x += player_speed
                        left_pressed = False
                    if event.key == pygame.K_UP and not player.on_ground:
                        player.jump_timer = 16
            if k < 5:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT}))
                pygame.event.post(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_RIGHT}))
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT}))
                pygame.event.post(pygame.event.Event(pygame.KEYUP, {"key": pygame.K_LEFT}))
                k += 1
            screen.fill((146, 244, 255))
            camera_x, camera_y = camera.scroll_camera(player.hitbox, resolution[0], resolution[1], 7000, 7000)
            screen.blit(tilemap.map_display, (-camera_x, -camera_y))
            tilerects = tilemap.tile_rects
            lavarects = tilemap.lava_rects
            player.move(tilerects,lavarects,tilemap.pipebottom_rects)
            player.draw(camera_x, camera_y)
            if player.on_ground:
                smash_counter = 0

            if enemy_smash_jump > pygame.time.get_ticks() - 800:
                player_invincible = True
            else:
                player_invincible = False
            if enemy_smash_jump < pygame.time.get_ticks() - 1:
                player.enemy_bounce = False
            for enemy in enemies:
                enemy.update(tilerects,enemies)
                screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y - camera_y))
            if player.y > 9000 or player.touching_lava:
                game_over(screen, resolution)
                running = False
                last_death = pygame.time.get_ticks()
            for enemy in enemies:
                if player.hitbox.colliderect(enemy.rect):
                    if player.velocity_y > 0 and enemy.flattened == False:
                        smash_counter += 1
                        enemy.image = pygame.transform.scale(enemy.image.convert_alpha(),(60, 7))
                        enemy.flattened = True
                        enemy_smash_jump = pygame.time.get_ticks()
                        player.enemy_bounce = True
                        player.jump()
                        score += 100*smash_counter

                    if player.velocity_y <= 0 and enemy.flattened == False and player_invincible == False and death_cooldown <= 0:
                        if score<500:
                            game_over(screen, resolution)
                            last_death = pygame.time.get_ticks()
                            running = False
                        else:
                            score-=500
                            death_cooldown = 180
                            player_invincible = True
                            player.is_invincible = True
            live_count = "❤" * (score//500 + 1)
            time = pygame.time.get_ticks() - last_death
            time_raw = time / 1000
            time = round(time_raw,1)
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            heart_text = font.render(f"Lives:{live_count}", True, (0, 0, 0))
            time_text = font.render(f"{time}", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))
            screen.blit(heart_text, (20,50))
            screen.blit(time_text, (20, 80))

            screen.blit(time_text, (20, 70))
            for c in coins:
                c.draw(screen, camera_x, camera_y)
            for c in coins.copy():
                if player.hitbox.colliderect(c.rect):
                    score += 50
                    coins.remove(c)
            fps.tick(90)
            screen.blit(score_text, (20, 20))
            screen.blit(heart_text, (20,50))
            screen.blit(time_text, (20, 80))
            pygame.display.update()
            death_cooldown -= 1
            if death_cooldown <= 0:
                player.is_invincible = False
main()