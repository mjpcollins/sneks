
from utils.utils import roll_dice, rock_paper_scissors
from utils.ai import BasePlayer
import numpy as np


class Board:

    def __init__(self, **kwargs):
        self._dice_config = kwargs['dice_config']
        self._end_number = kwargs['end_number']
        self._players = []
        self._register_of_locations = None
        self._matrix = kwargs['rps_matrix']

    def __str__(self):
        s = "Current state of board:\n"

    def add_player(self, player: BasePlayer):
        """
        Add a player to the board

        :param player: BasePlayer object to be added to the board
        :return: None
        """
        self._players.append(player)
        self.reset_register()

    def take_turn(self):
        """
        Simulate one turn on the board

        :return: None
        """

        # Loop through each of the players in the order they were added to the board
        for i, p in enumerate(self._players):
            res = sum(roll_dice(**self._dice_config))

            # update the register
            self._register_of_locations[i] = p.move(res)

            # Check for any location clashes
            if len(np.unique(self._register_of_locations)) < len(self._register_of_locations):
                for pl in self._players:
                    if p.clash_with(pl):
                        a = rock_paper_scissors(p, pl, self._matrix)
                        a['winner'].moveup()
                        a['loser'].movedown()
            print()

    def get_list_of_players(self):
        return self._players

    def info_on_players(self):
        return {p: p.get_position() for p in self._players}

    def check_for_winners(self):
        if self._end_number in self._register_of_locations:
            i = np.where(self._register_of_locations == self._end_number)
            return self._players

    def reset_register(self):
        self._register_of_locations = np.array([0 for _ in range(len(self._players))])


