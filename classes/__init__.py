# standard library
import os, sys

# third party library

# local
from classes.settings import LOG
from classes.settings import CONFIG

# relative pathing
path = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
print(path)
if path not in sys.path:
    print('inserting {!r} into sys.path'.format(path))
    sys.path.insert(0, path)