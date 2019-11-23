from utils.ai import BasePlayer
from utils.board import Board


def play_a_game(settings):
    """
    Takes input settings and plays a game. Outputs the final configuration of the game.

    :param settings: A dict containing all the information loaded from a json file
    :return: A generated report on the matter
    """

    b = Board(**settings['board'])
    for i in range(settings['players']['number_of_players']):
        p = BasePlayer("ai{}".format(i))
        b.add_player(p)

    while not b.check_for_winners():
        b.take_turn()

    return b.generate_report()

