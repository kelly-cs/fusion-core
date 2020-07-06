# standard library

# third party library

# local
from classes.player import Race
from classes import settings


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
        self.geysers = [0] * self.amtGeysers
        self.geysersUnderConstruction = [False] * self.amtGeysers
        # time to build gas  = 21, can probably put into config
        self.geysersRemainingTime = [
            settings.CONFIG["extractor"]["time"]] * self.amtGeysers
        # true or false, important for initial base vs expansions
        self.isUnderConstruction = underconstruction
        # amt of time to build a base
        self.constructionTime = settings.CONFIG["hatchery"]["time"]
        # amt of time remaining to construct this base
        self.constructionTimeRemaining = settings.CONFIG["hatchery"]["time"]
        self.timeToBuildWorker = settings.CONFIG["worker"]["time"]  # default
        self.tickNum = 0  # amt of elapsed game time since this base was made
        self.iscurrentlyResearching = False  # true/false
        self.current_research = None  # name of current research, from CONFIG/
        # time remaining of current research, reduce by 1 per tick
        # start time of current research, from CONFIG.
        self.current_research_time_remaining = 0
        # "z, t, or p" to represent zerg, terran, or protoss.
        self.raceType = race
        self.energyRegenRate = 0.7875  # every second, add this to energy.
        self.energy = 50
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
        if self.raceType == Race.ZERG:
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
        if self.raceType == Race.TERRAN:
            self.isOrbital = False
            self.isTurningIntoOrbital = 0
            self.orbitalConstructionTime = 25
            self.orbitalConstructionTimeRemaining = 0
            # this will be an array of timers, for occupied SCVs.
            self.workersCurrentlyBuilding = []

        # PROTOSS
        if self.raceType == Race.PROTOSS:
            # starting energy for protoss nexus
            self.energy = settings.CONFIG["chronoboost"]["co"]
            # cost for chrono boost
            self.chronoCost = settings.CONFIG["chronoboost"]["energycost"]
            self.isChronoBoosted = False  # is this structure chrono boosted?
            self.workersCurrentlyBuilding = []
            # arbitrary - this will assume how long your probe is out of mining to build something.
        # array containing a timer on how long the worker will take to be done.
        self.currentWorkerProduction = []
        if self.isUnderConstruction:
            self.constructionTimeRemaining = self.constructionTime

        # let's make a marine and see what happens
        # self.testUnit = unit.Unit("ghost", True)

    # updates 1 game second for everything in this object

    def tickUp(self):
        self.subtractTimeRemaining()  # deal with all timers, workers, upgrade production

        # ZERG

        # TERRAN

        # PROTOSS

        # OTHER
        if(self.raceType == Race.PROTOSS or (self.raceType == Race.TERRAN and self.isOrbital)):
            if(self.energy < self.maxenergy):
                self.energy += self.energyRegenRate

        self.tickNum += 1
        return True

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
        if self.raceType == Race.ZERG and self.currentlarva > 0:
            self.currentlarva -= 1
            self.currentWorkerProduction.append(self.timeToBuildWorker)
            return True
        # only 1 worker can be built at a time
        elif(self.raceType == Race.PROTOSS or self.raceType == Race.TERRAN) and self.hasFreeProduction():
            self.currentWorkerProduction.append(self.timeToBuildWorker)
            return True
        else:
            return False

    # run this function whenever making any non-worker unit.
    def useLarva(self):
        if(self.raceType == Race.ZERG and self.currentlarva > 0):
            self.currentlarva -= 1
            return True
        return False

    def getWorkers(self):
        return [self.workersOnMinerals, self.geysers[0], self.geysers[1]]

    def getProductionQueue(self):
        if(self.raceType == Race.ZERG):
            return[self.currentWorkerProduction, self.zergUnitsProducing]
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

    # this will immediately remove a worker from this base, from the mineral line by default.
    def transferWorkerOutOfBase(self, newbase):
        if(self.workersOnMinerals > 0):
            self.workersOnMinerals -= 1
            newbase.transferWorkerIntoBase()

        return None

    # this will add a worker to the "transferring to base" queue, which is about 10-15 seconds, in which case it will be sent to the mineral line.
    def transferWorkerIntoBase(self):
        self.workersBeingTransferredToThisBase.append(
            self.timetoTransferBetweenBases)
        return None

    # Can you build a worker right now?
    # T + P: Is there no workers/upgrades being built?
    # Z: Is there larvae + no upgrades being built?
    def hasFreeProduction(self):
        # research only matters if upgrading to a lair.
        if(self.raceType == Race.ZERG and self.currentlarva >= 1):
            return True
        elif(self.raceType == Race.TERRAN and self.iscurrentlyResearching == False and self.isTurningIntoOrbital == False and self.currentWorkerProduction == []):
            return True
        elif(self.raceType == Race.PROTOSS and self.iscurrentlyResearching == False and self.isTurningIntoOrbital == False and self.currentWorkerProduction == []):
            return True
        else:
            return False

    def buildGeyser(self):
        # to try and stop from building more geysers than are available
        if(self.raceType == Race.ZERG and self.builtGeysers < 2 and len(self.workersBeingSentToBuildGas) < 2 and (not self.geysersUnderConstruction[0] or not self.geysersUnderConstruction[1])):
            if(self.builtGeysers == 0):
                # this will trigger the countdown timer each tick
                self.geysersUnderConstruction[0] = True
                return True
            elif(self.builtGeysers == 1):
                # this will trigger the countdown timer each tick
                self.geysersUnderConstruction[1] = True
                return True
        return False

    # initiates the command to build a geyser. once travel time finishes, the geyser actually starts being constructed.
    def sendWorkerToBuildGeyser(self):
        if(self.workersOnMinerals > 0):
            self.workersOnMinerals -= 1
            self.workersBeingSentToBuildGas.append(
                self.timeToTransferMinsToGas)
            return True
        return False

        # when a geyser completes, run this function
        # that is to say, when a timer reaches 0 in self.geyserRemainingTime, run this.
        # current limitation: does not handle when 2 geysers finish at the same time. not a huge deal but might be worth fixing later.

    def geyserComplete(self):
        if(self.raceType == Race.ZERG):
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
            elif(self.builtGeysers == 1):
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

    # assumes that a worker has already traveled long enough to reach the gas
    # adds the worker to the most efficient geyser available
    def addWorkerToCompletedGeyser(self):
        for i in range(0, self.builtGeysers):
            # add to the least saturated geysers first.
            if(self.geysersUnderConstruction[i] == False and self.geysers[i] < 2):
                self.geysers[i] += 1
                return True

        for i in range(0, self.builtGeysers):
            # add to the most saturated geysers only if there are no other options
            if(self.geysersUnderConstruction[i] == False and self.geysers[i] < 3):
                self.geysers[i] += 1
                return True

        return False  # if all geysers are occupied.

