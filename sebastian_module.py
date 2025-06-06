import pygame
import sys
import random

class Character:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(self.screen, "blue", (self.x, self.y, 20, 20))
        pygame.draw.circle(self.screen, "red", (self.x + 5, self.y + 5), 3)
        pygame.draw.circle(self.screen, "red", (self.x + 15, self.y + 5), 3)
class Boss:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.radius = (50)
        self.x = random.randint(self.radius, self.screen.get_width() - self.radius)
        self.y = random.randint(self.radius, self.screen.get_height() - self.radius)
        self.speed_x = random.randint(1, 10)
        self.speed_y = random.randint(1, 10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def draw(self):
        pygame.draw.rect(self.screen, (self.color), (self.x, self.y), )



# This function is called when you run this file, and is used to test the Character class individually.
# When you create more files with different classes, copy the code below, then
# change it to properly test that class
def test_character():
    # TODO: change this function to test your class
    screen = pygame.display.set_mode((640, 480))
    character = Character(screen, 400, 400)
    boss = Boss(screen, 400, 400)
    clock = pygame.time.Clock()
    clock.tick(60)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            character.y -= 5
        if pressed_keys[pygame.K_DOWN]:
            character.y += 5
        if pressed_keys[pygame.K_RIGHT]:
            character.x += 5
        if pressed_keys[pygame.K_LEFT]:
            character.x -= 5

        screen.fill("white")
        character.draw()
        boss.draw()
        pygame.display.update()


# Testing the classes
# click the green arrow to the left or run "Current File" in PyCharm to test this class
if __name__ == "__main__":
    test_character()
