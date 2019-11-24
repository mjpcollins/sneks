from utils.utils import load_settings
from utils.simulation import run_n_games

settings = load_settings("./config/settings.json")['settings']

r = run_n_games(settings, n=10)

t = sum([r[k]['turns'] for k in r]) / len(r)
s = round(sum([r[k]['game_seconds'] for k in r]) / (60 * len(r)), 0)
d = sum([r[k]['drinks'] for k in r]) / len(r)

print("Average number of turns was: {}".format(t))
print("Average number of minutes was: {}".format(s))
print("Average number of drinks was: {}".format(d))
