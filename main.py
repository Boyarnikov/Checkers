# import GUI, DebugInterface
import CheckersBackend
import Bot
import time
import flet

import GUI

if __name__ == "__main__":

    GUI.start_GUI()

    print("started")

    '''
    b = CheckersBackend.Board()
    print(b)
    #moves = CheckersBackend.PossibleMoveGenerator._get_checker_move(b, 0, 5)
    #print(moves)
    moves = CheckersBackend.PossibleMoveGenerator.get_possible_moves(b, CheckersBackend.PlayerType.WHITE)
    for i in moves:
        print(i)
    
    '''

    b = CheckersBackend.Board([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 2, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 2, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
    ])

    wins1 = 0
    wins2 = 0

    g = CheckersBackend.Game(Bot.VerySillyBot(), Bot.VerySillyBot())
    while True:
        # print(g.board)
        res = g.make_turn()

        if res:

            if res == "player_2 Lost":
                wins1 += 1
            if res == "player_1 Lost":
                wins2 += 1
            break

    print(wins1, wins2)
