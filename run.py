from utils.board import Board
from utils.ai import BasePlayer
from utils.utils import load_settings

b = Board(**load_settings("./config/example_settings.json")['settings']['board'])
for i in range(4):
    p = BasePlayer("ai{}".format(i))
    b.add_player(p)

while not b.check_for_winners():
    b.take_turn()

r = b.generate_report()
print(r)