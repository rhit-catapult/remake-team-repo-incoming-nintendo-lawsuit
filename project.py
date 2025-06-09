import pygame
import sys
import character
import parkourmaptiling as tilemap
import camera
import random
import coin

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        r = random.randint(0,2)
        if r == 0:

            self.image = pygame.transform.scale(
                pygame.image.load("Gumba_Enemy.png").convert_alpha(),
                (40, 50)
            )
        elif r== 1:
            self.image = pygame.transform.scale(
                pygame.image.load("Glumbas_Enemy.png").convert_alpha(),
                (50, 50)
            )
        elif r==2:
            self.image = pygame.transform.scale(pygame.image.load("Eggumbo.png").convert_alpha(),
            (65,65))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_x = x
        self.vel_x = random.choice([-2, 2])

        self.vel_y = 0
        self.Ejump = False
        self.Ejump_timer = 0
        self.flattened = False
        self.platform_timer = 0
        self.max_platform_time = 180

    def update(self, platforms):
        # Horizontal movement & boundaries
        if not self.flattened:
            self.rect.x += self.vel_x
            for platform in platforms:
                if self.rect.colliderect(platform):
                    if self.vel_x > 0:  # Moving right, hit wall
                        self.rect.right = platform.left
                    elif self.vel_x < 0:  # Moving left, hit wall
                        self.rect.left = platform.right
                    self.vel_x *= -1  # Reverse direction
                    break  # Stop checking after first wall hit
            # Apply gravity velocity
            self.vel_y += 0.5

            # Vertical movement with collision stepwise resolution
            dy = self.vel_y
            step = 1 if dy > 0 else -1

            for _ in range(abs(int(dy))):
                self.rect.y += step
                for platform in platforms:
                    if self.rect.colliderect(platform):
                        if step > 0:  # Moving down, landed on platform
                            self.rect.bottom = platform.top
                            self.vel_y = 0
                            self.jump = False
                        elif step < 0:  # Moving up, hit ceiling
                            self.rect.top = platform.bottom
                            self.vel_y = 0
                        break  # No need to check other platforms this pixel move

            # After moving pixel by pixel vertically, check if on platform:
            on_platform = False
            standing_on_ground = False
            for platform in platforms:
                if self.rect.bottom == platform.top and self.rect.right > platform.left and self.rect.left < platform.right:
                    on_platform = True
                    if hasattr(platform, "is_ground") and platform.is_ground:
                        standing_on_ground = True

            # Jump timer and jump logic remain the same
            self.Ejump_timer -= 1
            if self.Ejump_timer <= 0 and not self.Ejump and on_platform:
                self.vel_y = -1
                self.Ejump = True
                self.Ejump_timer = random.randint(1, 3)

            if on_platform and not standing_on_ground and self.platform_timer > self.max_platform_time:
                self.vel_y = 5
                self.Ejump = True
        else:
            self.vel_y += 0.5
            dy = self.vel_y
            step = 1 if dy > 0 else -1

            for _ in range(abs(int(dy))):
                self.rect.y += step

                for platform in platforms:
                    if self.rect.colliderect(platform):
                        if step > 0: #a
                            self.rect.bottom = platform.top + self.image.get_height() - 7
                            self.vel_y = 0
                            self.jump = False
                        break

def game_over(screen, resolution):
    font = pygame.font.SysFont("segoeuiemoji", 80)
    text = font.render("🐒🐒🐒🐒🐒🐒", True, (255, 0, 0))
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
        player = character.Player(screen, 300, 5100)
        player_speed = 5

        tilemap.rendermap()
        tilerects = tilemap.tile_rects

        enemy_list = [Enemy(1315, 5500),Enemy(1415, 5500), Enemy(1615, 5500),Enemy(1815, 5500), Enemy(1915,5500),Enemy(2215, 5500)]
        enemies = pygame.sprite.Group(*enemy_list)
        running = True
        score = 0
        font = pygame.font.SysFont(None, 40)

        coin_list = [coin.Coin(800, 5200),
                     coin.Coin(650, 5500),
                     coin.Coin(500, 5200),
                     coin.Coin(1350, 5300),
                     coin.Coin(1750, 5300),
                     coin.Coin(2150, 5300),
                     coin.Coin(2500, 5300)
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
            lavatiles = tilemap.lava_rects
            player.move(tilerects)
            player.draw(camera_x, camera_y)
            if enemy_smash_jump > pygame.time.get_ticks() - 400:
                player_invincible = True
            else:
                player_invincible = False
            if enemy_smash_jump < pygame.time.get_ticks() - 1:
                player.enemy_bounce = False
            for enemy in enemies:
                enemy.update(tilerects)
                screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y - camera_y))

            if player.y > 6000:
                game_over(screen, resolution)
                running = False
                break
            for enemy in enemies:
                if player.hitbox.colliderect(enemy.rect):
                    if player.velocity_y > 0 and enemy.flattened == False:
                        enemy.image = pygame.transform.scale(pygame.image.load("Gumba_Enemy.png").convert_alpha(),(30, 7))
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
main()