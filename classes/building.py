"""Handles building construction AND unit production."""
# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library

# third party library

# local
from classes.settings import CONFIG
from classes.settings import LOG
from classes.unit import Unit
# "spawningpool": {"istech":0,"isbuilding":1,"supply": 0, "mincost": 200,"gascost": 0,"time": 46,"requires": [],"builtfrom": "worker"},


class Building():
    # by default buildings start under construction with values from units.ini
    def __init__(self, building_name):
        self.building_name = building_name
        #self.mincost = CONFIG[self.building_name]["mincost"]
        #self.gascost = CONFIG[self.building_name]["gascost"]
        self.time_to_build = CONFIG[self.building_name]["time"]
        self.build_time_remaining = self.time_to_build
        # 1 in vast majority of cases, but reactors make this complicated
        self.production_throughput = CONFIG[self.building_name]["throughput"]
        self.current_production = []
        self.is_constructed = False
        self.is_chronoboosted = False
        self.chronoboost_time = CONFIG["chronoboost"]["time"]
        self.chronoboost_remaining = 0
        self.completed_units = []
        # the design pattern we will use for producing things out of buildings is to:
        # check the unit name in CONFIG and see what it is built from (and ensure requirements are met)
        # query all appropriate production buildings with same name as one that is produced from and see if they have free production
        # if current_production == None, then the unit can be produced out of this building, and the building will handle it thereafter.

    # passing in currentunits is required, as it serves as a reference for completed units to be output to - we don't want to store them in Building forever.
    def tick(self, duration=1):
        if duration > 0:
            if self.build_time_remaining > 0:
                self.build_time_remaining -= 1
            else:
                self.is_constructed = True

            if self.current_production != []:
                if self.is_chronoboosted:
                    for units in self.current_production:  # handles instances where multiple units can be produced, really only including buildings with reactors
                        if units.build_time_remaining > 0:
                            units.chronoboost_tick()
                        else:
                            units.is_constructed = True
                            self.completed_units.append(units)
                            self.current_production = []
                else:
                    for units in self.current_production:  # handles instances where multiple units can be produced, really only including buildings with reactors
                        if units.build_time_remaining > 0:
                            units.tick()
                        else:
                            units.is_constructed = True
                            self.completed_units.append(units)
                            self.current_production = []

            if self.chronoboost_remaining <= 0:
                self.is_chronoboosted = False
            else:
                self.chronoboost_remaining -= 1

            self.tick(duration - 1)
        return True

    # this will build a unit in this building, but it will NOT handle the logic for:
    # whether or not enough supply exists for the unit to be built
    # whether or not other tech has been created yet
    # as these things are meant to be handled by player, gamestate, or simulation, and not managed directly by these classes.
    # however, this class will still ensure that it is the proper building to produce the unit from.

    def build(self, unitname):
        if(self.is_constructed):
            if self.current_production == []:  # if we are not building something else
                # if the unit is meant to be built from this building
                if unitname in CONFIG and CONFIG[unitname]["builtfrom"] == self.building_name:
                    self.current_production.append(
                        Unit(unitname))  # create a new unit and build it from this structure
                    return True
        return False

    # we don't handle whether or not it is OK to morph this building here.
    # instead, we only handle if it is OK to morph (i.e., if there is free production to do so)
    def morph(self, new_building):
        return False
