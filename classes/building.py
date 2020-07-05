# standard library

# third party library

# local
from classes.player import Race
from classes import settings

# "spawningpool": {"istech":0,"isbuilding":1,"supply": 0, "mincost": 200,"gascost": 0,"time": 46,"requires": [],"builtfrom": "worker"},


class Building():
    def __init__(self, building_name):
        self.building_name = building_name
        self.istech = settings.CONFIG[self.building_name]["istech"]
        self.mincost = settings.CONFIG[self.building_name]["mincost"]
        self.gascost = settings.CONFIG[self.building_name]["gascost"]
        self.time_to_build = settings.CONFIG[self.building_name]["time"]
        self.build_time_remaining = self.time_to_build
        self.current_production = None

    def tick():
        if(self.build_time_remaining > 0):
            self.build_time_remaining -= 1
        else:
            self.underConstruction = false
