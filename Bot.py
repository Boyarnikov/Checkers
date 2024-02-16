import CheckersBackend
from CheckersBackend import Piece
import random


def evaluate_position(board: CheckersBackend.Board):
    enemy = (Piece.BLACK_CHECKER, Piece.BLACK_KING)
    team = (Piece.WHITE_CHECKER, Piece.WHITE_CHECKER)

    e = 0
    for row in board.board:
        for piece in row:
            if piece in team:
                e += 1
            if piece in enemy:
                e -= 1

    return e


class VerySillyBot(CheckersBackend.Player):
    def move(self, moves):
        if moves:
            return random.choice(moves)


class Bot(CheckersBackend.Player):
    def move(self, moves: list):
        if not moves:
            return None

        max_eval = max([evaluate_position(move) for move in moves])
        moves = [move for move in moves if max_eval == evaluate_position(move)]
        if moves:
            return random.choice(moves)