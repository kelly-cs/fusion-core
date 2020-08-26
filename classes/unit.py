"""Units are created using this class, and they will be placed in an appropriate Building class to construct."""
# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

from classes.settings import CONFIG
from classes.settings import LOG

# Unit does not keep track of whether it is chronoboosted, only if it should tick as if it is chronoboosted.


class Unit:
    def __init__(self, unitname):
        self.name = unitname
        self.mincost = CONFIG[unitname]["mincost"]
        self.gascost = CONFIG[unitname]["gascost"]
        self.time_to_construct = CONFIG[unitname]["time"]
        self.build_time_remaining = self.time_to_construct
        self.supply = CONFIG[unitname]["supply"]
        # for units that produce other units/buildings, like workers! and carriers?
        self.current_production = []
        self.is_constructed = False
        self.chronoboost_speed = CONFIG["chronoboost"]["speedboost"]
        self.completed_units = []
        self.worker_travel_time = 3 # only used for workers

    def tick(self):
        if(self.build_time_remaining > 0):
            self.build_time_remaining -= 1
        else:
            self.is_constructed = True
        
        if(self.is_constructed and self.current_production != []):
            if current_production[0].build_time_remaining > 0:
                current_production.build_time_remaining -= 1
            else:
                self.completed_units.append(current_production[0])


    def chronoboost_tick(self):
        if(self.build_time_remaining > 0):
            self.build_time_remaining -= self.chronoboost_speed
        else:
            self.is_constructed = True

    # we don't handle whether or not it is OK to morph this building here.
    # instead, we only handle if it is OK to morph (i.e., if there is free production to do so, if unit is built yet, etc)
    def morph(self, new_building):
        return False
