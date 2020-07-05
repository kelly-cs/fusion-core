import json
from . import settings


class Unit:
    def __init__(self, unitname):
        # This will rely on a config being preloaded into GameState - in order to
        # prevent reloading the config over and over every time a unit is made.
        # maybe be concerned about this
        # https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance

        self.name = unitname
        self.underConstruction = underconstruction
        self.mincost = settings.CONFIG[unitname]["mincost"]
        self.gascost = settings.CONFIG[unitname]["gascost"]
        self.time_to_construct = settings.CONFIG[unitname]["time"]
        self.build_time_remaining = self.timeToConstruct
        self.supply = settings.CONFIG[unitname]["supply"]
        self.is_completed = False
        # for units that produce other units.. pretty much only the carrier? We'll need some special logic for this
        self.current_production = []

        # we'll use a config file for this later
        # we will consult a config file for all other unit names/times later

    def tick():
        if(self.build_time_remaining > 0):
            self.build_time_remaining -= 1
        else:
            self.underConstruction = false
