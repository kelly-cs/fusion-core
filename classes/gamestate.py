from base import Base


class GameState:
    def __init__(self, race, maxticks):
        # this will contain base objects, which contain workers. Income is based on amt of workers at a given base (it changes based on saturation)

        self.units = []  # all owned units/buildings/techs.
        self.mins = 50
        self.gas = 0
        # all logic about when we can build things should be handled here, and not in the children.
        self.usedSupply = 12  # default
        self.supply = 15  # default
        self.raceType = race
        self.startingWorkers = 12
        # allowed transitions between minerals/gas. will increase overhead as this rises.
        self.allowedTransitions = 6
        # how long will the simulation be allowed to go for? Each tick = 1 second ingame
        self.maxTicks = maxticks
        self.possibleActions = ["worker", "supply", "build",
                                "transferToGas", "transferToMins", "transferToBase", "chronoboost"]
        # we are assuming that all queens will be used to inject always, and that all orbitals will always make MULEs.
        # side tip - mules can mine at the same time an SCV is, so it doesn't mess with calculations.
        self.bases = [Base(self.startingWorkers, self.raceType, "normal", "normal", 2, false))]  # initialize first base.

    # progresses time by 1 unit
    # do this AFTER Collecting all necessary information for the current game tick, income, production etc
    def tick():
        for base in self.bases:
            base.tick()

    def getIncomeThisTick():
        incomeThisTick=0
        for base in self.bases:  # check each base for income
            incomeThisTick += base.getIncome()
        return incomeThisTick

    # we will explore all possible actions at this exact game tick. Do this before each tick to get every possibility.
    def attemptAction():
        for action in self.possibileActions:
            if(action == "worker"):
                attemptWorker(self.bases)


# takes a list of bases, and tries each one to see if we can make a worker there
    def canBuildWorker(bases):
        availableSupply=self.supply - self.usedSupply

        if(self.raceType == "z"):
            for base in bases:
                if(availableSupply >= 1 and base.currentlarva >= 1 and self.mins >= 50):
                    return true
        else:
            for base in bases:
                if(availableSupply >= 1 and len(base.currentWorkerProduction) == 0 and self.mins >= 50):
                    return true

    def canBuildSupply(bases)
        if(self.raceType == "z"):
            for base in bases:
                if(base.currentlarva >= 1 and self.mins >= 100):
                    return true
        else:
            if(self.mins >= 100):
                return true

    def canExpand()
        if(self.raceType == "z"):
            if(self.mins >= 300):
                return true
        else:
            if(self.mins >= 400):
                return true

    def canTransition()
        if(self.allowedTransitions > 0):
            return true
        else:
            return false

    def canBuildUnit(unit):
        availableSupply=self.supply - self.usedSupply
        minCost=50  # lookup from config, given unit name
        gasCost=0  # lookup from config, given unit name
        supplyCost=1  # lookup from config, given unit name
        if(hasTechFor(unit)):
            if(self.raceType == "z"):
                for base in self.bases:
                    if(base.currentlarva >= 1 and self.mins >= minCost and availableSupply >= supplyCost)
                        return true
        else:

    def hasTechFor(unit):
        # refer to config
        
        return true
