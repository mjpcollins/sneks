
import random


def roll_dice(number_of_dice=2, sides_of_dice=6):
    """
    Utils function for rolling dice
    :param number_of_dice: Number of dice you wish to roll
    :param sides_of_dice: Number of possible outcomes
    :return: List containing all the dice that have been rolled
    """
    return [random.randint(1, sides_of_dice) for _ in range(number_of_dice)]


def rock_paper_scissors(ai1: object, ai2: object, matrix: dict):
    """
    Simulate a game of RPS between two AI.

    Return the result as a dict

    :param ai1: first AI
    :param ai2: second AI
    :return: dict object containing the winner and the loser
    """

    no_winner = True
    while no_winner:
        r1 = ai1.select_rock_paper_scissors()
        r2 = ai2.select_rock_paper_scissors()
        if matrix[r1] == r2:
            w = {"winner": ai1, "loser": ai2}
            no_winner = False
        elif matrix[r2] == r1:
            w = {"winner": ai2, "loser": ai1}
            no_winner = False

    return w

