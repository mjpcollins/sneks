
import random


class BasePlayer:

    def __init__(self, name="ai"):
        self._position = 0
        self._name = name
        self._rps = ['Rock', 'Paper', 'Scissors']  # TODO: Remove the hardcoding

    def __str__(self):
        return "{} at {}".format(self._name, self._position)

    def move(self, dice_result: int):
        """
        Set a new position dependant on the result of a dice roll

        :param dice_result:
        :return:
        """

        self._position = self._position + dice_result
        self._check_within_limits()
        return self._position

    def get_position(self):
        """

        :return: Current position on the board
        """
        return self._position

    def clash_with(self, player: object):
        """
        Check whether or not this player clashes with the given player object

        :param player: Player to check the object with
        :return: Boolean on whether or not the clash
        """

        try:
            assert self != player
        except:
            return False

        if player.get_position() == self.get_position():
            return True
        return False

    def select_rock_paper_scissors(self):
        """
        Return an item from the Rock, Paper, Scissor list

        :return: The chosen item from the Rock Paper Scissor list
        """

        return random.choice(self._rps)

    def _check_within_limits(self, upper_limit=100, lower_limit=0):
        # Reset if over the limit
        if self._position > upper_limit:
            self._position = self._position - 10
        # Go to zero if knocked too low
        if self._position < lower_limit:
            self._position = lower_limit

    def move_up(self, limit=100):
        """
        Knock the player up a level

        :param limit: The max value on the board
        :return: None
        """

        self._position = self._position + 10
        self._check_within_limits(upper_limit=limit)
        return self._position

    def move_down(self, limit=0):
        """
        Knock the player down a level

        :param limit: The min value on the board
        :return: None
        """

        self._position = self._position - 10
        self._check_within_limits(lower_limit=limit)
        return self._position


