
from utils.utils import roll_dice, rock_paper_scissors
from utils.ai import BasePlayer
import numpy as np
import random


class Board:

    def __init__(self, **kwargs):
        self._dice_config = kwargs['dice_config']
        self._end_number = kwargs['end_number']
        self._start_number = kwargs['start_number']
        self._snakes_and_ladders = kwargs['snakes_and_ladders']
        self._turn_time_per_person = kwargs['turn_time_per_person']
        self._rps_time = kwargs['rps_time']
        self._players = []
        self._register_of_locations = None
        self._matrix = kwargs['rps_matrix']
        self._number_of_turns = 0
        self._length_of_game = 0

    def __str__(self):
        s = "\nCurrent state of board:\n-----------------------"
        for p in self._players:
            s = s + "\n{p}".format(p=str(p))
        s = s + "\n-----------------------"
        s = s + "\nCurrently on turn {n}".format(n=self._number_of_turns)
        s = s + "\nGame has taken {m} minutes so far".format(m=round(self._length_of_game / 60, 1))
        s = s + "\n{d} drinks have been consumed in total".format(d=sum(p.get_drinks() for p in self._players))
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
        self.reset_register()

    def _check_snakes_and_ladders(self):
        """
        Check for snakes and ladders, move to the locations dictated by the chart.

        :return: None
        """
        for idx, player in enumerate(self._players):
            p = player.get_position()
            for sl in self._snakes_and_ladders:
                if p == sl[0]:
                    self._register_of_locations[idx] = player.move(sl[1] - sl[0], self._players)
                    break

    def _update_registry(self):
        self._register_of_locations = np.array([p.get_position() for p in self._players])

    def take_turn(self):
        """
        Simulate one turn on the board

        :return: None
        """

        # Loop through each of the players in the order they were added to the board
        for idx, player in enumerate(self._players):

            # Update the length of the game
            self.action_time(self._turn_time_per_person)

            # Roll the dice, move the player, and update the register
            self._register_of_locations[idx] = player.move(sum(roll_dice(**self._dice_config)), self._players)

            # Resolve the complicated stuff
            self._resolve_board_changes()

        self._number_of_turns = self._number_of_turns + 1

    def action_time(self, seconds):
        self._length_of_game = self._length_of_game + seconds

    def _resolve_board_changes(self):
        """
        Check for any changes that need to be resolved

        :return: None
        """

        self._check_snakes_and_ladders()

        # Check for any location clashes
        temp_list = self._register_of_locations[np.where(self._register_of_locations != 0)]
        while len(temp_list) > len(np.unique(temp_list)):
            # This is very greedy, should be reduced to only check that which has changed.
            for p in self._players:
                for pl in self._players:
                    if p.clash_with(pl):

                        a = rock_paper_scissors(p, pl, self._matrix)

                        # For the winner, the spoils
                        a['winner'].move_up(limit=self._end_number, players=self._players)

                        # For the loser, drinks
                        a['loser'].move_down(limit=self._start_number, players=self._players)

                        self._update_registry()
                        self.action_time(self._rps_time)

            self._check_snakes_and_ladders()

            temp_list = self._register_of_locations[np.where(self._register_of_locations != 0)]

    def get_list_of_players(self):
        return self._players

    def info_on_players(self):
        return {p: p.get_position() for p in self._players}

    def check_for_winners(self):
        if self._end_number in self._register_of_locations:
            i = np.where(self._register_of_locations == self._end_number)
            return self._players
        else:
            return False

    def reset_register(self):
        self._register_of_locations = np.array([0 for _ in range(len(self._players))])

    def generate_report(self):
        j = dict()
        j['board'] = {
            'turns': self._number_of_turns,
            'game_seconds': self._length_of_game,
            'drinks': sum(p.get_drinks() for p in self._players)
        }
        j['players'] = {p._name: {'final_position': p.get_position(),'drinks': p.get_drinks()} for p in self._players}
        return j
