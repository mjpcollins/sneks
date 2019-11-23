from utils.board import Board
from utils.ai import BasePlayer
from utils.utils import load_settings

settings = load_settings("./config/settings.json")['settings']

b = Board(**settings['board'])
for i in range(settings['players']['number_of_players']):
    p = BasePlayer("ai{}".format(i))
    b.add_player(p)

while not b.check_for_winners():
    b.take_turn()

r = b.generate_report()
print(r)
