""" Unit Testing For Simulation """

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
import os, sys

# third party library
import pytest

# local
path = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
print(path)
if path not in sys.path:
    print('inserting {!r} into sys.path'.format(path))
    sys.path.insert(0, path)

from classes.gamestate import GameState
from classes.player import Player, Race
from classes.building import Building
from classes.unit import Unit

def run_tests():
    assert zerg_build_order_test() == True
    assert terran_build_order_test() == True
    assert protoss_build_order_test() == True

# Implement Later, should return build order in format:
# [["action","remainingticks"], etc.]


def zerg_build_order_test():
    return True


def terran_build_order_test():
    return True


def protoss_build_order_test():
    return True


# pytest.main.<
if __name__ == "__main__":
    output = run_tests()
