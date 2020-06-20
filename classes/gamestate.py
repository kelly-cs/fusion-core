from . import base
import os.path
import json
from . import settings

# The GameState represents a single game, not all possible simulations.
# The Simulation module will create new GameStates when branching into different


class GameState:
    def __init__(self, race="z", maxticks=1000, currentTick=0, goalUnits=[], _currentTarget=None, currentUnits=[], _currentProductionBuildings=[], _currentTechBuildings=[], _currentBuildingsInConstruction=[], _minerals=0, _gas=0, _currentBases=[]):

        # print(self.config["marine"])
        # this will contain base objects, which contain workers. Income is based on amt of workers at a given base (it changes based on saturation)
        # should be an array containing unit names/upgrade names as indicated in units.ini
        self.requiredTech = self.getAllRequiredTech(goalUnits) + goalUnits
        print(self.requiredTech)
        self.units = []  # all owned units/buildings/techs.
        self.mins = _minerals
        self.gas = _gas
        self.currentTarget = _currentTarget

        # all logic about when we can build things should be handled here, and not in the children.
        self.usedSupply = 12  # default
        self.supply = 15  # default
        self.raceType = race
        self.currentProductionBuildings = _currentProductionBuildings
        self.currentTechBuildings = _currentTechBuildings
        self.currentBuildingsInConstruction = _currentBuildingsInConstruction
        self.startingWorkers = 12
        self.currentBuildOrder = []  # in format: [["unit",tickNum],["tech",tickNum]]
        # allowed transitions between minerals/gas. will increase overhead as this rises.
        self.allowedTransitions = 6
        # how long will the simulation be allowed to go for? Each tick = 1 second ingame
        self.tickNum = currentTick
        self.maxTicks = maxticks
        self.possibleActions = ["worker", "supply", "build", "geyser",
                                "transferToGas", "transferToMins", "transferToBase", "chronoboost", "wait"]
        # we are assuming that all queens will be used to inject always, and that all orbitals will always make MULEs.
        # side tip - mules can mine at the same time an SCV is, so it doesn't mess with calculations.
        # initialize first base.
        if(_currentBases == []):
            self.bases = [base.Base(self.startingWorkers, self.raceType,
                                    "normal", "normal", 2, False)]

        self.simulationResults = self.runSimulation()
        # print(self.getAllRequiredTech(["ultralisk", "ultralisk", "hydralisk", "zergling"]))

    # We start from 2 p
    def runSimulation(self):
        potential_orders = []
        while self.tickNum < self.maxTicks:  # while we are not at the time limit
            if(self.currentTarget == None):  # if there's not a target at this moment
                for action in self.possibleActions:  # branch here and try all possibilities
                    # append these possibilities to a build order
                    potential_orders.append([action, self.tickNum])
                    GameState(self.raceType, self.maxTicks,  # make a new object branching into this area of possibiltiies
                              self.tickNum, self.requiredTech, action, self.units,)
            else:
                self.attemptAction(self.currentTarget)
            self.tick()
            self.tickNum += 1

        return potential_orders
        # progresses time by 1 unit
        # do this AFTER Collecting all necessary information for the current game tick, income, production etc

    def tick(self):
        print("Tick: ", self.tickNum)
        income = self.getIncomeThisTick()
        print("Income: ", income)
        print("Minerals: ", self.mins)
        print("Gas: ", self.gas)
        self.mins += income[0]  # mins
        self.gas += income[1]  # gas
        for base in self.bases:
            # i had to rename this because it was clashing somehow with the "tick" function in this file. Will need to look into..
            base.tickUp()
        self.tickNum += 1

    # returns a list [ minerals, gas ]
    def getIncomeThisTick(self):
        incomeThisTick = [0, 0]
        for base in self.bases:  # check each base for income
            # [ minerals, gas ]
            incomeThisTick[0] += base.getIncomeThisTick()[0]
            # we'll pare this down later because this is stupid
            incomeThisTick[1] += base.getIncomeThisTick()[1]
        return incomeThisTick  # as a list [ mins, gas ]

    # we will explore all possible actions at this exact game tick. Do this before each tick to get every possibility.
    def attemptAction(self):
        for action in self.possibileActions:
            if(action == "worker"):
                if(canBuildWorker(self.bases)):
                    print("You can build a worker")
            elif(action == "supply"):
                if(canBuildSupply(self.bases)):
                    print("You can build supply!")
            elif(action == "build"):
                pass
                # takes a list of bases, and tries each one to see if we can make a worker there

    def canBuildWorker(self, bases):
        availableSupply = self.supply - self.usedSupply

        if(self.raceType == "z"):
            for base in bases:
                if(availableSupply >= 1 and base.currentlarva >= 1 and self.mins >= 50):
                    return True
        else:
            for base in bases:
                if(availableSupply >= 1 and len(base.currentWorkerProduction) == 0 and self.mins >= 50):
                    return True

    def canBuildSupply(self, bases):
        if(self.raceType == "z"):
            for base in bases:
                if(base.currentlarva >= 1 and self.mins >= 100):
                    return True
        else:
            if(self.mins >= 100):
                return True

    def canExpand(self):
        if(self.raceType == "z"):
            if(self.mins >= 300):
                return True
        else:
            if(self.mins >= 400):
                return True

    def canTransition(self):
        if(self.allowedTransitions > 0):
            return True
        else:
            return False

    def canBuildUnit(self, unit):
        availableSupply = self.supply - self.usedSupply
        minCost = 50  # lookup from config, given unit name
        gasCost = 0  # lookup from config, given unit name
        supplyCost = 1  # lookup from config, given unit name
        if(self.hasTechFor(unit)):
            if(self.raceType == "z"):
                for base in self.bases:
                    if(base.currentlarva >= 1 and self.mins >= minCost and availableSupply >= supplyCost):
                        return True
        else:
            pass

    def buildUnit(self, unit):
        return None

    def buildSupply(self):
        return None

    def hasTechFor(self, unit):
        # refer to config
        requiredtech = self.getAllRequiredTech(unit)

        for each in requiredtech:
            if each not in self.units:  # if there is still a tech to be made
                return False
        return True

    # takes a list of strings representing unit names to figure out what tech we need
    # [ "marine", "firebat" ]
    # we could put a failsafe in here to check for race type, but I'd have to go dump it in
    # the CONFIG file. I'll get around to it.
    def getAllRequiredTech(self, composition):
        requiredtech = []  # return a list of all required items, using the config file for help
        for unitname in composition:  # for all things you want to make
            if unitname in settings.CONFIG:  # if these things are things you can actually make
                # if there's any requirements
                if len(settings.CONFIG[unitname]["requires"]) > 0:
                    # check each requirement for that unit
                    for each_requirement in settings.CONFIG[unitname]["requires"]:
                        if each_requirement not in requiredtech:
                            # print(each_requirement)
                            requiredtech.append(each_requirement)
                            # if there's more nested requirements
                            if(len(settings.CONFIG[each_requirement]["requires"]) > 0):
                                requiredtech.extend(  # let's just call this function again
                                    self.getAllRequiredTech([each_requirement]))

        # this gets rid of duplicates from nested tech tree because I was lazy
        # this will cause issues later when we have units that morph from other units
        # (i.e. banelings). I can probably just fix this after the fact by requiring
        # the zerglings to be produced to be at least the same as the expected baneling count,
        # or the amount of templars to be at least double the amount of expected archons.
        return list(dict.fromkeys(requiredtech))

    def remainingTechToBuild(self):
        tech = self.requiredTech
        for requirements in tech:
            if requirements in self.units:
                tech.remove(requirements)
        return tech

    def attemptAction(self, action):
        actionSuccess = False
        # if you're trying to see if you can build a worker
        if(action == "worker" and self.canBuildWorker(self.bases)):
            for base in self.bases:  # tell all bases to make a worker
                base.makeWorker()
                actionSuccess = True
        elif(action == "supply" and self.canBuildSupply(self.bases)):
            # temporarily take 1 worker out of the mining pool to build, for duration of building + 5-10 seconds (if t or p)
            # otherwise, just use a larva. buildSupply function will handle this.
            self.buildSupply()
            actionSuccess = True
        # if the target in fact needs to be built
        elif(action == "build"):
            for each in self.remainingTechToBuild():  # check all things we can make
                # if we are able to build it now, do so.
                if(self.canBuildUnit(each)):
                    self.buildUnit(each)
                    actionSuccess = True
        elif(action == "transferToGas"):
            for base in self.bases:
                # if the geysers aren't all occupied
                if(base.builtGeysers > 0 and (base.geysers[0] < 3 or base.geysers[1] < 3)):
                    base.transferMinsToGas()
                    actionSuccess = True
                    break  # we only want to do one at a time.
        elif(action == "transferToMins"):
            for base in self.bases:
                # if there is at least 1 worker in a geyser
                if(base.builtGeysers > 0 and (base.geysers[0] > 0 or base.geysers[1] > 0)):
                    base.transferGasToMins()
                    actionSuccess = True
                    break  # we only want to do one at a time.
