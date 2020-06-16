from unit import Unit


class Base:
    def __init__(self, startingworkers, race, mineraltype, gastype, geysers, underconstruction):
        # ALL WORKERS ARE SENT TO MINERALS BY DEFAULT, until a transfer order is made.
        # this is only for the 1st starting base.
        self.mineraltype = mineraltype  # can be "normal" or "rich"
        self.gasType = gastype  # can be "normal" or "rich"
        self.amtGeysers = geysers  # amount of gas geysers
        # how many workers are mining minerals here actively
        self.workersOnMinerals = startingworkers
        self.builtGeysers = 0  # amt of built geysers
        # array containing amt of workers at each geyser. 0 and 1 index can each have workers.
        self.geysers = [0, 0]
        self.isUnderConstruction = underconstruction  # true or false
        self.constructionTime = 71  # amt of time to build a base
        self.constructionTimeRemaining = 0  # amt of time remaining to construct this base
        self.timeToBuildWorker = 12  # default
        # "z, t, or p" to represent zerg, terran, or protoss.
        self.raceType = race
        self.energyRegenRate = 0.7875  # every second, add this to energy.
        self.energy = 0
        self.maxenergy = 200

        # other stuff
        # about how long it takes to transfer workers from 1 base to another
        self.timetoTransferBetweenBases = 15
        # this is a list that will just contain timers represnting workers [4, 11, 15]
        self.workersBeingTransferredBetweenBases = []
        # about how long it takes to transfer workers from minerals to gas, and vice versa
        self.timetoTransferMinsToGas = 3
        # this is a list that will just contain timers represnting workers [4, 11, 15]
        self.workersBeingTransferredFromMinsToGas = []
        self.workersBeingTransferredFromGasToMins = []

        # ZERG
        if(self.raceType="z"):
            self.currentlarva = 3  # start the game with 3 active.
            self.larvemax = 3  # max that can produce normally (via larvatimer)
            # max that can exist (with the help of a queen)
            self.larvainjectmax = 19
            # this is how long it takes to make a larvae, when below larvamax.
            self.larvatimer = 11
            # this is the current time before making another larva.
            self.currentLarvaTimer = 0
            # this is 4 in HotS and WoL, but I don't care. This is how much a queen adds when injecting.
            self.injectAmt = 3

            self.isInjected = 0  # 0 or 1.
            # this is how long it takes for an inject to procuce injectAmt of larva here.
            self.injectTime = 40
            # this is how long is remaining to produce injectAmt of larva, but only if isInjected is active (1)
            self.injectTimeRemaining = 0
            # array containing all active non-worker units being made
            self.zergUnitsProducing = []

        # TERRAN
        if(self.raceType="t"):

            self.isOrbital = false
            self.isTurningIntoOrbital = 0
            self.orbitalConstructionTime = 25
            self.orbitalConstructionTimeRemaining = 0

        # PROTOSS
        if(self.raceType="p"):
            self.energy = 50  # starting energy for protoss nexus
            self.chronoCost = 50  # cost for chrono boost
            self.isChronoBoosted = false  # is this structure chrono boosted?

        # array containing a timer on how long the worker will take to be done.
        self.currentWorkerProduction = []
        self.tick = 0  # amt of elapsed game time since this base was made

        try:
            if(self.isUnderConstruction)
            self.constructionTimeRemaining = self.constructionTime
        except:
            print(
                "Something happened when initializing UnderConstruction for Base: " + str(e))

    # updates 1 game second for everything in this object

    def tick(self):

        # ZERG
        for x in range(len(self.zergUnitsProducing)):
            if(self.zergUnitsProducing[x].buildTimeRemaining > 0):
                self.zergUnitsProducing[x].tick()
            else:

                del self.zergUnitsProducing[x]
                if(x > 0):
                    x = - 1  # this prevents it from messing up the index we're at

        # TERRAN

        # PROTOSS

        # OTHER
        if(self.raceType="p" or (self.raceType="t" and self.isOrbital)):
            if(self.energy < self.maxenergy):
                self.energy += self.energyRegenRate

    # returns an array [minerals, gas] for all income gained this tick. Should be ran before "tick" for accurate income.
    # first 2-3 ticks are never offering income.
    def getIncomeThisTick(self):
        if(self.tick < 3):
            return [0, 0]

        mineralincome = 0
        gasincome = 0

        if(self.mineraltype == "normal"):
            if(workersOnMinerals <= 16):
                mineralincome = workersOnMinerals * 0.958
            elif(workersOnMinerals == 17):
                mineralincome = workersOnMinerals * 0.916
            elif(workersOnMinerals >= 18):
                mineralincome = workersOnMinerals * 0.819
        elif(self.mineraltype == "rich"):
            if(workersOnMinerals <= 12):
                mineralincome = workersOnMinerals * 1.375
            elif(workersOnMinerals >= 13 and workersOnMinerals < 18):
                mineralincome = workersOnMinerals * 1.22
            elif(workersOnMinerals >= 18):
                mineralincome = workersOnMinerals * 1.111

        if(geysers[0] <= 2):
            gasincome += geysers[0] * 1
        elif(geysers[0] == 3):
            gasincome += 2.666

        if(geysers[1] <= 2):
            gasincome += geysers[1] * 1
        elif(geysers[1] == 3):
            gasincome += 2.666

        income = [mineralincome, gasincome]
        return income  # return as array

    # tell this base to make a worker - assumes that money is already spent by parent.
    # returns true if action succeeded/was possible
    # returns false if action failed/was not possible
    def makeWorker(self):
        # build as many workers as you want, if larvae exist.
        if(self.raceType="z" and self.currentlarva > 0):
            self.currentlarva -= 1
            self.currentWorkerProduction.append(self.timeToBuildWorker)
            return true
        # only 1 worker can be built at a time
        elif((self.raceType="p" or self.raceType="t") and len(self.currentlyBuildingWorker) == 0):
            self.currentWorkerProduction.append(self.timeToBuildWorker)
            return true
        else:
            return false
