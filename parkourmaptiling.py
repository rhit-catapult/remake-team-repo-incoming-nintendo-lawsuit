import pygame
import csv

tile_rects = []
lava_rects = []
pipebottom_rects = []
brick_rects = []
tilesize = 50
grass_image_raw = pygame.image.load("Dirt_Grass_Block2.png")
dirt_image_raw = pygame.image.load("Dirt_Block2.png")
air_image_raw = pygame.image.load("air_tile.png")
lava1_image_raw = pygame.image.load("lava_2.png")
lava2_image_raw =pygame.image.load("lava_1.png")
pipetop_raw=pygame.image.load("Pipe_T.png")
pipemid_raw=pygame.image.load("Pipe_M.png")
pipebot_raw=pygame.image.load("Pipe_B.png")
brick_raw=pygame.image.load("bricks.png")
hog_raw = pygame.image.load("hog.png")
brick_background_raw = pygame.image.load("brick_Background.png")
dirt_image = pygame.transform.scale(dirt_image_raw, (tilesize, tilesize))
thegoldenhog_image = pygame.transform.scale(hog_raw, (tilesize,tilesize))
grass_image = pygame.transform.scale(grass_image_raw, (tilesize, tilesize))
barrier_image = pygame.transform.scale(air_image_raw, (tilesize, tilesize))
lava1_image = pygame.transform.scale(lava1_image_raw, (tilesize, tilesize))
lava2_image = pygame.transform.scale(lava2_image_raw, (tilesize, tilesize))
pipetop_image = pygame.transform.scale(pipetop_raw, (tilesize, tilesize))
pipemiddle_image = pygame.transform.scale(pipemid_raw, (tilesize, tilesize))
pipebottom_image = pygame.transform.scale(pipebot_raw, (tilesize, tilesize))
brick_image=pygame.transform.scale(brick_raw, (tilesize, tilesize))
brick_background_image = pygame.transform.scale(brick_background_raw, (tilesize, tilesize))
map_display = pygame.Surface((7500,7500))
map_yoffset = 4490
game_map = []
with open("map.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        game_map.append([int(value) for value in row])


def rendermap():
    global tile_rects, lava_rects, pipebottom_rects
    tile_rects = []
    lava_rects = []
    pipebottom_rects = []
    map_display.fill((126, 224, 235))
    map_display.set_colorkey((126,224,235))
    #map_display.blit(background_image, (0, 0))
    y = 0

    for row in game_map:
        x = 0
        for tile in row:
            if tile == 4:
                rect = pygame.Rect(x * tilesize, y * tilesize + map_yoffset, tilesize, tilesize)
                lava_rects.append(rect)
            elif tile == 11:
                 rect = pygame.Rect(x * tilesize, y * tilesize + map_yoffset, tilesize, tilesize)
                 pipebottom_rects.append(rect)
            elif tile == 5 or tile == 6 or tile == 7 or tile == 8 or tile == 10:
                pass
            elif tile != 0:
                rect = pygame.Rect(x * tilesize, y * tilesize + map_yoffset, tilesize, tilesize)
                tile_rects.append(rect)
            if tile == 1:
                map_display.blit(dirt_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile == 2:
                map_display.blit(grass_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile == 3:
                map_display.blit(barrier_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile == 4:
                map_display.blit(lava2_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile == 5:
                map_display.blit(lava1_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile==6:
                map_display.blit(pipetop_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile ==7:
                map_display.blit(pipemiddle_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile == 8:
                map_display.blit(pipebottom_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile==9:
                map_display.blit(brick_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile == 10:
                map_display.blit(brick_background_image, (x * tilesize, y * tilesize + map_yoffset))
            elif tile == 11:
                map_display.blit(thegoldenhog_image, (x * tilesize, y * tilesize + map_yoffset))
            x += 1
        y += 1