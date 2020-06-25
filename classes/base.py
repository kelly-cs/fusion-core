from . import unit
from . import gamestate
from . import settings


class Base():
    def __init__(self, startingworkers, race, mineraltype, gastype, geysers, underconstruction):
        # ALL WORKERS ARE SENT TO MINERALS BY DEFAULT, until a transfer order is made.
        # this is only for the 1st starting base.
        self.mineraltype = mineraltype  # can be "normal" or "rich"
        self.gasType = gastype  # can be "normal" or "rich"
        self.amtGeysers = geysers  # amount of gas geysers
        # how many workers are mining minerals here actively
        self.workersOnMinerals = startingworkers
        self.builtGeysers = 0  # amt of built geysers
        # array containing amt of workers at each geyser. 0 and 1 index can each have workers. (so, [2,1] to represent 2 on the first, 1 on the second)
        self.geysers = [0, 0]
        self.geysersUnderConstruction = [False, False]
        # time to build gas  = 21, can probably put into config
        self.geysersRemainingTime = [21, 21]
        self.isUnderConstruction = underconstruction  # true or false
        self.constructionTime = 71  # amt of time to build a base
        self.constructionTimeRemaining = 0  # amt of time remaining to construct this base
        self.timeToBuildWorker = settings.CONFIG["worker"]["time"]  # default
        self.tickNum = 0
        self.iscurrentlyResearching = False  # true/false
        self.currentResearch = "None"  # name of current research, from CONFIG/
        # time remaining of current research, reduce by 1 per tick
        self.currentResearchTime = 0
        # start time of current research, from CONFIG.
        self.currentResarchTimeRemaining = 0
        # "z, t, or p" to represent zerg, terran, or protoss.
        self.raceType = race
        self.energyRegenRate = 0.7875  # every second, add this to energy.
        self.energy = 0
        self.maxenergy = 200

        # other stuff
        # about how long it takes to transfer workers from 1 base to another
        self.timetoTransferBetweenBases = settings.CONFIG["timeToTransferWorkerseBetweenBases"]
        # this is a list that will just contain timers represnting workers [4, 11, 15]
        self.workersBeingTransferredToThisBase = []
        # about how long it takes to transfer workers from minerals to gas, and vice versa
        self.timeToTransferMinsToGas = settings.CONFIG["timeToTransferWorkersFromMinsToGas"]
        # this is a list that will just contain timers represnting workers [4, 11, 15]
        self.workersBeingTransferredFromMinsToGas = []
        self.workersBeingTransferredFromGasToMins = []
        # list containing timers for how long it takes to build a refinery/gas extractor. Generally about 2-3 seconds/ticks.
        self.workersBeingSentToBuildGas = []
        # generally how long it takes for a worker to move to and from building something (one way)
        self.workerTravelTimeToBuild = settings.CONFIG["timeForWorkersToBuild"]

        # ZERG
        if(self.raceType == "z"):
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
            self.isHatchery = True
            self.isLair = False
            self.isHive = False
            self.lairResearchTime = settings.CONFIG["lair"]["time"]
            self.hiveResearchTime = settings.CONFIG["hive"]["time"]
            self.burrowResearchTime = settings.CONFIG["burrow"]["time"]
            self.pneumatizedCarapaceResearchTime = settings.CONFIG["pneumatizedcarapace"]["time"]
        # TERRAN
        if(self.raceType == "t"):

            self.isOrbital = false
            self.isTurningIntoOrbital = 0
            self.orbitalConstructionTime = 25
            self.orbitalConstructionTimeRemaining = 0
            # this will be an array of timers, for occupied SCVs.
            self.workersCurrentlyBuilding = []

        # PROTOSS
        if(self.raceType == "p"):
            self.energy = 50  # starting energy for protoss nexus
            self.chronoCost = 50  # cost for chrono boost
            self.isChronoBoosted = false  # is this structure chrono boosted?
            self.workersCurrentlyBuilding = []
            # arbitrary - this will assume how long your probe is out of mining to build something.
        # array containing a timer on how long the worker will take to be done.
        self.currentWorkerProduction = []
        self.tick = 0  # amt of elapsed game time since this base was made

        try:
            if(self.isUnderConstruction):
                self.constructionTimeRemaining = self.constructionTime
        except:
            print(
                "Something happened when initializing UnderConstruction for Base: " + str(e))

        # let's make a marine and see what happens
        # self.testUnit = unit.Unit("ghost", True)

    # updates 1 game second for everything in this object

    def tickUp(self):
        self.subtractTimeRemaining()  # deal with all timers, workers, upgrade production

        # ZERG

        # TERRAN

        # PROTOSS

        # OTHER
        if(self.raceType == "p" or (self.raceType == "t" and self.isOrbital)):
            if(self.energy < self.maxenergy):
                self.energy += self.energyRegenRate

        self.tickNum += 1

    # returns an array [minerals, gas] for all income gained this tick. Should be ran before "tick" for accurate income.
    # first 5 ticks are never offering income.
    def getIncomeThisTick(self):
        if(self.tickNum < 5):
            return [0, 0]

        mineralincome = 0
        gasincome = 0

        if(self.mineraltype == "normal"):
            if(self.workersOnMinerals <= 16):
                mineralincome = self.workersOnMinerals * 0.958
            elif(self.workersOnMinerals == 17):
                mineralincome = self.workersOnMinerals * 0.916
            elif(self.workersOnMinerals >= 18):
                mineralincome = self.workersOnMinerals * 0.819
        elif(self.mineraltype == "rich"):
            if(self.workersOnMinerals <= 12):
                mineralincome = self.workersOnMinerals * 1.375
            elif(self.workersOnMinerals >= 13 and self.workersOnMinerals < 18):
                mineralincome = self.workersOnMinerals * 1.22
            elif(self.workersOnMinerals >= 18):
                mineralincome = self.workersOnMinerals * 1.111

        if(self.geysers[0] <= 2):
            gasincome += self.geysers[0] * 1
        elif(self.geysers[0] == 3):
            gasincome += 2.666

        if(self.geysers[1] <= 2):
            gasincome += self.geysers[1] * 1
        elif(self.geysers[1] == 3):
            gasincome += 2.666

        income = [mineralincome, gasincome]
        return income  # return as array

    # tell this base to make a worker - assumes that money is already spent by parent.
    # returns true if action succeeded/was possible
    # returns false if action failed/was not possible
    # Supply and resources are ignored, and instead handled by GameState.
    # Bases exclusively handle Workers - any other unit will be instead be processed in GameState.
    def makeWorker(self):
        # build as many workers as you want, if larvae exist.
        if(self.raceType == "z" and self.currentlarva > 0):
            self.currentlarva -= 1
            self.currentWorkerProduction.append(self.timeToBuildWorker)
            return True
        # only 1 worker can be built at a time
        elif((self.raceType == "p" or self.raceType == "t") and self.hasFreeProduction()):
            self.currentWorkerProduction.append(self.timeToBuildWorker)
            return True
        else:
            return False

    # run this function whenever making any non-worker unit.
    def useLarva(self):
        if(self.raceType == "z" and self.currentlarva > 0):
            self.currentlarva -= 1
            return True
        return False

    def getWorkers(self):
        return [self.workersOnMinerals, self.geysers[0], self.geysers[1]]

    def getProductionQueue(self):
        if(self.raceType == "z"):
            return[self.currentWorkerProduction]
        else:
            return[self.currentWorkerProduction]

    # This function will move 1 worker from minerals to Gas, putting them into the wait queue to move in.
    def transferMinsToGas(self):
        if(self.workersOnMinerals > 0):
            self.workersOnMinerals -= 1
            self.workersBeingTransferredFromMinsToGas.append(
                self.timeToTransferMinsToGas)
            return True
        return False

    # This function will move 1 worker from Gas to minerals
    def transferGasToMins(self):
        # always take from which geyser has 3 workers on it first - it affects gas income least.
        if(self.geysers[0] > 2):
            self.geysers[0] -= 1
            self.workersBeingTransferredFromGasToMins.append(
                self.timeToTransferMinsToGas)
            return True
        elif(self.geysers[1] > 2):
            self.geysers[1] -= 1
            self.workersBeingTransferredFromGasToMins.append(
                self.timeToTansferMinsToGas)
            return True
        elif(self.geysers[0] > 0):
            self.geysers[0] -= 1
            self.workersBeingTransferredFromGasToMins.append(
                self.timeToTansferMinsToGas)
            return True
        elif(self.geysers[1] > 0):
            self.geysers[1] -= 1
            self.workersBeingTransferredFromGasToMins.append(
                self.timeToTansferMinsToGas)
            return True
        return False

    # this will immediately remove a worker from this base.
    def transferWorkerOutOfBase(self):
        return None

    # this will add a worker to the "transferring to base" queue, which is about 10-15 seconds, in which case it will be sent to the mineral line.
    def transferWorkerIntoBase(self):
        return None

    # Can you build a worker right now?
    # T + P: Is there no workers/upgrades being built?
    # Z: Is there larvae + no upgrades being built?
    def hasFreeProduction(self):
        # research only matters if upgrading to a lair.
        if(self.raceType == "z" and self.currentlarva >= 1):
            return True
        elif(self.raceType == "t" and self.iscurrentlyResearching == False and self.isTurningIntoOrbital == False and self.currentWorkerProduction == []):
            return True
        elif(self.raceType == "p" and self.iscurrentlyResearching == False and self.isTurningIntoOrbital == False and self.currentWorkerProduction == []):
            return True
        else:
            return False

    def buildGeyser(self):
        # to try and stop from building more geysers than are available
        if(self.raceType == "z" and self.builtGeysers < 2 and len(self.workersBeingSentToBuildGas) < 2):
            self.workersOnMinerals -= 1  # use workers from the mineral line
            self.workersBeingSentToBuildGas.append(
                self.workerTravelTimeToBuild)  # add a worker to a queue to build the gas
            if(self.builtGeysers == 0):
                # this will trigger the countdown timer each tick
                self.geysersUnderConstruction[0] = True
                return True
            elif(self.builtGeysers == 1):
                # this will trigger the countdown timer each tick
                self.geysersUnderConstruction[1] = True
                return True
        return False

    # when a geyser completes, run this function
    # that is to say, when a timer reaches 0 in self.geyserRemainingTime, run this.
    # current limitation: does not handle when 2 geysers finish at the same time. not a huge deal but might be worth fixing later.
    def geyserComplete(self):
        if(self.raceType == "z"):
            if(self.builtGeysers == 0):
                self.builtGeysers += 1
                self.geysersUnderConstruction[0] = False
                return True
            elif(self.builtGeysers == 1):
                self.builtGeysers += 1
                self.geysersUnderConstruction[1] = False
                return True
        else:
            # if this is the first geyser for this base
            if(self.builtGeysers == 0):
                self.geysers[0] = 1  # add 1 worker to the first geyser
                self.builtGeysers += 1
                self.geysersUnderConstruction[0] = False
                return True
            # if this is the second geyser for this base
            elif(builtGeysers == 1):
                self.geysers[1] = 1  # add 1 worker to the second geyser.
                self.builtGeysers += 1
                self.geysersUnderConstruction[1] = False
                return True
            else:
                return False  # this shouldn't happen.

    def isGeyserCompleted(self):
        if(self.geysersUnderConstruction[0] == True and self.geysersRemainingTime[0] <= 0):
            return True
        elif(self.geysersUnderConstruction[1] == True and self.geysersRemainingTime[1] <= 0):
            return True
        return False

    # this will take all timers in this object and subtract them by 1 per tick.
    # It also will remove objects from the production queue if they are finished, and apply them to the base.
    def subtractTimeRemaining(self):
        if(self.geysersUnderConstruction[0]):
            self.geysersRemainingTime[0] -= 1
        if(self.geysersUnderConstruction[1]):
            self.geysersRemainingTime[1] -= 1
        if(self.isGeyserCompleted()):
            self.geyserComplete()
        for workers in self.workersBeingTransferredFromGasToMins:
            workers -= 1  # subtract 1 from their timer
        for workers in self.workersBeingTransferredFromMinsToGas:
            workers -= 1
        for workers in self.workersBeingTransferredToThisBase:
            workers -= 1
        for workers in self.workersBeingSentToBuildGas:
            if(workers <= 0):  # if the timer is over
                workers.pop(index)  # the first element will always be the
                workersBeingSentToBuildGas.append(
                    self.workerTravelTimeToBuild)  # about 5 seconds before you get to building
            workers -= 1
        index = 0
        for workers in self.currentWorkerProduction:
            if(workers <= 0):  # if the timer is over
                # the first element will always be the worker
                self.currentWorkerProduction.pop(index)
                workersBeingTransferredToThisBase.append(
                    self.timeToTransferMinsToGas)  # about 5 seconds before you factor in income
            workers -= 1
