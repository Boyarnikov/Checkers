import enum


class PlayerType(enum.Enum):
    WHITE = 0
    BLACK = 1


class Piece(enum.Enum):
    WHITE_CHECKER = 0
    WHITE_KING = 1
    BLACK_CHECKER = 2
    BLACK_KING = 3
    FREE = -1


class Board:
    board = list()

    @staticmethod
    def get_starting_cell_content(x, y):
        if (x + y) % 2:
            if y < 3:
                return Piece.BLACK_CHECKER
            elif y > 4:
                return Piece.WHITE_CHECKER
            else:
                return Piece.FREE
        return None

    def __init__(self):
        self.board = [[Board.get_starting_cell_content(j, i) for j in range(8)] for i in range(8)]

    def copy(self):
        b = Board()
        b.board = [[self.board[i][j] for j in range(8)] for i in range(8)]
        return b

    def get_checker_move(self, x, y):
        enemy = (Piece.BLACK_CHECKER, Piece.BLACK_KING)

        if y == 0:
            return []
        moves = []
        if x > 0 and self.board[y - 1][x - 1] == Piece.FREE:
            move = self.copy()
            move.board[y - 1][x - 1] = self.board[y][x]
            move.board[y][x] = self.board[y - 1][x - 1]
            moves.append(move)
        if x < 7 and self.board[y - 1][x + 1] == Piece.FREE:
            move = self.copy()
            move.board[y - 1][x + 1] = self.board[y][x]
            move.board[y][x] = self.board[y - 1][x + 1]
            moves.append(move)
        if x > 1 and y > 1 and (self.board[y - 1][x - 1] in enemy) and self.board[y - 2][x - 2] == Piece.FREE:
            move = self.copy()
            move.board[y - 2][x - 2] = self.board[y][x]
            move.board[y][x] = self.board[y - 2][x - 2]
            move.board[y - 1][x - 1] = Piece.FREE
            moves.append(move)
        if x < 6 and y > 1 and (self.board[y - 1][x + 1] in enemy) and self.board[y - 2][x + 2] == Piece.FREE:
            move = self.copy()
            move.board[y - 2][x + 2] = self.board[y][x]
            move.board[y][x] = self.board[y - 2][x + 2]
            move.board[y - 1][x + 1] = Piece.FREE
            moves.append(move)
        return moves

    def get_possible_moves(self, player: PlayerType):
        our_figs = (Piece.WHITE_CHECKER, Piece.WHITE_KING)
        enemy_figs = (Piece.BLACK_CHECKER, Piece.BLACK_KING)
        moves = []
        b = self

        if player == PlayerType.BLACK:
            b = b.change_perspective()

        for y, row in enumerate(b.board):
            for x, item in enumerate(row):
                if item in our_figs:
                    moves.extend(b.get_checker_move(x, y))

        if player == PlayerType.BLACK:
            for i in range(len(moves)):
                moves[i] = moves[i].change_perspective()

        return moves

    counterparts = {
        None: None,
        Piece.FREE: Piece.FREE,
        Piece.WHITE_KING: Piece.BLACK_KING,
        Piece.BLACK_KING: Piece.WHITE_KING,
        Piece.WHITE_CHECKER: Piece.BLACK_CHECKER,
        Piece.BLACK_CHECKER: Piece.WHITE_CHECKER,
    }

    def change_perspective(self):
        b = Board()
        b.board = [[self.counterparts[self.board[7 - i][7 - j]] for j in range(8)] for i in range(8)]
        return b

    def __str__(self):
        s = ""
        for row in self.board:
            for item in row:
                if item:
                    if item == Piece.FREE:
                        s += "_ "
                    else:
                        s += str(item.value) + " "
                else:
                    s += " " + " "
            s += "\n"
        return s


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.turn = 1

    def make_turn(self):
        if self.turn % 2:
            b = self.player1.move(self.board.get_possible_moves(PlayerType.WHITE))
        else:
            b = self.player2.move(self.board.get_possible_moves(PlayerType.BLACK))

        self.board = b
        self.turn += 1


class Player:
    def move(self, moves):
        return None

