class GameState:
    def __init__(self, race, maxticks):
        # this will contain base objects, which contain workers. Income is based on amt of workers at a given base (it changes based on saturation)

        self.units = []  # all owned units/buildings/techs.
        self.mins = 50
        self.gas = 0
        self.raceType = race
        self.startingWorkers = 12
        # how long will the simulation be allowed to go for? Each tick = 1 second ingame
        self.maxTicks = maxticks
        self.possibleActions = ["worker", "supply", "build",
                                "transferToGas", "transferToMins", "transferToBase", "chronoboost"]
        # we are assuming that all queens will be used to inject always, and that all orbitals will always make MULEs.
        # side tip - mules can mine at the same time an SCV is, so it doesn't mess with calculations.
        self.bases = [Base(self.startingWorkers, self.raceType, "normal", "normal", 2, false))]  # initialize first base.

    def getIncomeThisTick():
        incomeThisTick=0
        for base in self.bases:  # check each base for workers
            incomeThisTick += base.getIncome()
        return incomeThisTick
