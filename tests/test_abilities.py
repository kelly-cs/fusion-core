
""" Unit Testing For Abilities """

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
from enum import Enum

# third party library
import pytest
from unittest.mock import MagicMock
# local
from classes.base import Base
from classes.building import Building
from classes.player import Race
from classes.settings import CONFIG

startingworkers = CONFIG["startingworkers"]["amount"]
races = [Race.ZERG, Race.TERRAN, Race.PROTOSS]

# returns a fully constructed base for each race to play with
@pytest.fixture(scope="module",params=races)
def base(request):
    race = request.param
    base = Base(startingworkers, race, "normal", "normal", 2, False, True)
    return base

def test_base_abilities(base):
    if base.raceType == Race.ZERG:
        assert base.currentlarva == 3 # starting larvae should be 3 
        # create a queen
        base.has_queen = 1
        # as soon as a queen is created, it should be able to inject always.
        assert base.inject() == True
        # there should not be enough energy to inject twice consecutively right off the bat
        assert base.inject() == False
        # inject time remaining should be updated
        assert base.injectTimeRemaining == base.injectTime
        # ticking up should decrement injectTimeRemaining by 1
        base.tickUp(1)
        assert base.currentlarva == 3 # starting larvae should STILL be 3 - the inject hasn't finished yet.
        assert base.injectTimeRemaining == base.injectTime - 1
        # finishing inject time remaining should increase larvae count and end the timer
        base.tickUp(base.injectTimeRemaining + 1)
        assert base.injectTimeRemaining == 0
        assert base.currentlarva == 3 + base.injectAmt # put this in settings later
    elif base.raceType == Race.TERRAN:
        pass
    elif base.raceType == Race.PROTOSS:
        pass
        
if __name__ == '__main__':
    # test this file only
    pytest.main([__file__])