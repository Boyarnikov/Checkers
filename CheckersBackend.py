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


class PossibleMoveGenerator:
    """
    Класс который описывает логику поиска всех корректных ходов.
    Подразумевается что каждый внутренний запрос идёт от лица первого игрока
    """

    @staticmethod
    def get_possible_moves(board, player: PlayerType):
        """
        Запрос на все кооретные ходы
        :param board: Изначальная доска
        :param player: Игрок для которого делается ход
        :return: list всех кооретных досок, продолжений игры
        """
        our_figs = (Piece.WHITE_CHECKER, Piece.WHITE_KING)
        enemy_figs = (Piece.BLACK_CHECKER, Piece.BLACK_KING)
        moves = []
        takes = []
        forced_takes = False
        b = board

        if player == PlayerType.BLACK:
            b = b.change_perspective()

        for y, row in enumerate(b.board):
            for x, item in enumerate(row):
                if item in our_figs:
                    _takes, _moves = PossibleMoveGenerator._get_checker_move(b, x, y)
                    moves.extend(_moves)
                    takes.extend(_takes)

        # print(f"found {len(takes)} takes and {len(moves)} moves")
        if takes:
            moves = takes

        if player == PlayerType.BLACK:
            for i in range(len(moves)):
                moves[i] = moves[i].change_perspective()

        return moves

    @staticmethod
    def _generate_all_checker_takes(board, x, y):
        moves = []
        for position in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
            move = PossibleMoveGenerator._get_checker_one_take_move(board, x, y, x + position[0], y + position[1])
            if move:
                all_moves = PossibleMoveGenerator._generate_all_checker_takes(move, x + position[0], y + position[1])
                if all_moves:
                    moves.extend(all_moves)
                else:
                    moves.append(move)

        return moves

    @staticmethod
    def _get_checker_one_cell_move(board, x, y, x1, y1):
        """
        :param board:
        :param x: :param y: Клетка с которой берётся шашка
        :param x1: :param y1: Клетка куда мы хотим переместить шашку
        :return: Возвращает ход если он корректен, иначе None
        """
        if abs(x - x1) != 1 or abs(y - y1) != 1:
            raise ValueError("Ход выполнен больше чем на одну клетку")

        if (0 <= x < 8) and (0 <= y < 8) and (0 <= x1 < 8) and (0 <= y1 < 8):
            if board.board[y1][x1] == Piece.FREE:
                move = board.copy()
                move.board[y1][x1] = board.board[y][x]
                move.board[y][x] = board.board[y1][x1]
                return move
        return None

    @staticmethod
    def _get_checker_one_take_move(board, x, y, x1, y1):
        """
        :param board:
        :param x: :param y: Клетка с которой берётся шашка
        :param x1: :param y1: Клетка куда мы хотим переместить шашку, срубив среднюю клетку
        :return: Возвращает ход если он корректен, иначе None
        """
        enemy = (Piece.BLACK_CHECKER, Piece.BLACK_KING)

        if abs(x - x1) != 2 or abs(y - y1) != 2:
            raise ValueError("Ход выполнен больше чем на одну клетку")

        if 0 <= x < 8 and 0 <= y < 8 and 0 <= x1 < 8 and 0 <= y1 < 8:
            xm, ym = (x + x1) // 2, (y + y1) // 2
            if board.board[y1][x1] == Piece.FREE and board.board[ym][xm] in enemy:
                move = board.copy()
                move.board[y1][x1] = board.board[y][x]
                move.board[y][x] = board.board[y1][x1]
                move.board[ym][xm] = Piece.FREE
                return move
        return None

    @staticmethod
    def _get_checker_move(board, x, y):
        """
        Функия, описывающая все ходы для конкретной шашки
        :return: первый аргумент - все корректные ходы со взятием, второй - без
        """
        enemy = (Piece.BLACK_CHECKER, Piece.BLACK_KING)

        if y == 0:
            return [], []
        moves = []

        moves = PossibleMoveGenerator._generate_all_checker_takes(board, x, y)

        if moves:
            return moves, []

        for position in ((-1, -1), (1, -1)):
            move = PossibleMoveGenerator._get_checker_one_cell_move(board, x, y, x + position[0], y + position[1])
            if move:
                moves.append(move)

        return [], moves


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

    def __init__(self, position=None):
        if position:
            self.board = [[Piece.FREE for j in range(8)] for i in range(8)]
            for i in range(len(position)):
                for j in range(len(position[i])):
                    if position[i][j] == 1:
                        self.board[i][j] = Piece.WHITE_CHECKER
                    elif position[i][j] == 2:
                        self.board[i][j] = Piece.BLACK_CHECKER



        else:
            self.board = [[Board.get_starting_cell_content(j, i) for j in range(8)] for i in range(8)]

    def copy(self):
        b = Board()
        b.board = [[self.board[i][j] for j in range(8)] for i in range(8)]
        return b

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
    def __init__(self, player1, player2, board=None):
        if board:
            self.board = board
        else:
            self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.turn = 1

    def make_turn(self):
        if self.turn % 2:
            res = self.player1.move(PossibleMoveGenerator.get_possible_moves(self.board, PlayerType.WHITE))
            if res is None:
                return "player_1 Lost"
            b = res
        else:
            moves = PossibleMoveGenerator.get_possible_moves(self.board, PlayerType.BLACK)
            reversed_moves = [move.change_perspective() for move in moves]
            res = self.player2.move(reversed_moves)
            if res is None:
                return "player_2 Lost"
            b = res.change_perspective()

        self.board = b
        self.turn += 1


class Player:
    def move(self, moves):
        return None
