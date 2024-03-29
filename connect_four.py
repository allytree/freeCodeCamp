import numpy as np
import pygame
import sys
import math

BLUE = (67,12,118)
BLACK = (0,0,0)
RED = (0,231,255) # player 1 colour
YELLOW = (0,0,255)
FONT_COLOUR = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row_(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horisontalk locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range (ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

#Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

# Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range (ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

# Check for negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range (3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
                
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE/2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2), RADIUS)
 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE/2, height-(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE+SQUARESIZE/2, height-(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size =  (width, height)

RADIUS = (SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, SQUARESIZE/2), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, SQUARESIZE/2),RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            #Ask for player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row_(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label =myfont.render("Player 1 wins!!", 1, FONT_COLOUR)
                        screen.blit(label, (40,10))
                        # print("player 1 wins!!!! Congrats!!!")
                        game_over = True

            # #Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row_(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label =myfont.render("Player 2 wins!!", 2, FONT_COLOUR)
                        screen.blit(label, (40,10))
                        # print("player 2 wins!!!! Congrats!!!")
                        game_over = True
                        
            print_board(board)
            draw_board(board)
                
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)