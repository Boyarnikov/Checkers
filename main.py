#import GUI, DebugInterface
import CheckersBackend
import Bot
import time
import flet

if __name__ == "__main__":
    print("started")
    g = CheckersBackend.Game(Bot.VerySillyBot(), Bot.VerySillyBot())
    while True:
        print(g.board)
        g.make_turn()

        time.sleep(3)
