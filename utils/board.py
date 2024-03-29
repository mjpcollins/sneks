
from utils.utils import roll_dice, rock_paper_scissors
from utils.ai import BasePlayer
import numpy as np

#
# Decorator
#


def game_over_check(func):

    def function_wrapper(*args):

        # If the game has been won, prevent any further functions being run
        if args[0].is_game_over():
            return None
        else:
            return func(*args)

    return function_wrapper

#
# Class
#


class Board:

    def __init__(self, **kwargs):
        self._dice_config = kwargs['dice_config']
        self._end_number = kwargs['end_number']
        self._start_number = kwargs['start_number']
        self._snakes_and_ladders = kwargs['snakes_and_ladders']
        self._turn_time_per_person = kwargs['turn_time_per_person']
        self._rps_time = kwargs['rps_time']
        self._snl_time = kwargs['snl_time']
        self._players = []
        self._game_is_over = False
        self._register_of_locations = self._update_registry()
        self._matrix = kwargs['rps_matrix']
        self._number_of_turns = 0
        self._length_of_game = 0

    def __str__(self):
        s = "\nCurrent state of board:\n-----------------------"
        for player in self.get_list_of_players():
            s = s + "\n{p}".format(p=str(player))
        s = s + "\n-----------------------"
        s = s + "\nCurrently on turn {n}".format(n=self._number_of_turns)
        s = s + "\nGame has taken {m} minutes so far".format(m=round(self._length_of_game / 60, 1))
        s = s + "\n{d} drinks have been consumed in total".format(d=sum(player.get_drinks()
                                                                        for player in self.get_list_of_players()))
        return s

    def get_number_of_turns(self):
        return self._number_of_turns

    def add_player(self, player: BasePlayer):
        """
        Add a player to the board

        :param player: BasePlayer object to be added to the board
        :return: None
        """
        self._players.append(player)
        self._update_registry()

    @game_over_check
    def take_turn(self):
        """
        Simulate one turn on the board

        :return: None
        """

        # Loop through each of the players in the order they were added to the board
        for player in self.get_list_of_players():

            # Although the decorator checks on run of the function, this will prevent further movement in win occurs
            if not self.check_for_winners():

                # Update the length of the game
                self._action_time(self._turn_time_per_person)

                # Roll the dice, move the player
                player.move(sum(roll_dice(**self._dice_config)), board=self)

                # Resolve the complicated stuff
                self._resolve_board_changes()

        self._number_of_turns = self._number_of_turns + 1

    def check_for_winners(self):
        self._game_is_over = self._end_number in self._register_of_locations
        return self._game_is_over

    def is_game_over(self):
        return self._game_is_over

    def get_list_of_players(self):
        return self._players

    def generate_report(self):
        j = dict()
        j['board'] = {
            'turns': self._number_of_turns,
            'game_seconds': self._length_of_game,
            'drinks': sum(player.get_drinks() for player in self.get_list_of_players())
        }
        j['players'] = {player._name: {'position': player.get_position(),'drinks': player.get_drinks()}
                        for player in self.get_list_of_players()}
        return j

    @game_over_check
    def _check_snakes_and_ladders(self):
        """
        Check for snakes and ladders, move to the locations dictated by the matrix.

        :return: None
        """
        for player in self.get_list_of_players():
            for snake_or_ladder in self._snakes_and_ladders:
                if snake_or_ladder[0] == player.get_position():
                    player.move(snake_or_ladder[1] - snake_or_ladder[0], self)
                    self._action_time(self._snl_time)
                    # I assume that no one is chaining together snakes or ladders. Please don't do that.
                    break

    @game_over_check
    def _resolve_board_changes(self):
        """
        Check for any changes that need to be resolved. Loops resolving RPS until everyone's position is unique

        :return: None
        """

        # Loop while location clashes exist
        while self.check_for_clashes():
            # This is very greedy, should be reduced to only check that which has changed.
            for player1 in self.get_list_of_players():
                for player2 in self.get_list_of_players():
                    if player1.clash_with(player2, min_loc=self._start_number):

                        result = rock_paper_scissors(player1, player2, self._matrix)

                        # For the winner, the spoils
                        result['winner'].move(10, board=self)

                        # For the loser, the drinks
                        result['loser'].move(-10, board=self)

                        self._action_time(self._rps_time)

    def check_for_clashes(self):
        temp_list = self._register_of_locations[np.where(self._register_of_locations != 0)]
        return len(temp_list) > len(np.unique(temp_list))

    def _update_registry(self):
        """
        Update the registry for all current locations of players. Registry could be removed, but might make
        other parts less obvious in logic.

        :return: Current register
        """

        self._register_of_locations = np.array([player.get_position() for player in self.get_list_of_players()])
        self.check_for_winners()
        return self._register_of_locations

    def _action_time(self, seconds):
        self._length_of_game = self._length_of_game + seconds


