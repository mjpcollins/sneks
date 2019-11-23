
import random


class BasePlayer:

    def __init__(self, name="ai"):
        self._position = 0
        self._name = name
        self._rps = ['Rock', 'Paper', 'Scissors']

    def __str__(self):
        return "This is {}, located at {}".format(self._name, self._position)

    def move(self, dice_result: int):
        self._position = self._position + dice_result
        return self._position

    def get_position(self):
        return self._position

    def clash_with(self, player: object):
        try:
            assert self != player
        except:
            return False

        if player.get_position() == self.get_position():
            return True
        return False

    def select_rock_paper_scissors(self):
        return random.choice(self._rps)

    def moveup(self):
        self._position = self._position + 10

    def movedown(self):
        self._position = self._position - 10
