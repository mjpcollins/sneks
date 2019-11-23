from utils.ai import BasePlayer
from utils.board import Board


def play_a_game(settings, snakes_and_ladders=False):
    """
    Takes input settings and plays a game. Outputs the final configuration of the game.

    :param settings: A dict containing all the information loaded from a json file
    :param snakes_and_ladders: Optional arg. If blank, will just use the snakes and ladders from the settings,
                                if not, will use the configuration supplied.
    :return: A generated report on the matter
    """

    if snakes_and_ladders:
        settings['board']['snakes_and_ladders'] = snakes_and_ladders

    b = Board(**settings['board'])
    for i in range(settings['players']['number_of_players']):
        p = BasePlayer("ai{}".format(i))
        b.add_player(p)

    while not b.check_for_winners():
        b.take_turn()

    return b.generate_report()


