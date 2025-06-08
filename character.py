import pygame
class Player:
    def __init__(self, screen,x,y):
        self.image_temporary = pygame.image.load("SCH_Modulescaled.png")
        self.image_width = self.image_temporary.get_rect().width
        self.image_height = self.image_temporary.get_rect().height
        self.image = pygame.transform.scale(self.image_temporary, (self.image_width / 7.02, self.image_height / 7.02))
        self.flipped_image = pygame.transform.flip(self.image, True, False)
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
        self.facing_left = False
        self.hit_list = []
        self.hitbox = pygame.Rect(self.x,self.y,31,50)
    def draw(self):
        # pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox, 2) # shows player hitbox
        if self.velocity_x < 0:
            self.screen.blit(self.flipped_image,(self.x,self.y))
            self.facing_left = True
        elif self.velocity_x > 0:
            self.screen.blit(self.image, (self.x, self.y))
            self.facing_left = False
        elif self.facing_left:
            self.screen.blit(self.flipped_image, (self.x, self.y))
        else:
            self.screen.blit(self.image, (self.x, self.y))

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
# CHATGPT VER
    def move(self, tiles):
        collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}

        # Move horizontally
        self.x += self.velocity_x
        self.hitbox.topleft = (self.x, self.y)
        self.hit_list = self.collision(tiles)
        for tile in self.hit_list:
            if self.velocity_x > 0:
                self.hitbox.right = tile.left
                self.x = self.hitbox.left  # Correct position
                collision_types['right'] = True
            elif self.velocity_x < 0:
                self.hitbox.left = tile.right
                self.x = self.hitbox.left
                collision_types['left'] = True

        # Move vertically
        self.y += self.velocity_y
        self.hitbox.topleft = (self.x, self.y)
        self.hit_list = self.collision(tiles)
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
        if not collision_types['bottom']:
            # Check if player is very close to the ground (within 2 pixels)
            self.hitbox.y += 2  # shift hitbox 2 pixels down temporarily
            close_to_ground = any(self.hitbox.colliderect(tile) for tile in tiles)
            self.hitbox.y -= 2  # restore position
            if close_to_ground:
                collision_types['bottom'] = True
                self.on_ground = True
            else:
                self.on_ground = False
        else:
            self.on_ground = True
        # Gravity and jump timer
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
    def collision(self, tiles):
        self.hit_list = []
        for tile in tiles: # runs
            if self.hitbox.colliderect(tile):
                self.hit_list.append(tile)
        return self.hit_list
    def jump(self):
        if self.on_ground:
            self.velocity_y = 0
            self.velocity_y += self.jump_power
            self.on_ground = False
