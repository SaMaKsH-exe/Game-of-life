import pygame as pg
import numpy as np
import time
import sys

pg.init()

# Define colors
COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE = (170, 170, 170)
COLOR_ALIVE = (255, 255, 255)
WHITE = (255, 255, 255)

# Define screen dimensions
WIDTH, HEIGHT = 800, 600

# Define button colors
BUTTON_COLOR = (0, 180, 0)
HOVER_COLOR = (0, 255, 0)

# Define font and button size
FONT = pg.font.Font(None, 36)
font_rules = pg.font.Font(None, 24)
BUTTON_SIZE = (250, 70)  # Increased button size

def menu():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    buttons = [
        {"label": "Play", "pos": (WIDTH/2, HEIGHT/2), "action": main},
        {"label": "Rules", "pos": (WIDTH/2, HEIGHT/2 + 80), "action": rules_page},  # Adjusted button positions
        {"label": "Quit", "pos": (WIDTH/2, HEIGHT/2 + 160), "action": sys.exit},   # Adjusted button positions
    ]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                check_button_click(event.pos, buttons)

        screen.fill((0, 0, 0))
        for button in buttons:
            draw_button(screen, button)

        pg.display.flip()

def draw_button(screen, button):
    mouse = pg.mouse.get_pos()
    label = FONT.render(button["label"], True, WHITE)
    label_rect = label.get_rect(center=button["pos"])
        
    if label_rect.collidepoint(mouse):
        pg.draw.rect(screen, HOVER_COLOR, label_rect.inflate(20, 20)) 
    else:
        pg.draw.rect(screen, BUTTON_COLOR, label_rect.inflate(20, 20))  

    screen.blit(label, label_rect)

def check_button_click(pos, buttons):
    for button in buttons:
        label = FONT.render(button["label"], True, WHITE)
        label_rect = label.get_rect(center=button["pos"])
        if label_rect.collidepoint(pos):
            button["action"]()

def rules_page():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))

    rules_text = [
        "Rules of Conway's Game of Life:",
        "",
        "1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.",
        "2. Any live cell with two or three live neighbors lives on to the next generation.",
        "3. Any live cell with more than three live neighbors dies, as if by overpopulation.",
        "4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.",
        "",
        "Hotkeys:",
        "Spacebar: Start/Pause simulation",
        "C: Clear the grid",
        "R: Randomize the grid",
        "Left Click: Place alive cell",
        "Right Click: Place dead cell",
        "Q: Close the program",
        "Esc: Return to the main menu",

        "Press any key or click to return to the main menu."
    ]

    y_offset = 100
    for line in rules_text:
        text_surface = font_rules.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 30

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN: 
                menu()

        pg.display.flip()

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

def main():
    pg.init()
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

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = not running
                
                if event.key == pg.K_c:
                    cells = np.zeros((60, 80))
                    update(screen, cells, 10)
                    pg.display.update()

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

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    cells = np.random.choice([0, 1], (60, 80), p=[0.7, 0.3])
                    update(screen, cells, 10)
                    pg.display.update()

                if event.key == pg.K_c:
                    cells = np.zeros((60, 80))
                    update(screen, cells, 10)
                    pg.display.update()
                    running = False
                
                if event.key == pg.K_q:
                    pg.quit()
                    return
                if event.key == pg.K_ESCAPE:
                    menu()

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pg.display.update()

        time.sleep(0.05)  # Adjust this value to control the speed of the simulation


if __name__ == '__main__':
    menu()
