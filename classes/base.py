# standard library

# third party library

# local
from classes.player import Race
from classes import settings
from classes.unit import Unit


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
        self.raceType = race
        self.energyRegenRate = 0.7875  # every second, add this to energy.
        self.energy = 50
        self.maxenergy = 200

        # about how long it takes to transfer workers from 1 base to another
        self.timetoTransferBetweenBases = settings.CONFIG["timeToTransferWorkerseBetweenBases"]
        # this is a list that will just contain timers representing workers [4, 11, 15]
        self.workersBeingTransferredToThisBase = []
        # about how long it takes to transfer workers from minerals to gas, and vice versa
        self.timeToTransferMinsToGas = settings.CONFIG["timeToTransferWorkersFromMinsToGas"]
        # this is a list that will just contain timers representing workers [4, 11, 15]
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
        # TERRAN
        if self.raceType == Race.TERRAN:
            self.isOrbital = False
            self.isTurningIntoOrbital = 0
            self.orbitalConstructionTime = settings.CONFIG["orbitalcommand"]["time"]
            self.orbitalConstructionTimeRemaining = self.orbitalConstructionTime

        # PROTOSS
        if self.raceType == Race.PROTOSS:
            # cost for chrono boost
            self.chronoCost = settings.CONFIG["chronoboost"]["energycost"]
            self.isChronoBoosted = False  # is this structure chrono boosted?

        # workers represented by Unit class here, but will be treated as ints for less memory usage afterward in workersOnMins and workersInGas, etc.
        self.currentWorkerProduction = []
        self.iscurrentlyResearching = False  # true/false
        self.current_research = None  # current research represented by Unit class

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

        for g in self.geysers:
            if g <= 2:
                gasincome += g
            else:
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
            self.currentWorkerProduction.append(Unit("worker"))
            return True
        # only 1 worker can be built at a time
        elif(self.raceType == Race.PROTOSS or self.raceType == Race.TERRAN) and self.hasFreeProduction():
            self.currentWorkerProduction.append(Unit("worker"))
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
        return self.workersOnMinerals, self.geysers

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
        for g in self.geysers:
            # always take from which geyser has 3 workers on it first - it affects gas income least.
            if g > 2:
                g -= 1
                self.workersBeingTransferredFromGasToMins.append(
                    self.timeToTransferMinsToGas)
                return True
            elif g > 0:
                g -= 1
                self.workersBeingTransferredFromGasToMins.append(
                    self.timeToTransferMinsToGas)
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
        if(self.raceType == Race.ZERG and self.builtGeysers < self.amtGeysers and len(self.workersBeingSentToBuildGas) < self.amtGeysers and not self.geysersUnderConstruction[self.builtGeysers]):
            self.geysersUnderConstruction[self.builtGeysers] = True
        return False

    # initiates the command to build a geyser. once travel time finishes, the geyser actually starts being constructed.
    def sendWorkerToBuildGeyser(self):
        if(self.workersOnMinerals > 0):
            self.workersOnMinerals -= 1
            self.workersBeingSentToBuildGas.append(
                self.timeToTransferMinsToGas)
            return True
        return False

    # current limitation: does not handle when 2 geysers finish at the same time. not a huge deal but might be worth fixing later.
    # (this is due to only 1 action being handled per tick)

    def geyserComplete(self):
        if self.raceType == Race.ZERG:  # does not get worker added automatically
            self.geysersUnderConstruction[self.builtGeysers] = False
            self.builtGeysers += 1
            return True
        else:
            # adds worker to the newest geyser
            self.geysersUnderConstruction[self.builtGeysers] = False
            self.geysers[self.builtGeysers] = 1
            self.builtGeysers += 1
            return True
        return False

    def isGeyserCompleted(self):
        for g in range(0, self.amtGeysers):
            if self.geysersUnderConstruction[g] == True and self.geysersRemainingTime[g] <= 0:
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
        for g in range(0, self.amtGeysers):
            if self.geysersUnderConstruction[g]:
                self.geysersRemainingTime[g] -= 1
        if(self.isGeyserCompleted()):
            self.geyserComplete()

        index = 0
        for workers in self.workersBeingTransferredFromGasToMins:
            if(workers <= 0):  # if the timer is over
                self.workersBeingTransferredFromGasToMins.pop(index)
                self.workersBeingSentToBuildGas.append(
                    self.workerTravelTimeToBuild)  # about 5 seconds before you get to building
            else:
                workers.tick()
                index += 1

        index = 0
        for workers in self.workersBeingSentToBuildGas:
            if(workers <= 0):  # if the timer is over
                self.workersBeingSentToBuildGas.pop(index)
                self.buildGeyser()
            else:
                workers.tick()
                index += 1

        index = 0
        for workers in self.workersBeingTransferredFromMinsToGas:
            if(workers <= 0):
                self.workersBeingTransferredFromMinsToGas.pop(index)
                self.addWorkerToCompletedGeyser()
            else:
                workers.tick()
                index += 1

        index = 0
        for workers in self.workersBeingTransferredToThisBase:
            if(workers <= 0):
                self.workersBeingTransferredToThisBase.pop(index)
                self.workersOnMinerals += 1
            else:
                workers.tick()
                index += 1

        index = 0
        for workers in self.workersBeingSentToBuildGas:
            if(workers <= 0):  # if the timer is over
                self.currentWorkerProduction.pop(index)
                self.workersBeingSentToBuildGas.append(
                    self.workerTravelTimeToBuild)  # about 5 seconds before you get to building
            else:
                workers.tick()
                index += 1

        index = 0
        for workers in self.currentWorkerProduction:
            if(workers.build_time_remaining <= 0):  # if the timer is over
                self.currentWorkerProduction.pop(index)
                self.workersBeingTransferredToThisBase.append(
                    self.timeToTransferMinsToGas)  # about 5 seconds before you factor in income
            else:
                workers.tick()
                index += 1

    def debug(self):
        return None

    def get_production(self):
        if self.current_research == None and len(self.currentWorkerProduction) <= 0:
            return None
        elif len(self.currentWorkerProduction) > 0:
            return {"worker": self.currentWorkerProduction[0].build_time_remaining}
        else:
            return {self.current_research.name: self.current_research.build_time_remaining}
