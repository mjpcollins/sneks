from utils.utils import load_settings
from utils.simulation import play_a_game

settings = load_settings("./config/settings.json")['settings']

r = play_a_game(settings)

print(r)
