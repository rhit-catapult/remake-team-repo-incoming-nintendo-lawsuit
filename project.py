import pygame
import sys
import character
import parkourmaptiling as tilemap
import camera
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance=100, speed=2):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_x = x
        self.distance = distance
        self.speed = speed

        self.vel_y = 0
        self.jump = False
        self.jump_timer = random.randint(60, 180)

        self.platform_timer = 0
        self.max_platform_time = 180

    def update(self, platforms):
        # Horizontal movement & boundaries
        self.rect.x += self.speed
        if self.rect.x > self.start_x + self.distance:
            self.speed = -abs(self.speed)
        elif self.rect.x < self.start_x:
            self.speed = abs(self.speed)

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
                        on_platform = True
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
        self.jump_timer -= 1
        if self.jump_timer <= 0 and not self.jump and on_platform:
            self.vel_y = -10
            self.jump = True
            self.jump_timer = random.randint(60, 180)

        if on_platform and not standing_on_ground and self.platform_timer > self.max_platform_time:
            self.vel_y = 5
            self.jump = True

def game_over(screen, resolution):
    font = pygame.font.SysFont(None, 80)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(resolution[0] // 2, resolution[1] // 2))

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.update()

    pygame.time.delay(3000)
    pygame.event.clear()  # Clear input events# Wait 3 seconds

def main():
    pygame.init()
    resolution = (1000, 600)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("work pls")

    while True:  # Restart loop
        fps = pygame.time.Clock()
        player = character.Player(screen, 50, 4700)
        player_speed = 5

        tilemap.rendermap()
        tilerects = tilemap.tile_rects

        enemy_list = [Enemy(300, 4700), Enemy(600, 4700)]
        enemies = pygame.sprite.Group(*enemy_list)

        running = True
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

            player.move(tilerects)
            player.draw(camera_x, camera_y)

            for enemy in enemies:
                enemy.update(tilerects)
                screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y - camera_y))

            # Check collision
            for enemy in enemies:
                if player.hitbox.colliderect(enemy.rect):
                    game_over(screen, resolution)
                    running = False  # Break inner loop to restart
                    break

            pygame.display.update()
            fps.tick(90)

main()