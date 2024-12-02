import pygame
import sys
import random

pygame.init()

turn_number = 0
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH // COLS
LINE_WIDTH = 5
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5x5 Tic Tac Toe")
screen.fill(WHITE)

board = [["" for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    for row in range(1, ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 ((col + 1) * SQUARE_SIZE - SPACE, (row + 1) * SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED,
                                 (col * SQUARE_SIZE + SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                                 ((col + 1) * SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner():
    for row in range(ROWS):
        if all(board[row][col] == "X" for col in range(COLS)) or all(board[row][col] == "O" for col in range(COLS)):
            draw_winning_line((0, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2))
            return board[row][0]
    for col in range(COLS):
        if all(board[row][col] == "X" for row in range(ROWS)) or all(board[row][col] == "O" for row in range(ROWS)):
            draw_winning_line((col * SQUARE_SIZE + SQUARE_SIZE // 2, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT))
            return board[0][col]
    if all(board[i][i] == "X" for i in range(ROWS)) or all(board[i][i] == "O" for i in range(ROWS)):
        draw_winning_line((0, 0), (WIDTH, HEIGHT))
        return board[0][0]
    if all(board[i][ROWS - i - 1] == "X" for i in range(ROWS)) or all(board[i][ROWS - i - 1] == "O" for i in range(ROWS)):
        draw_winning_line((0, HEIGHT), (WIDTH, 0))
        return board[0][ROWS - 1]
    if all(board[row][col] != "" for row in range(ROWS) for col in range(COLS)):
        return "Tie"
    return None

def draw_winning_line(start, end):
    pygame.draw.line(screen, GREEN, start, end, LINE_WIDTH * 3)

def restart():
    global board, player, game_over, turn_number
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]
    player = True
    game_over = False
    turn_number = 0
    screen.fill(WHITE)
    draw_grid()

def ai_make_move():
    global AI, player, game_over, turn_number

    def can_form_chain(row, col, symbol):
        if board[row][col] != "":
            return False
        temp_board = [row[:] for row in board]
        temp_board[row][col] = symbol
        for r in range(ROWS):
            if all(temp_board[r][c] == symbol for c in range(COLS)):
                return True
        for c in range(COLS):
            if all(temp_board[r][c] == symbol for r in range(ROWS)):
                return True
        if all(temp_board[i][i] == symbol for i in range(ROWS)):
            return True
        if all(temp_board[i][ROWS - i - 1] == symbol for i in range(ROWS)):
            return True
        return False

    for row in range(ROWS):
        for col in range(COLS):
            if can_form_chain(row, col, "O"):
                board[row][col] = "O"
                turn_number += 1
                winner = check_winner()
                if winner:
                    game_over = True
                AI = False
                player = True
                return

    for row in range(ROWS):
        for col in range(COLS):
            if can_form_chain(row, col, "X"):
                board[row][col] = "O"
                turn_number += 1
                winner = check_winner()
                if winner:
                    game_over = True
                AI = False
                player = True
                return

    for _ in range(100):
        AI_row = random.randint(0, ROWS - 1)
        AI_column = random.randint(0, COLS - 1)
        if board[AI_row][AI_column] == "":
            board[AI_row][AI_column] = "O"
            turn_number += 1
            winner = check_winner()
            if winner:
                game_over = True
            AI = False
            player = True
            return

draw_grid()

player = True
game_over = False
AI = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not player and AI and not game_over:
            ai_make_move()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if board[clicked_row][clicked_col] == "":
                board[clicked_row][clicked_col] = "X"
                turn_number += 1
                AI = True
                player = False
                winner = check_winner()
                if winner:
                    game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
    draw_figures()
    pygame.display.update()




