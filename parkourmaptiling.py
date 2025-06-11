import pygame

tile_rects = []
lava_rects = []
pipebottom_rects = []
tilesize = 50
grass_image_raw = pygame.image.load("Dirt_Grass_Block2.png")
dirt_image_raw = pygame.image.load("Dirt_Block2.png")
air_image_raw = pygame.image.load("air_tile.png")
lava1_image_raw = pygame.image.load("lava_2.png")
lava2_image_raw =pygame.image.load("lava_1.png")
pipetop_raw=pygame.image.load("Pipe_T.png")
pipemid_raw=pygame.image.load("Pipe_M.png")
pipebot_raw=pygame.image.load("Pipe_B.png")
dirt_image = pygame.transform.scale(dirt_image_raw, (tilesize, tilesize))
grass_image = pygame.transform.scale(grass_image_raw, (tilesize, tilesize))
barrier_image = pygame.transform.scale(air_image_raw, (tilesize, tilesize))
lava1_image = pygame.transform.scale(lava1_image_raw, (tilesize, tilesize))
lava2_image = pygame.transform.scale(lava2_image_raw, (tilesize, tilesize))
pipetop_image = pygame.transform.scale(pipetop_raw, (tilesize, tilesize))
pipemiddle_image = pygame.transform.scale(pipemid_raw, (tilesize, tilesize))
pipebottom_image = pygame.transform.scale(pipebot_raw, (tilesize, tilesize))
map_display = pygame.Surface((7500,7500))
map_yoffset = 4490
game_map = [
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*139 + [3],
[3] + [0]*78 + [2]*11 + [0]*45 + [3],
[3] + [0]*78 + [1]*11 + [0]*45 + [3],
[3] + [0]*89 + [1] + [0]*49 + [3],
[3] + [0]*139 + [3],
[3] + [0]*78 + [2]*3 + [0]*2 + [2] + [0]*2 + [2] + [0]*54 + [3],
[3] + [0]*72 + [3] + [0]*72+ [3],
[3] + [0]*139 + [3],
[3] + [0]*66 + [3] + [0]*78+ [3],
[3] + [0]*139 + [3],
[3] + [0]*60 + [3] + [0]*84+ [3],
[3] + [0]*139 + [3],
[3] + [0]*52 + [2]*3 + [0]*84+ [3],
[3] + [0]*35 + [2]*2 + [0]*2 + [2] + [0]*7 + [2] + [0]*6 + [1] + [0]*84 + [3],
[3] + [0]*54 + [0] + [0]*84+ [3],
[3] + [0]*54 + [0] + [0]*84+ [3],
[3] + [0]*30 + [2]*2 + [0]*18 + [2]*3 + [0] + [0] + [0]*86+ [3],
[3] + [0]*139+ [3],
[3] + [2]*2 + [0]*137 + [3],
[3] + [1]*2 + [0]*33 + [2]*2 + [0]*101 + [3],
[3] + [1]*2 + [0]*5 + [2]*10 + [0]*122 + [3],
[3] + [1]*2 + [0]*5 + [1]*10 + [0]*122 + [3],
[3] + [1]*2 + [0]*28 + [2]*2 + [0]*118 + [6]+[0]*24+[3],
[3] + [1]*2 + [2]*23  + [0]*25  + [2]*70 +[6]+[2]*23+ [3],
[3] + [1]*25 + [2] + [0]*24 + [1]*70 + [6] +[1]*23+ [3],
[3] + [1]*25 + [0]*23 + [2]*2 + [1]*70+[6] +[1]*23+ [3],
[3] + [1]*25 + [0]*23 + [1]*72+[6]+[1]*24 + [3],
[3] + [1]*25 + [2]*23 + [1]*72+[6]+[1]*24 + [3],
[3] + [1]*120+[6]+[1]*20 + [3],
[3] + [1]*120+[6]+[1]*20+ [3]
]


def rendermap():
    global tile_rects, lava_rects, pipebottom_rects
    tile_rects = []
    lava_rects = []
    pipebottom_rects = []
    map_display.fill((126, 224, 235))
    y = 0

    for row in game_map:
        x = 0
        for tile in row:
            if tile == 4:
                rect = pygame.Rect(x * tilesize, y * tilesize + map_yoffset, tilesize, tilesize)
                lava_rects.append(rect)
            # elif tile == 8:
            #      rect = pygame.Rect(x * tilesize, y * tilesize + map_yoffset, tilesize, tilesize)
            #      pipebottom_rects.append(rect)
            elif tile == 5 or tile == 6 or tile == 7 or tile == 8:
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
            x += 1
        y += 1