"""
    client.py

    Handle Client-side
"""

import sys
import pygame
from src.classes import Network
pygame.font.init()

# Setup the main window
SIDE, MARGIN = 150, 0
WIDTH, HEIGHT = 3 * SIDE, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Setup Clock()
FPS = 60
CLOCK = pygame.time.Clock()

# Setup Font
FONT = pygame.font.SysFont("Secular One", 200)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 55)
BLACK = (10, 10, 10)

# Some useful comment
client = Network(server=False)


def draw_board():
    """Draw main board"""

    # COLUMNS
    x, y = 0, MARGIN
    for _ in range(4):
        pygame.draw.line(WIN, BLACK, (x, y),
                        (x, HEIGHT - (HEIGHT - WIDTH - MARGIN)), 9)
        x += SIDE

    # ROWS
    x, y = 0, MARGIN
    for _ in range(4):
        pygame.draw.line(WIN, BLACK, (x, y), (WIDTH, y), 9)
        y += SIDE


def update_board(board):
    """Place marks on the board"""
    MARK_O = FONT.render(" o", 1, GREEN)
    MARK_X = FONT.render(" x", 1, GREEN)
    DEFAULT = FONT.render("", 1, GREEN)

    for i in board:
        for j in i:
            if j[0] == "o":
                WIN.blit(MARK_O, j[1])
            elif j[0] == "x":
                WIN.blit(MARK_X, j[1])
            else:
                WIN.blit(DEFAULT, j[1])


def check_if_won(board, player):
    """Check if a player won"""

    marks = [[y[0] for y in x] for x in board]

    return ((marks[0][0] == marks[0][1]
         and marks[0][1] == marks[0][2]
         and marks[0][2] == player.mark)

                         or

            (marks[1][0] == marks[1][1]
         and marks[1][1] == marks[1][2]
         and marks[1][2] == player.mark)

                         or

            (marks[2][0] == marks[2][1]
         and marks[2][1] == marks[2][2]
         and marks[2][2] == player.mark)

                         or

            (marks[0][0] == marks[1][0]
         and marks[1][0] == marks[2][0]
         and marks[2][0] == player.mark)

                         or

            (marks[0][1] == marks[1][1]
         and marks[1][1] == marks[2][1]
         and marks[2][1] == player.mark)

                         or

            (marks[0][2] == marks[1][2]
         and marks[1][2] == marks[2][2]
         and marks[1][2] == player.mark)

                         or

            (marks[0][0] == marks[1][1]
         and marks[1][1] == marks[2][2]
         and marks[2][2] == player.mark)

                         or

            (marks[0][2] == marks[1][1]
         and marks[1][1] == marks[2][0]
         and marks[2][0] == player.mark))


def get_new_data():
    """Get new data"""


def draw(board):
    """Draw the things"""
    WIN.fill(WHITE)
    draw_board()
    update_board(board)
    pygame.display.update()
    CLOCK.tick(FPS)


def create_board():
    """Create a new board"""
    CELL_WIDTH, CELL_HEIGHT = 150, 150
    board = []

    for i in range(3):
        y = i*CELL_HEIGHT
        board.append([])
        for j in range(3):
            x = j*CELL_WIDTH
            board[i].append(0)
            board[i][j] = ["", (x, y)]

    return board


def main():
    """Start of the program"""

    game = client.receive()
    player = game.get_player()
    print(game)
    print(player.mark)

    game_on = True
    while game_on:

        # Event loop
        for event in pygame.event.get():

            # QUIT
            if event.type == pygame.QUIT:
                for _player in game.players:
                    if _player.mark == player.mark:
                        print(_player.mark)
                        res = game.rem_player(_player.mark)
                        break
                    res = False
                if res:
                    client.send(["!rem", game])
                else:
                    print(f"[ERROR] Player does not exist!")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP and len(game.players) == 2:
                pos = pygame.mouse.get_pos()

                x, y = pos

                # Find the clicked box
                if x in range(SIDE):
                    j = 0
                elif x in range(SIDE, 2*SIDE):
                    j = 1
                else:
                    j = 2

                if y in range(SIDE):
                    i = 0
                elif y in range(SIDE, 2*SIDE):
                    i = 1
                else:
                    i = 2

                # Update board
                if not game.board[i][j][0]:
                    game.board[i][j][0] = player.mark

        if len(game.players) == 2:
            client.send(game)
            game = client.receive()

            # Update window
            draw(game.board)

            if check_if_won(game.board, player):
                print(player, "won!")
                game.board = create_board()   # FOR NOW: It creates a new board
        else:
            client.send(game)
            game = client.receive()

            draw(game.board)


if __name__ == "__main__":
    main()
