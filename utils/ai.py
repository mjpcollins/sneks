
import random


class BasePlayer:

    def __init__(self, name="ai"):
        self._position = 0
        self._drinks = 0
        self._name = name
        self._rps = ['Rock', 'Paper', 'Scissors']  # TODO: Remove the hardcoding

    def __str__(self):
        return "{} at {} and has had {} drinks".format(self._name, self._position, self._drinks)

    def move(self, move_spaces: int, board: object):
        """
        Set a new position dependant on the result of a dice roll

        :param move_spaces: Int value for the number of spaces to move
        :param board: the board that the game is being played on
        :return: Players who have just been overtaken
        """

        if self._position < 10:
            starting_level = board._start_number
        else:
            starting_level = int(str(int(self._position))[:-1])

        if move_spaces > 0:

            players_ahead = [player for player in board.get_list_of_players()
                             if player.get_position() > self.get_position()]

            self._position = self._position + move_spaces
            self._check_within_limits(upper_limit=board._end_number, lower_limit=board._start_number)

            players_behind = [player for player in players_ahead if player.get_position() < self.get_position()]

            # Silly people who were overtaken. They're too slow!
            for p in players_behind:
                p.take_a_drink()

            if self._position < 10:
                current_level = board._start_number
            else:
                current_level = int(str(int(self._position))[:-1])

            # Time to delegate the pain (if we can)
            for _ in range(current_level - starting_level):
                self.delegate_a_drink(board.get_list_of_players())

        elif move_spaces < 0:

            players_behind = [player for player in board.get_list_of_players()
                              if player.get_position() < self.get_position()]

            self._position = self._position + move_spaces
            self._check_within_limits(upper_limit=board._end_number, lower_limit=board._start_number)

            players_ahead = [player for player in players_behind if player.get_position() > self.get_position()]

            # take drinks for people who overtook us due to our blunder
            for _ in players_ahead:
                self.take_a_drink()

            if self._position < 10:
                current_level = board._start_number
            else:
                current_level = int(str(int(self._position))[:-1])

            # and accept punishment for moving down levels
            if starting_level > current_level:
                self.take_a_drink(starting_level - current_level)

        board._update_registry()

        board._check_snakes_and_ladders()

        return self._position

    def get_drinks(self):
        return self._drinks

    def get_position(self):
        """

        :return: Current position on the board
        """
        return self._position

    def take_a_drink(self, drinks=1):
        self._drinks = self._drinks + drinks
        return self._drinks

    def delegate_a_drink(self, players):
        """
        Pick a random player and delegate a drink. Make sure not to pick self. (Though, within the rules that is legal.)

        Grudges are not implemented. TODO: Implement grudges. (Sounds like game theory?)

        :param player: Player giving a drink
        :return: None
        """

        p = random.choice(players)
        while p != self:
            p = random.choice(players)
        p.take_a_drink()

    def clash_with(self, player: object, min_loc: int=0):
        """
        Check whether or not this player clashes with the given player object

        If a self is located at min_loc, skip.

        :param player: Player to check the object with
        :return: Boolean on whether or not the clash
        """

        if self.get_position() == min_loc:
            return False

        try:
            assert self != player
        except:
            return False

        if self.get_position() == player.get_position():
            return True
        return False

    def select_rock_paper_scissors(self):
        """
        Return an item from the Rock, Paper, Scissor list

        :return: The chosen item from the Rock Paper Scissor list
        """

        return random.choice(self._rps)

    def _check_within_limits(self, upper_limit=100, lower_limit=0):
        """

        :param upper_limit:
        :param lower_limit:
        :return:
        """

        # Reset if over the limit
        if self._position > upper_limit:
            self._position = self._position - (self._position - upper_limit)
        # Go to zero if knocked too low
        if self._position < lower_limit:
            self._position = lower_limit


