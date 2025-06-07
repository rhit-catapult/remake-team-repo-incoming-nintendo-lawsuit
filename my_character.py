import pygame
import sys


class Character:
    def __init__(self, screen: pygame.Surface, x, y, x_velocity, y_velocity):
        self.screen = screen
        self.x = x
        self.y = y
        self.y_velocity = y_velocity
        self.x_velocity = x_velocity
        self.falling = False
    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.y_velocity += 5
    def draw(self):
        pygame.draw.rect(self.screen, "blue", (self.x, self.y, 20, 20))
        pygame.draw.circle(self.screen, "red", (self.x + 5, self.y + 5), 3)
        pygame.draw.circle(self.screen, "red", (self.x + 15, self.y + 5), 3)



# This function is called when you run this file, and is used to test the Character class individually.
# When you create more files with different classes, copy the code below, then
# change it to properly test that class
def test_character():
    # TODO: change this function to test your class
    screen = pygame.display.set_mode((640, 480))
    character = Character(screen, 400, 400, 0,0)
    clock = pygame.time.Clock()
    clock.tick(60)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed_keys = pygame.key.get_pressed()

        screen.fill("white")
        character.draw()
        pygame.display.update()


# Testing the classes
# click the green arrow to the left or run "Current File" in PyCharm to test this class
if __name__ == "__main__":
    test_character()
