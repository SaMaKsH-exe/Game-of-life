import pygame as pg
import numpy as np
import time
import sys
import asyncio
pg.init()


# Define colors
COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE = (170, 170, 170)
COLOR_ALIVE = (255, 255, 255)
WHITE = (255, 255, 255)





def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row in range(cells.shape[0]):
        for col in range(cells.shape[1]):
            alive = np.sum(cells[max(0, row-1):min(cells.shape[0], row+2),
                                  max(0, col-1):min(cells.shape[1], col+2)]) - cells[row, col]
            color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE

            if cells[row, col] == 1:
                if alive < 2 or alive > 3:
                    if with_progress:
                        color = COLOR_DIE
                elif 2 <= alive <= 3:
                    updated_cells[row, col] = 1
                    if with_progress:
                        color = COLOR_ALIVE
            else:
                if alive == 3:
                    updated_cells[row, col] = 1
                    if with_progress:
                        color = COLOR_ALIVE

            pg.draw.rect(screen, color, (col*size, row*size, size-1, size-1))

    return updated_cells

async def main():
    screen = pg.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pg.display.flip()
    pg.display.update()

    running = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = not running
                
                if event.key == pg.K_c:
                    cells = np.zeros((60, 80))
                    update(screen, cells, 10)
                    pg.display.update()
                    running = False


                if event.key == pg.K_r:
                    cells = np.random.choice([0, 1], (60, 80), p=[0.75, 0.25])
                    update(screen, cells, 10)
                    pg.display.update()
                    
                if event.key == pg.K_q:
                    pg.quit()
            
           
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                cells[pos[1]//10, pos[0]//10] = 1
                update(screen, cells, 10)
                pg.display.update()

            if pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()
                cells[pos[1]//10, pos[0]//10] = 0
                update(screen, cells, 10)
                pg.display.update()

        screen.fill(COLOR_GRID)
        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pg.display.update()

        time.sleep(0.04)

        asyncio.sleep(0)
asyncio.run(main())


