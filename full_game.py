#THIS PROJECT IS NOT COMPLETED
#_______________________________





import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 4, 4
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
offense = False
defense = False
AI_row = 0
AI_column = 0
# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4x4 Tic Tac Toe")
screen.fill(WHITE)

# Board
board = [["" for _ in range(COLS)] for _ in range(ROWS)]

# Functions
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
    # Check rows
    for row in range(ROWS):
        if all(board[row][col] == "X" for col in range(COLS)) or all(board[row][col] == "O" for col in range(COLS)):
            draw_winning_line((0, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2))
            return board[row][0]

    # Check columns
    for col in range(COLS):
        if all(board[row][col] == "X" for row in range(ROWS)) or all(board[row][col] == "O" for row in range(ROWS)):
            draw_winning_line((col * SQUARE_SIZE + SQUARE_SIZE // 2, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT))
            return board[0][col]

    # Check main diagonal
    if all(board[i][i] == "X" for i in range(ROWS)) or all(board[i][i] == "O" for i in range(ROWS)):
        draw_winning_line((0, 0), (WIDTH, HEIGHT))
        return board[0][0]

    # Check anti-diagonal
    if all(board[i][ROWS - i - 1] == "X" for i in range(ROWS)) or all(board[i][ROWS - i - 1] == "O" for i in range(ROWS)):
        draw_winning_line((0, HEIGHT), (WIDTH, 0))
        return board[0][ROWS - 1]

    # Check for tie
    if all(board[row][col] != "" for row in range(ROWS) for col in range(COLS)):
        return "Tie"

    return None

def draw_winning_line(start, end):
    pygame.draw.line(screen, GREEN, start, end, LINE_WIDTH * 3)

def restart():
    global board, player, game_over
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]
    player = True
    game_over = False
    screen.fill(WHITE)
    draw_grid()

# Game variables
player = True
game_over = False
AI = False
# Draw initial grid
draw_grid()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if player == False and AI == True:
            while True:
                AI_row = random.randint(0, 3)
                AI_column = random.randint(0, 3)
                if board[AI_row][AI_column] == "":
                    board[AI_row][AI_column] = "O"
                    AI = False
                    player = True
                    break

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == True:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] == "":
                board[clicked_row][clicked_col] = "X"
                if player == True:
                    AI = True
                    player = False
                else:
                    player = True
                    AI = False
                winner = check_winner()
                if winner:
                    game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    draw_figures()
    pygame.display.update()
