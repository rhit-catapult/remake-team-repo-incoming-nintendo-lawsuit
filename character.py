import pygame
class Player:
    def __init__(self, screen,x,y):
        self.jump_image = self.scale_sprite_image("Nur_Jump.png")
        self.jump_left_image = pygame.transform.flip(self.jump_image, True, False)
        self.walk_right_images = [
            self.scale_sprite_image("Nur_Walking_1.png"),
            self.scale_sprite_image("Nur_Walking_2.png"),
            self.scale_sprite_image("Nur_Walking_1.png"),
            self.scale_sprite_image("Nur_Walking_3.png")
        ]
        self.idle_images = [
            self.scale_sprite_image("Idol_1.png"),
            self.scale_sprite_image("Idol_2.png"),
            self.scale_sprite_image("Idol_3.png"),
            self.scale_sprite_image("Idol_3.png"),
            self.scale_sprite_image("Idol_2.png")
        ]
        self.last_movement = 0
        self.idle_time = 0
        self.walk_left_images = [pygame.transform.flip(img, True, False) for img in self.walk_right_images]
        self.frame_index = 0
        self.idle_frame_index = 0
        self.idle_animation_timer = 0
        self.idle_animation_speed = .15
        self.animation_timer = 0
        self.animation_speed = .15
        self.rect = self.walk_right_images[0].get_rect()
        self.screen = screen
        self.is_invincible = False
        self.has_won = False
        self.x = x
        self.y = y
        self.jump_power = -7
        self.gravity = .35
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.jump_time = 0
        self.jump_timer = 0
        self.facing_left = False
        self.hit_list = []
        self.coyote_timer = 0
        self.coyote_enable = False
        self.enemy_bounce = False
        self.touching_lava = False
        self.hitbox = pygame.Rect(self.x,self.y,31,50)
        self.invincibletimer = 0
    def scale_sprite_image(self, image):
        temp_image = pygame.image.load(image)
        width = temp_image.get_rect().width
        height = temp_image.get_rect().height
        scaled_image = pygame.transform.scale(temp_image, (width / 7.02, height / 7.02))
        return scaled_image

    def draw(self, camera_x=0, camera_y=0):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        if self.velocity_x != 0 and self.on_ground:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.walk_right_images)
        else:
            self.frame_index = 0
        if not self.on_ground:
            if self.velocity_x > 0:
                image = self.jump_image
                self.facing_left = False
            if self.velocity_x < 0:
                image = self.jump_left_image
                self.facing_left = True
            if self.velocity_x == 0:
                image = self.jump_left_image if self.facing_left else self.jump_image
        elif self.velocity_x < 0:
            image = self.walk_left_images[self.frame_index]
            self.facing_left = True
        elif self.velocity_x > 0:
            image = self.walk_right_images[self.frame_index]
            self.facing_left = False
        else:
            image = self.walk_left_images[0] if self.facing_left else self.walk_right_images[0]
        if 925 > self.idle_time > 900 or  1000 > self.idle_time > 975:
            self.idle_animation_timer += self.idle_animation_speed
            if self.idle_animation_timer >= 1:
                self.idle_animation_timer = 0
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_images)
            image = self.idle_images[self.idle_frame_index]
        else:
            self.idle_frame_index = 0
        if self.is_invincible == True:
            if self.invincibletimer % 2 == 0:
                image = pygame.image.load("air_tile.png")
            self.invincibletimer += 1
        else:
            self.invincibletimer = 0
        self.screen.blit(image, (draw_x, draw_y))

    # def move(self,tiles):
    #     collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
    #     self.x += self.velocity_x
    #     self.y += self.velocity_y
    #     self.hitbox.topleft = (self.x, self.y)
    #     self.hit_list = self.collision(tiles)
    #     for tile in self.hit_list:
    #          if self.velocity_x > 0:
    #              self.hitbox.right = tile.left
    #              self.x = self.hitbox.right
    #              collision_types['right'] = True
    #          elif self.velocity_x < 0:
    #              self.hitbox.left = tile.right
    #              self.x = self.hitbox.left
    #              collision_types['left'] = True
    #     for tile in self.hit_list:
    #         if self.velocity_y > 0:
    #             self.hitbox.bottom = tile.top
    #             self.y = self.hitbox.top
    #             collision_types['bottom'] = True
    #             self.on_ground = True
    #         elif self.velocity_y < 0:
    #             self.hitbox.top = tile.bottom
    #             self.y = self.hitbox.top
    #             collision_types['top'] = True
    #     self.on_ground = collision_types['bottom']
    #     if not self.on_ground:
    #         self.jump_timer += 1
    #         if self.jump_timer > 15:
    #             self.velocity_y += self.gravity
    #             if self.velocity_y > 5:
    #                 self.velocity_y = 5
    #     else:
    #         self.jump_timer = 0
    #     if self.jump_time + 200 > pygame.time.get_ticks() and self.on_ground: # 200ms since last jump input
    #         self.jump() # jumps when landing
