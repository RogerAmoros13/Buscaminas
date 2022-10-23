import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from simple_term_menu import TerminalMenu as tm
from cell import Cell 
import random
import time
from settings import *

size = (600, 600)

def get_adjacent_bombs(arr, i, j):
    n = len(arr) - 1
    m = len(arr[0]) - 1
    bombs_qty = 0
    for dx in range(-1 if (i > 0) else 0, 2 if (i < n) else 1):
        for dy in range(-1 if (j > 0) else 0, 2 if (j < m) else 1):
            if (dx != 0 or dy != 0) and arr[i + dx][j + dy].bomb:
                bombs_qty += 1
    return bombs_qty

class BuscaMinas:
    def __init__(self, rows, cols, bombs):
        pygame.init()

        self.cols = cols
        self.rows = rows
        self.size = 25
        self.screen = pygame.display.set_mode((self.cols * self.size, self.rows * self.size))
        self.clock = pygame.time.Clock()

        self.win = False
        self.lost = False
        self.mine_qty = bombs
        self.table = []

        bombs_pos = set()
        while len(bombs_pos) < self.mine_qty:
            x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1) 
            bombs_pos.add((x, y))

        for i in range(self.cols):
            row = []
            for j in range(self.rows):
                row.append(Cell((i, j), self.size, (i, j) in bombs_pos))
            self.table.append(row)
        for i in range(self.cols):
            for j in range(self.rows):
                if self.table[i][j].bomb:
                    continue
                self.table[i][j].adjacent_bombs = get_adjacent_bombs(self.table, i, j)
                self.table[i][j].get_color()

    def run(self):
        running = True
        end_game = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            self.screen.fill(GREY)
            self.make_play()
            remaining = 0
            for i in range(self.cols):
                for j in range(self.rows):
                    if self.table[i][j].invisible:
                        remaining += 1
                    if self.win and self.table[i][j].bomb:
                        self.disabled = True
                    if self.lost or self.win:
                        self.table[i][j].invisible = False
                        end_game = True

                    self.table[i][j].draw()
            if remaining == self.mine_qty:
                self.win = True
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(30)
            if end_game:
                time.sleep(2)
                running = False
    
    def make_play(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            pos = pygame.mouse.get_pos()
            x = (pos[0] // self.size)
            y = (pos[1] // self.size)
            if mouse_buttons[0] and not self.table[x][y].flaged:
                if self.table[x][y].bomb:
                    self.lost = True
                else:
                    self.table[x][y].invisible = False
                    if not self.table[x][y].adjacent_bombs:
                        self.open_adjacent_cells(x, y)
            if mouse_buttons[2] and self.table[x][y].invisible:
                self.table[x][y].flaged = not self.table[x][y].flaged
                time.sleep(.1)

                

    def open_adjacent_cells(self, i, j):
        n = self.cols - 1
        m = self.rows - 1
        for dx in range(-1 if (i > 0) else 0, 2 if (i < n) else 1):
            for dy in range(-1 if (j > 0) else 0, 2 if (j < m) else 1):
                if (dx != 0 or dy != 0) and self.table[i + dx][j + dy].invisible:
                    self.table[i + dx][j + dy].invisible = False
                    if not self.table[i + dx][j + dy].adjacent_bombs: 
                        self.open_adjacent_cells(i + dx, j + dy)
                        
            

    def draw_grid(self):
        for i in range(self.cols):
            pygame.draw.line(self.screen, BLACK, (i * self.size, 0), (i * self.size, self.size * self.rows))
        for i in range(self.rows):
            pygame.draw.line(self.screen, BLACK, (0, i * self.size), (self.size * self.cols, i * self.size))



if __name__ == "__main__":
    playing = True
    while playing:
        rows = int(input("# of rows: "))
        cols = int(input("# of cols: "))
        print("Select difficulty:")
        level = tm(["Fácil", "Normal", "Difícil", "Extremo"]).show()
        if level == 0:
            bombs = int(0.1 * rows * cols)
            
        elif level == 2:
            bombs = int(0.3 * rows * cols)
        elif level == 3:
            bombs = int(0.4 * rows * cols)
        else:
            bombs = int(0.2 * rows * cols)
        game = BuscaMinas(rows, cols, bombs)
        game.run()
        pygame.quit()
        print("Jugar otra vez?")
        again = tm(["Si", "No"]).show()
        if again:
            playing = False

