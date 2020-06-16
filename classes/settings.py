import json
import os.path
# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
global CONFIG

CONFIG = []


def init():
    global CONFIG
    CONFIG = json.load(
        open(os.path.dirname(__file__) + '/../config/units.ini'))
