from utils.board import Board
from utils.ai import BasePlayer
from config.conf import settings

b = Board(**settings['board'])
for i in range(4):
    p = BasePlayer("ai{}".format(i))
    b.add_player(p)

while not b.check_for_winners():
    b.take_turn()

print(b)
