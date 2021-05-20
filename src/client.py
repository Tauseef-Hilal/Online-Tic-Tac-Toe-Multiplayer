"""
    client.py

    Handle Client-side
"""

import sys
from random import choice
import pygame
from src.classes import Network
pygame.font.init()

# Setup the main window
SIDE, MARGIN = 150, 2
WIDTH, HEIGHT = 3 * SIDE, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Setup Clock()
FPS = 30
CLOCK = pygame.time.Clock()

# Setup MARK
MARK = pygame.font.SysFont("Secular One", 200)
DETAILS_FONT = pygame.font.SysFont("Secular One", 100)

# Colors
BACK = (0, 240, 230)
MARKS = (30, 30, 30)
LINES = (50, 50, 50)

# Some useful comment
client = Network(server=False)


def draw_board():
    """Draw main board"""

    # COLUMNS
    x, y = 0, MARGIN
    for _ in range(4):
        pygame.draw.line(WIN, LINES, (x, y),
                        (x, HEIGHT - (HEIGHT - WIDTH - MARGIN)), 9)
        x += SIDE

    # ROWS
    x, y = 0, MARGIN
    for _ in range(4):
        pygame.draw.line(WIN, LINES, (x, y), (WIDTH, y), 9)
        y += SIDE
    
    # DETAILS
    # x, y = (WIDTH / 2 - 9 / 5), (y - SIDE)
    # pygame.draw.line(WIN, LINES, (x, y), 
    #                 (x, y + (SIDE / 2) - 15), 9)
    # pygame.draw.rect(WIN, LINES, ())


def update_board(board, game):
    """Place marks on the board"""
    MARK_O = MARK.render(" o", 1, MARKS)
    MARK_X = MARK.render(" x", 1, MARKS)
    DEFAULT = MARK.render("", 1, MARKS)

    # MARKS
    for i in board:
        for j in i:
            if j[0] == "o":
                WIN.blit(MARK_O, j[1])
            elif j[0] == "x":
                WIN.blit(MARK_X, j[1])
            else:
                WIN.blit(DEFAULT, j[1])
    
    # DETAILS
    if game.whose_turn:
        TURN = DETAILS_FONT.render(f"  {game.whose_turn.title()}'s   MOVE", 1, MARKS)
    else:
        TURN = DETAILS_FONT.render(f"  WAITING...", 1, MARKS)
    
    WIN.blit(TURN, (0, SIDE*3 + 9 + 30))


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


def draw(board, game):
    """Draw the things"""
    WIN.fill(BACK)
    draw_board()
    update_board(board, game)
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

            if len(game.players) == 2:
                if event.type == pygame.MOUSEBUTTONUP \
                and game.whose_turn == player.mark:
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
                        game.whose_turn = opponent.mark
                        game.moves += 1

        if len(game.players) == 2:

            client.send(game)
            game = client.receive()
            players = game.players

            if not game.whose_turn:
                try:
                    opponent = players[0] if player != players[0] else players[1]
                except:
                    continue
                game.whose_turn = choice(["o", "x"])

            # Update window
            draw(game.board, game)

            if check_if_won(game.board, player):
                print(player, "won!")
                game.board = create_board()   # FOR NOW: It creates a new board
            else:
                if game.moves == 9:
                    print("DRAW!")
                    game.board = create_board()
        else:
            game.moves = 0
            game.whose_turn = None
            client.send(game)
            game = client.receive()

            draw(game.board, game)


if __name__ == "__main__":
    main()