# this will take all timers in this object and subtract them by 1 per tick.
# It also will remove objects from the production queue if they are finished, and apply them to the base.
    def subtractTimeRemaining(self):
        if(self.geysersUnderConstruction[0]):
            self.geysersRemainingTime[0] -= 1
        if(self.geysersUnderConstruction[1]):
            self.geysersRemainingTime[1] -= 1
        if(self.isGeyserCompleted()):
            self.geyserComplete()

        index = 0
        for workers in self.workersBeingTransferredFromGasToMins:
            if(workers <= 0):  # if the timer is over
                self.workersBeingTransferredFromGasToMins.pop(index)
                self.workersBeingSentToBuildGas.append(
                    self.workerTravelTimeToBuild)  # about 5 seconds before you get to building
            else:
                workers -= 1
                index += 1

        index = 0
        for workers in self.workersBeingSentToBuildGas:
            if(workers <= 0):  # if the timer is over
                self.workersBeingSentToBuildGas.pop(index)
                self.buildGeyser()
            else:
                workers -= 1
                index += 1

        index = 0
        for workers in self.workersBeingTransferredFromMinsToGas:
            if(workers <= 0):
                self.workersBeingTransferredFromMinsToGas.pop(index)
                self.addWorkerToCompletedGeyser()
            else:
                workers -= 1
                index += 1

        index = 0
        for workers in self.workersBeingTransferredToThisBase:
            if(workers <= 0):
                self.workersBeingTransferredToThisBase.pop(index)
                self.workersOnMinerals += 1
            else:
                workers -= 1
                workers -= 1

        index = 0
        for workers in self.workersBeingSentToBuildGas:
            if(workers <= 0):  # if the timer is over
                self.currentWorkerProduction.pop(index)
                self.workersBeingSentToBuildGas.append(
                    self.workerTravelTimeToBuild)  # about 5 seconds before you get to building
            else:
                workers -= 1
                index += 1

        index = 0
        for workers in self.currentWorkerProduction:
            if(workers <= 0):  # if the timer is over
                self.currentWorkerProduction.pop(index)
                self.workersBeingTransferredToThisBase.append(
                    self.timeToTransferMinsToGas)  # about 5 seconds before you factor in income
            else:
                workers -= 1
                index += 1

    def debug(self):
        return None
