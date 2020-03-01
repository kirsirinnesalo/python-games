import numpy as np, math, pygame, sys


BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)

ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
WIDTH = COLUMNS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)

screen = None


def create_board():
    board = np.zeros((ROWS,COLUMNS))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # Check positively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def draw_board(board):
    global screen 
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()



def main():
    global screen

    board = create_board()
    game_over = False
    turn = 0

    gameoverfont = pygame.font.SysFont("monospace", 64)
    size = (WIDTH, HEIGHT)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Connect 4 by kirsirinnesalo')
    draw_board(board)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))

                # Player 1 turn
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = gameoverfont.render("Pelaaja 1 voitti!", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True
                
                # Player 2 turn
                elif turn == 1:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = gameoverfont.render("Pelaaja 2 voitti!", 1, YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True
                        else:
                            # Check if board is full -> TIE
                            tie = True
                            for c in range(COLUMNS):
                                if board[ROWS-1][c] == 0:
                                    tie = False
                            if tie:
                                label = gameoverfont.render("Tasapeli", 1, BLUE)
                                screen.blit(label, (200,10))
                                game_over = True

                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(5000)


    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    pygame.init()
    main()

