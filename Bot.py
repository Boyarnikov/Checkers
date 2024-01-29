import CheckersBackend
import random


class VerySillyBot(CheckersBackend.Player):
    def move(self, moves):
        return random.choice(moves)
