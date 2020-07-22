
""" Testing for Geysers """

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library

# third party library
import pytest
from unittest.mock import MagicMock
# local
from classes.base import Base
from classes.settings import CONFIG
from classes.unit import Unit

from classes.player import Race
from classes.settings import CONFIG

startingworkers = CONFIG["startingworkers"]["amount"]
races = [Race.ZERG, Race.TERRAN, Race.PROTOSS]
amt_geysers = 2
mineral_type = "normal"
gas_type = "normal"
first_base = True
under_construction = False
# returns a fully constructed base for each race to play with
@pytest.fixture(scope="module",params=races)
def base(request):
    race = request.param
    base = Base(startingworkers, race, mineral_type, gas_type, amt_geysers, under_construction, first_base)
    return base
    
# 
def test_geyser_building(base):
    if base.raceType == Race.ZERG:
        if base.amtGeysers > 0:
            assert base.builtGeysers == 0 # not built yet
            assert base.geysersUnderConstruction[0] == False
            assert base.buildGeyser() # assert that building a geyser works.
            assert base.geysersRemainingTime[0] == CONFIG["extractor"]["time"] + CONFIG["timeToTransferWorkersFromMinsToGas"]["time"]
            assert base.geysersUnderConstruction[0] == True
            base.tickUp(1)
            assert base.geysersUnderConstruction[0] == True
            assert base.geysersRemainingTime[0] == CONFIG["extractor"]["time"] + CONFIG["timeToTransferWorkersFromMinsToGas"]["time"] - 1
            assert base.transferMinsToGas() == False # extractor is not done yet.
            assert base.transferGasToMins() == False # can't send gas to mins if it doesn't exist
            base.tickUp(CONFIG["extractor"]["time"] + CONFIG["timeToTransferWorkersFromMinsToGas"]["time"] - 1)
            assert base.geysersRemainingTime[0] == 0
            assert base.geysersUnderConstruction[0] == False
            assert base.builtGeysers == 1

if __name__ == '__main__':
    # test this file only
    pytest.main([__file__])