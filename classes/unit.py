import json
from . import settings


class Unit:
    def __init__(self, unitname, underconstruction):
        # This will rely on a config being preloaded into GameState - in order to
        # prevent reloading the config over and over every time a unit is made.
        # maybe be concerned about this
        # https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance

        try:
            if unitname in settings.CONFIG:
                self.name = unitname
                print("Worked")
            else:
                Exception("Incorrect Unit Name")
        except Exception as e:
            print("Unknown Unit Name: " + unitname + str(e))

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
