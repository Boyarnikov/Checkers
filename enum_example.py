from enum import Enum


class Piece(Enum):
    KNIGHT = 0
    PAWN = 1
    BISHOP = 2


def f(a: Piece):
    print(a, a.name, a.value, type(a), dir(a))


f(Piece.KNIGHT)
