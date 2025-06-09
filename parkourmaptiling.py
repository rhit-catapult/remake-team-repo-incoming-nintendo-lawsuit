import pygame
tile_rects = []
tilesize = 50
grass_image_raw = pygame.image.load("Dirt_Grass_Block2.png")
dirt_image_raw = pygame.image.load("Dirt_Block2.png")
air_image_raw = pygame.image.load("air_tile.png")
dirt_image = pygame.transform.scale(dirt_image_raw, (tilesize, tilesize))
grass_image = pygame.transform.scale(grass_image_raw, (tilesize, tilesize))
barrier_image = pygame.transform.scale(air_image_raw, (tilesize, tilesize))
map_display = pygame.Surface((7500,7500))
map_yoffset = 5000
game_map = [
[3] + [0]*139+ [3],
[3] + [0]*139+ [3],
[3] + [0]*139+ [3],
[3] + [0]*139+ [3],
[3] + [0]*139+ [3],
[3] + [0]*139+ [3],
[3] + [2]*2 + [0]*137+ [3],
[3] + [1]*2 + [0]*24 + [2]*9 + [0]*5 + [2]*10 + [0]*107 + [3],
[3] + [1]*2 + [0]*5 + [2]*10 + [0]*8 + [2] + [1]*9 + [0]*5 + [1]*10 +[0]*107 + [3],
[3] + [1]*2 + [0]*5 + [1]*10 + [0]*132 + [3],
[3] + [1]*2 + [0]*137 + [3],
[3] + [1]*2 + [2]*23  + [0]*25  + [2]*95 + [3],
[3] + [1]*25 + [0]*25 + [1]*95 + [3],
[3] + [1]*25 + [0]*23 + [2]*2 + [1]*95 + [3],
[3] + [1]*25 + [0]*23 + [1]*97 + [3],
[3] + [1]*25 + [2]*23 + [1]*97 + [3],
[3] + [1]*139 + [3],
[3] + [1]*139 + [3]
]
def rendermap():
    global tile_rects
    tile_rects = []
    map_display.fill((146, 244, 255))
    y = 0

    for row in game_map:
        x = 0
        for tile in row:
            if tile != 0:
                tile_rects.append(pygame.Rect(x*tilesize, y*tilesize+map_yoffset, tilesize, tilesize))
            if tile == 1:
                map_display.blit(dirt_image, (x*tilesize, y*tilesize+map_yoffset))
            elif tile == 2:
                map_display.blit(grass_image, (x*tilesize, y*tilesize+map_yoffset))
            elif tile == 3:
                map_display.blit(barrier_image, (x*tilesize, y*tilesize+map_yoffset)) # INVISIBLE WALL
            elif tile == 4:
                pass
            x += 1
        y += 1
    # for tile in tile_rects:  # tile hitboxes
    #     pygame.draw.rect(map_display, (0, 255, 0), tile, 1)