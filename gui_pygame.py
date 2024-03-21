import pygame
import time
import sys
from CheckersBackend import Game, Board, PlayerType, Piece
from Bot import VerySillyBot


pygame.init()

size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Шашки")

black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

cell_size = 100
board_size = 8


def draw_board(board):
    for row in range(board_size):
        for col in range(board_size):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, white, [col * cell_size, row * cell_size, cell_size, cell_size])
            else:
                pygame.draw.rect(screen, black, [col * cell_size, row * cell_size, cell_size, cell_size])
            piece = board.board[row][col]
            center = (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2)
            if piece in [Piece.WHITE_CHECKER, Piece.WHITE_KING]:
                pygame.draw.circle(screen, red, center, 40)
            elif piece in [Piece.BLACK_CHECKER, Piece.BLACK_KING]:
                pygame.draw.circle(screen, green, center, 40)


def main():
    wins1 = wins2 = 0
    clock = pygame.time.Clock()
    player1 = VerySillyBot()
    player2 = VerySillyBot()
    game = Game(player1, player2)

    while True:
        res = game.make_turn()
        if res:
            if res == "player_2 Lost":
                wins1 += 1
            if res == "player_1 Lost":
                wins2 += 1
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        draw_board(game.board)
        pygame.display.flip()
        clock.tick(2)

    print(f'{wins1= }, {wins2= }')

if __name__ == "__main__":
    main()
