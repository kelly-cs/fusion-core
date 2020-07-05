import json
import logging
import sys
import os.path
# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
global CONFIG
global LOG
global SHORTEST_ORDER


def init():
    global CONFIG
    global LOG

    # This will be a number to represent the fastest build order so far, represented by the remaining tick value. Higher is better.
    global SHORTEST_COMPLETED_BUILD_ORDER
    SHORTEST_COMPLETED_BUILD_ORDER = None

    CONFIG = json.load(
        open(os.path.dirname(__file__) + '/../config/units.ini'))

    # https://docs.python.org/3/howto/logging-cookbook.html
    # root logger
    LOG = logging.getLogger("all")
    LOG.setLevel(level=logging.DEBUG)
    # file handler which logs even debug messages
    fh = logging.FileHandler('debug.log')  # file output
    fh.setLevel(logging.INFO)
    # console handler with a higher log level
    ch = logging.StreamHandler()  # the console
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    # https://www.programcreek.com/python/example/184/logging.StreamHandler
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    LOG.addHandler(fh)
    LOG.addHandler(ch)
