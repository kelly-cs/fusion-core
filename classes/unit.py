"""Units are created using this class, and they will be placed in an appropriate Building class to construct."""
# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

from . import settings


class Unit:
    def __init__(self, unitname):
        # This will rely on a config being preloaded into GameState - in order to
        # prevent reloading the config over and over every time a unit is made.
        # maybe be concerned about this
        # https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance

        self.name = unitname
        self.mincost = settings.CONFIG[unitname]["mincost"]
        self.gascost = settings.CONFIG[unitname]["gascost"]
        self.time_to_construct = settings.CONFIG[unitname]["time"]
        self.build_time_remaining = self.time_to_construct
        self.supply = settings.CONFIG[unitname]["supply"]
        # for units that produce other units.. pretty much only the carrier? We'll need some special logic for this
        self.current_production = []
        self.is_constructed = False
        self.chronoboost_speed = settings.CONFIG["chronoboost"]["speedboost"]

    def tick(self):
        if(self.build_time_remaining > 0):
            self.build_time_remaining -= 1
        else:
            self.is_constructed = True

    def chronoboost_tick(self):
        if(self.build_time_remaining > 0):
            self.build_time_remaining -= self.chronoboost_speed
        else:
            self.is_constructed = True