# CHATGPT VERSION (MUCH BETTER FUNCTIONALLY THAN MINE - 2 HOURS OF FAILURE)
    def move(self, tiles,lavatiles,pipetiles):
        collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        # if self.y > 5700:
        #     self.x = 50
        #     self.y = 4700
        if self.velocity_x == 0 and self.on_ground:
            self.last_movement += 1
            if self.last_movement >= 300:
                self.idle_time += 1
        else:
            self.last_movement = 0
            self.idle_time = 0
        self.x += self.velocity_x
        self.hitbox.topleft = (self.x, self.y)
        self.hit_list = self.collision(tiles)
        if len(self.hit_list) > 0:
            for tile in self.hit_list:
                if self.velocity_x > 0:
                    self.hitbox.right = tile.left
                    self.x = self.hitbox.left
                    collision_types['right'] = True
                elif self.velocity_x < 0:
                    self.hitbox.left = tile.right
                    self.x = self.hitbox.left
                    collision_types['left'] = True

        # Move vertically
        self.y += self.velocity_y
        self.hitbox.topleft = (self.x, self.y)
        self.hit_list = self.collision(tiles)
        if len(self.hit_list) > 0:
            for tile in self.hit_list:
                if self.velocity_y > 0:
                    self.hitbox.bottom = tile.top
                    self.y = self.hitbox.top
                    collision_types['bottom'] = True
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.hitbox.top = tile.bottom
                    self.y = self.hitbox.top
                    collision_types['top'] = True
                    self.velocity_y = 0
        self.on_ground = collision_types['bottom']

        # Additional ground check:
        sensor_height = 2
        sensor = pygame.Rect(self.hitbox.midbottom[0]-2.5, self.hitbox.bottom, 5, sensor_height)
        close_to_ground = any(sensor.colliderect(tile) for tile in tiles)
        # pygame.draw.rect(self.screen, (255, 0, 0),
        # pygame.Rect(self.hitbox.midbottom[0]-2.5, int(self.hitbox.bottom), 5,sensor_height)) # hitbox draw
        if collision_types['bottom'] or close_to_ground:
            self.on_ground = True
            self.coyote_timer = pygame.time.get_ticks()
        else:
            self.on_ground = False
            self.coyote_enable = pygame.time.get_ticks() - self.coyote_timer <= 200
        if not self.on_ground:
            self.jump_timer += 1
            if self.jump_timer > 15:
                self.velocity_y += self.gravity
                if self.velocity_y > 5:
                    self.velocity_y = 5
        else:
            self.jump_timer = 0

        # Jump when jump timer and on ground conditions met
        if self.jump_time + 200 > pygame.time.get_ticks() and self.on_ground:
            self.jump()
        self.hitbox.topleft = (self.x, self.y)
        self.collision(lavatiles)
        if len(self.hit_list) > 0:
            self.touching_lava = True
        else:
            self.touching_lava = False
        self.collision(pipetiles)
        if len(self.hit_list) > 0:
            self.has_won = True
    def collision(self, tiles):
        self.hit_list = []
        for tile in tiles: # runs
            if self.hitbox.colliderect(tile):
                self.hit_list.append(tile)
        return self.hit_list
    def jump(self):
        # if self.on_ground or self.coyote_enable or self.enemy_bounce:
            self.velocity_y = 0
            self.velocity_y += self.jump_power
            self.on_ground = False
    def enemy_collision(self, enemies):
        pass

