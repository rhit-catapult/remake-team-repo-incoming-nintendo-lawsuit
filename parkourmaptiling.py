import pygame
tile_rects = []
tilesize = 50
grass_image_raw = pygame.image.load("grass_tile.png")
dirt_image_raw = pygame.image.load("dirt_tile.png")
dirt_image = pygame.transform.scale(dirt_image_raw, (tilesize, tilesize))
grass_image = pygame.transform.scale(grass_image_raw, (tilesize, tilesize))
map_display = pygame.Surface((7500,7500))

game_map = [
[0]*150,
[0]*150,
[0]*150,
[0]*150,
[1]*150,
[1]*150,
[1]*150,
[1]*150,
[1]*150,
[1]*150,
[1]*150
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
                tile_rects.append(pygame.Rect(x*tilesize, y*tilesize+5000, tilesize, tilesize))
            if tile == 1:
                map_display.blit(dirt_image, (x*tilesize, y*tilesize+5000))
            elif tile == 2:
                map_display.blit(grass_image, (x*tilesize, y*tilesize+5000))
            x += 1
        y += 1
    # for tile in tile_rects:  # tile hitboxes
    #     pygame.draw.rect(map_display, (0, 255, 0), tile, 1)