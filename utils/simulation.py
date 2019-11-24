from utils.ai import BasePlayer
from utils.board import Board


def play_a_game(settings, snakes_and_ladders=False, report_frequency='end'):
    """
    Takes input settings and plays a game. Outputs the final configuration of the game.

    :param settings: A dict containing all the information loaded from a json file
    :param snakes_and_ladders: Optional arg. If blank, will just use the snakes and ladders from the settings,
                                if not, will use the configuration supplied.
    :param report_frequency: Choice for frequency of reports. Options are: 'end' for end of game, and 'turn' for
                                a report every turn.
    :return: A generated report on the matter
    """

    if snakes_and_ladders:
        settings['board']['snakes_and_ladders'] = snakes_and_ladders

    b = Board(**settings['board'])

    for i in range(settings['players']['number_of_players']):
        p = BasePlayer("ai{}".format(i))
        b.add_player(p)

    if report_frequency == 'end':
        while not b.check_for_winners():
            b.take_turn()
        final_report = b.generate_report()

    elif report_frequency == 'turn':
        final_report = dict()

        while not b.check_for_winners():
            t = b.get_number_of_turns()
            r = b.generate_report()
            final_report[t] = r
            b.take_turn()

        t = b.get_number_of_turns()
        r = b.generate_report()
        final_report[t] = r

    else:
        raise ValueError('{} is not a valid input'.format(report_frequency))

    return final_report


