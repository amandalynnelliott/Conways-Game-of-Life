# PYGAME
# 
# Milestones
# 1. Build a data structure to store the board state
# ----- board[][] with height (rows) and width (columns)
# ----- cells = w*h
# ----- row = board[y]
# ----- individual cell = board[y][x]
# ----- loops
# ----- random number [0,1] inputed into each cell. 50% assigned to 0; 50% to 1
# 2. “Pretty-print” the board to the terminal
# ----- render function outputs a string (append '#' alive or ' ' dead for each cell) for each row
# 3. Given a starting board state, calculate the next one
# ----- Apply the RULES. Generate new_board.
# ----- When creating new_board[][], need to index old_board[][]
# ----- Can't index new_board[][] while creating it.
# 4. Run the game forever
# ----- Input of last board state -> Output next board state ~ LOOP
# ----- Render new_board
# ----- new_board then passed into original function, essentially becoming the "new" old_board

# Rules
# Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
# Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
# Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
# Any dead cell with exactly 3 live neighbors becomes alive, by reproduction

# Extensions
# Save interesting starting positions to files and add the ability to reload them into your Life
# Improve the User Interface
# Change the rules of Life

###

import os
import random
import sys
import pygame

pygame.init()

Alive = 1
Dead = 0

width = 100
height = 100
cell_size = 10
size = width * cell_size, height * cell_size

bg_color = 0, 0, 0
alive_color = 255, 255, 255

screen = pygame.display.set_mode(size)


def dead_state(w, h):
    board = []

    for _ in range(0, h):
        row = []

        for _ in range(0, w):
            row.append(0)

        board.append(row)

    return board


def random_state(w, h):
    board = dead_state(w, h)

    for y in range(0, h):

        for x in range(0, w):
            random_number = random.random()
            if random_number >= 0.5:
                board[y][x] = Dead
            else:
                board[y][x] = Alive
    return board


def render(board):
    screen.fill(bg_color)
    for y in range(0, height):
      
        for x in range(0, width):
            cell = board[y][x]
            cell_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if cell == Dead:
                pass
            elif cell == Alive:
                pygame.draw.rect(screen, alive_color, cell_rect)
    pygame.display.flip()


def next_board_state(old_board):
    new_board = dead_state(width, height)

    for y in range(0, height):

        for x in range(0, width):
            alive_neighbors = 0
            dead_neighbors = 0
            for ny in range(y-1, y+1+1):
                for nx in range(x-1, x+1+1):
                    if ny < 0 or ny >= height or nx < 0 or nx >= width:  # If python doesn't wrap
                        continue
                    if nx == x and ny == y:
                        continue
                    else:
                        if old_board[ny][nx] == Alive:
                            alive_neighbors += 1
                        elif old_board[ny][nx] == Dead:
                            dead_neighbors += 1
            if old_board[y][x] == Alive:
                if alive_neighbors == 0 or alive_neighbors == 1:
                    new_board[y][x] = Dead
                if alive_neighbors == 2 or alive_neighbors == 3:
                    new_board[y][x] = Alive
                if alive_neighbors > 3:
                    new_board[y][x] == Dead
            elif old_board[y][x] == Dead:
                if alive_neighbors == 3:
                    new_board[y][x] = Alive

    return new_board


board = random_state(width, height)
paused = False

while True:
    for event in pygame.event.get(): # Event Handler
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: 
            x = round(event.pos[0] / cell_size)
            y = round(event.pos[1] / cell_size)
            if board[y][x] == Alive:
                board[y][x] = Dead
            elif board[y][x] == Dead:
                board[y][x] = Alive
        if event.type == pygame.KEYDOWN:
            if event.key == 112:
                paused = not paused

    render(board)
    
    if paused == False:
        board = next_board_state(board)

    