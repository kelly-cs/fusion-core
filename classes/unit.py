import json
import os.path


class Unit:
    def __init__(self, unitname, underconstruction):

        self.name = unitname  # see config
        self.underConstruction = underconstruction  # true or false
        self.timeToConstruct = 12  # default for workers
        self.buildTimeRemaining = self.timeToConstruct
        self.supply = 0  # we'll use a config file for this later
        # we will consult a config file for all other unit names/times later

    def tick():
        if(self.buildTimeRemaining > 0):
            self.buildTimeRemaining -= 1
        else:
            self.underConstruction = false
