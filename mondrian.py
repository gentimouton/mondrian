""" truchet tiling a la mondrian 
http://www.algorithmic-worlds.net/blog/blog.php?Post=20110201
Using pure pygame drawing, but could also use surfarray and numpy. 
"""
import pygame as pg
import random 


# TODO: mondrian: screen, area of screen to fill -> rects created
# so that: 
# rects = mondrian(screen,(0,0,res[0],res[1]))
# for r in rects
#     mondrian(screen,r) 

# TODO: use functional programming? Screen pixels is just an array of arrays

random.seed(0)

WHITE = 255, 255, 255
BLACK = 0, 0, 0
def random_color():
    return random.randint(22, 222), random.randint(22, 188), random.randint(22, 222)


# make i+j random floats in [0.1, 0.9]
junc = []
def make_junctures(i, j):
    for _ in range(2 * i + 1):
        col = [random.random() * 0.8 + 0.1 for _ in range(j + 1)]
        junc.append(col)
        
    
def make_tile(size, i, j, thickness=20):
    """ make a square tile. size in px. return surface. """
    surf = pg.Surface((size, size))
    surf.fill(random_color())
#     surf.fill(WHITE)
#     pg.draw.line(surf, (222, 222, 222), (0, 0), (size, 0)) # debug lines
#     pg.draw.line(surf, (222, 222, 222), (0, 0), (0, size))
    # draw lines with given junctions
    y1 = junc[2 * i][j]  # y of the segment coming from the left side   
    x2 = junc[2 * i + 1][j]  # x of the segment coming from the top side
    y3 = junc[2 * i + 2][j]  # y from right side
    x4 = junc[2 * i + 1][j + 1]  # x from bottom side
    start = 0, y1 * size  # segment from left side to mid
    end = max(x2, x4) * size, y1 * size
    pg.draw.line(surf, BLACK, start, end, size // thickness)
    start = x2 * size, 0  # segment from top side to mid
    end = x2 * size, max(y1, y3) * size
    pg.draw.line(surf, BLACK, start, end, size // thickness)
    start = size, y3 * size  # segment from right side to mid
    end = min(x2, x4) * size, y3 * size  
    pg.draw.line(surf, BLACK, start, end, size // thickness)
    start = x4 * size, size  # segment from bottom side to mid
    end = x4 * size, min(y1, y3) * size
    pg.draw.line(surf, BLACK, start, end, size // thickness)
    
    return surf
    

def main():
    res = 800, 600
    pg.init()
    screen = pg.display.set_mode(res)
    clock = pg.time.Clock()
    tile_size = 100
    make_junctures(res[0] // tile_size, res[1] // tile_size)
    for i in range(res[0] // tile_size):
        for j in range(res[1] // tile_size):
            tile = make_tile(tile_size, i, j)
            screen.blit(tile, (i * tile_size, j * tile_size))
    pg.display.flip()
    
    while 1:
        if pg.event.peek([pg.QUIT, pg.KEYDOWN]): break
        clock.tick(30)


if __name__ == '__main__': 
    main()
