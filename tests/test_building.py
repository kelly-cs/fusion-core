
""" Unit Testing For Building """

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library

# third party library
import pytest
from unittest.mock import MagicMock
# local
from classes.building import Building
from classes.settings import CONFIG
from classes.unit import Unit

all_units = []
all_buildings = []

for content in CONFIG.keys():
    print(content)
    if "isbuilding" in CONFIG[content] and CONFIG[content]["isbuilding"] and "issetting" not in CONFIG[content]:
        all_buildings.append(content)
    elif "isbuilding" in CONFIG[content] and not CONFIG[content]["isbuilding"] and "issetting" not in CONFIG[content]:
        all_units.append(content)


@pytest.fixture(scope="module",params=all_buildings)
def building(request):
    building_name = request.param
    building = Building(building_name)
    return building

@pytest.fixture(scope="module",params=all_units)
def unit(request):
    unit_name = request.param
    unit = Unit(unit_name)
    return unit
    
def test_building_tick(unit, building):
    # ensure that we can't build units if the building isn't constructed
    if not building.is_constructed:
        # ensure that we cannot build a unit while building is being constructed
        assert building.build(unit.name) == False
        # ensure that building reports that it is constructed after appropriate time 
        building.tick(CONFIG[building.building_name]["time"] + 1)
        assert building.is_constructed == True
    
    # ensure units made from this building all build correctly.
    if(CONFIG[unit.name]["builtfrom"] == building.building_name):
        # there should be no residual production blocking unit construction
        assert len(building.current_production) == 0
        # building a unit should work at this point
        assert building.build(unit.name) == True
        # ensure singular tick updates time remaining
        assert building.current_production[0].build_time_remaining == CONFIG[unit.name]["time"]
        building.tick(1)
        assert building.current_production[0].build_time_remaining == CONFIG[unit.name]["time"] - 1
        # ensure it takes the appropriate amount of time to finish a unit thereafter
        building.tick(CONFIG[unit.name]["time"])
        # ensure unit is added to list of completed units when finished
        #assert building.completed_units[0].name == unit.name


if __name__ == '__main__':
    # test this file only
    pytest.main([__file__])