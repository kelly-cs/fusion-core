class Unit:
    def __init__(self, unitname, underconstruction):
        self.name = unitname  # see config
        self.underConstruction = underconstruction  # true or false
        self.timeToConstruct = 12  # default for workers
        self.timeRemaining = self.timeToConstruct
        # we will consult a config file for all other unit names/times later
