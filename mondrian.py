""" truchet tiling a la mandrian 
http://www.algorithmic-worlds.net/blog/blog.php?Post=20110201
Using pure pygame drawing, but could also use surfarray and numpy. 
"""
import datetime
import random 
import time

import pygame as pg


SEED = 'mondrian_seed'
RESOLUTION = 400, 300
TILE_SIZE = 25
TILE_THICKNESS = 2

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 222, 222, 222
BLUE = 0, 0, 222
RED = 222, 0, 0
YELLOW = 222, 222, 0
   
def random_color():
    return random.randint(22, 222), random.randint(22, 188), random.randint(22, 222)


def make_junctures(i, j):
    junc = [[random.random() * 0.9 + 0.05 for _ in range(j + 1)] for _ in range(2 * i + 1)]
    return junc
    
    
def make_tile(size, i, j, junc, thickness=4):
    """ make a square tile. size in px. return surface and central rect. """
    if thickness % 2 == 1:  # we're going to divide this by 2 throughout
        thickness += 1
    surf = pg.Surface((size, size))
    surf.fill(WHITE)
#     pg.draw.line(surf, GRAY, (0, 0), (size, 0))  # debug lines
#     pg.draw.line(surf, GRAY, (0, 0), (0, size))
    # draw lines with given junctions
    y1 = round(junc[2 * i][j] * size)  # y of the segment coming from the left side   
    x2 = round(junc[2 * i + 1][j] * size)  # x of the segment coming from the top side
    y3 = round(junc[2 * i + 2][j] * size)  # y from right side
    x4 = round(junc[2 * i + 1][j + 1] * size)  # x from bottom side
    # segment from left side to mid
    x, y = 0, y1 - thickness // 2  
    w, h = max(x2, x4) + thickness // 2, thickness
    pg.draw.rect(surf, BLACK, (x, y, w, h))
    # segment from top side to mid
    x, y = x2 - thickness // 2, 0  # segment from top side to mid
    w, h = thickness, max(y1, y3) + thickness // 2
    pg.draw.rect(surf, BLACK, (x, y, w, h))
    # segment from right side to mid
    x, y = min(x2, x4) - thickness // 2, y3 - thickness // 2
    w, h = size - min(x2, x4) + thickness // 2, thickness
    pg.draw.rect(surf, BLACK, (x, y, w, h))
    # segment from bottom side to mid
    x, y = x4 - thickness // 2, min(y1, y3) - thickness // 2   
    w, h = thickness, size - min(y1, y3) + thickness // 2 
    pg.draw.rect(surf, BLACK, (x, y, w, h))
    
    rect = (min(x2, x4) + thickness // 2,
            min(y1, y3) + thickness // 2,
            abs(x2 - x4) - thickness,
            abs(y1 - y3) - thickness 
            )
    
    surf.fill(random.choice([RED, BLUE, YELLOW, WHITE]), rect)
    return surf


def make_mondrian(surf, seed):
    random.seed(seed)
    res = surf.get_size()
    junc = make_junctures(res[0] // TILE_SIZE, res[1] // TILE_SIZE)
    for i in range(res[0] // TILE_SIZE):
        for j in range(res[1] // TILE_SIZE):
            tile = make_tile(TILE_SIZE, i, j, junc, TILE_THICKNESS)
            surf.blit(tile, (i * TILE_SIZE, j * TILE_SIZE))
    pg.display.flip()
    

def screenshot():
    # https://github.com/gentimouton/olympus/blob/master/src/pview.py
    fname_template = 'mondrian_screenshot_%Y%m%d%H%M%S.png'
    fname = datetime.datetime.now().strftime(fname_template)
    pg.image.save(pg.display.get_surface(), fname)
    
    
def main():
    pg.init()
    screen = pg.display.set_mode(RESOLUTION)
    make_mondrian(screen, SEED)
    
    done = False
    while not done:
        event = pg.event.wait()
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True
            elif event.key == pg.K_PRINT:
                screenshot()
            else:
                make_mondrian(screen, time.time())


if __name__ == '__main__': 
    main()
