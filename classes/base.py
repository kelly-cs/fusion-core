# standard library

# third party library

# local
from classes.player import Race
from classes.settings import CONFIG
from classes.settings import LOG
from classes.unit import Unit
from classes.player import Race


class Base():
    def __init__(self, startingworkers, race, mineraltype, gastype, geysers, underconstruction, firstbase):
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
            CONFIG["extractor"]["time"]] * self.amtGeysers
        # true or false, important for initial base vs expansions
        self.isUnderConstruction = underconstruction
        # amt of time to build a base
        self.constructionTime = CONFIG["hatchery"]["time"]
        # amt of time remaining to construct this base
        self.constructionTimeRemaining = CONFIG["hatchery"]["time"]
        self.timeToBuildWorker = CONFIG["worker"]["time"]  # default
        self.tickNum = 0  # amt of elapsed game time since this base was made
        self.raceType = race
        self.energyRegenRate = 0.7875  # every second, add this to energy.
        self.energy = 50
        self.maxenergy = 200
        # used primarily for hatcheries to know how many larvae start out
        self.firstbase = firstbase

        # about how long it takes to transfer workers from 1 base to another
        self.timetoTransferBetweenBases = CONFIG["timeToTransferWorkerseBetweenBases"]["time"]
        # this is a list that will just contain timers representing workers [4, 11, 15]
        self.workersBeingTransferredToThisBase = []
        # about how long it takes to transfer workers from minerals to gas, and vice versa
        self.timeToTransferMinsToGas = CONFIG["timeToTransferWorkersFromMinsToGas"]["time"]
        # this is a list that will just contain timers representing workers [4, 11, 15]
        self.workersBeingTransferredFromMinsToGas = []
        self.workersBeingTransferredFromGasToMins = []
        # list containing timers for how long it takes to build a refinery/gas extractor. Generally about 2-3 seconds/ticks.
        self.workersBeingSentToBuildGas = []
        # generally how long it takes for a worker to move to and from building something (one way)
        self.workerTravelTimeToBuild = CONFIG["timeForWorkersToBuild"]["time"]
        self.workersBeingSentToBuild = []

        # ZERG

        # start the game with 3 active - Only 1 when base is newly created (Thanks DEVIN)
        if self.firstbase:
            self.currentlarva = 3
        else:
            self.currentlarva = 1

        self.larvemax = 3  # max that can produce normally (via larvatimer)
        # max that can exist (with the help of a queen)
        self.larvainjectmax = 19
        # this is how long it takes to make a larvae, when below larvamax.
        self.larvatimer = 11
        # this is the current time before making another larva.
        self.currentLarvaTimer = self.larvatimer
        # this is 4 in HotS and WoL, but I don't care. This is how much a queen adds when injecting.
        self.injectAmt = 3
        self.has_queen = False
        self.queen_energy = 25
        self.queen_energy_max = 200
        self.queen_inject_energy_cost = 25
        self.isInjected = 0  # 0 or 1.
        # this is how long it takes for an inject to procuce injectAmt of larva here.
        self.injectTime = 40
        # this is how long is remaining to produce injectAmt of larva, but only if isInjected is active (1)
        self.injectTimeRemaining = 0
        self.isHatchery = True
        self.isLair = False
        self.isHive = False
    # TERRAN
        self.isOrbital = False
        self.isTurningIntoOrbital = 0
        self.orbitalConstructionTime = CONFIG["orbitalcommand"]["time"]
        self.orbitalConstructionTimeRemaining = self.orbitalConstructionTime

    # PROTOSS
        # cost for chrono boost
        self.chronoboost_cost = CONFIG["chronoboost"]["energycost"]
        self.is_chronoboosted = False  # is this structure chrono boosted?

        # only for zerg as they do not use normal buildings to produce units.
        self.currentArmyProduction = []
        # for zerg, indicates time until an overlord is completed. for terran/toss, indicates time until supply depot/pylon completes.
        self.currentSupplyProduction = []
        # workers represented by Unit class here, but will be treated as ints for less memory usage afterward in workersOnMins and workersInGas, etc.
        self.currentWorkerProduction = []

        # Player will ask Base for any positive changes in supply each tick.
        self.supply_to_add = 0
        # Player will ask Base for any newly completed units/buildings/tech each tick to add to ITS current_units list. Player does not care about workers.
        self.completed_units = []

        self.iscurrentlyResearching = False  # true/false
        self.current_research = None  # current research represented by Unit class

    # updates 1 game second for everything in this object
    def tickUp(self, duration):
        if duration > 0:
            self.subtractTimeRemaining()  # deal with all timers, workers, upgrade production

            # ZERG

            # TERRAN

            # PROTOSS

            # OTHER

            # supply building does not benefit from chronoboost in any race
            for supply in self.currentSupplyProduction:
                if supply.build_time_remaining > 0:
                    supply.tick()
                elif self.raceType == Race.ZERG:
                    self.completed_units.append(supply)
                    self.supply_to_add += CONFIG["overlord"]["providedsupply"]
                elif self.raceType == Race.TERRAN:
                    self.completed_units.append(supply)
                    self.supply_to_add += CONFIG["supplydepot"]["providedsupply"]
                elif self.raceType == Race.PROTOSS:
                    self.completed_units.append(supply)
                    self.supply_to_add += CONFIG["pylon"]["providedsupply"]                    

            if self.currentWorkerProduction != []:
                if self.is_chronoboosted and not self.raceType == Race.ZERG:
                    for units in self.currentWorkerProduction:  # handles instances where multiple units can be produced, really only including buildings with reactors
                        if units.build_time_remaining > 0:
                            units.chronoboost_tick()
                        else:
                            units.is_constructed = True
                            self.completed_units.append(units)
                            self.currentWorkerProduction = []
                else:
                    for units in self.currentWorkerProduction:  # handles instances where multiple units can be produced, really only including buildings with reactors
                        if units.build_time_remaining > 0:
                            units.tick()
                        else:
                            units.is_constructed = True
                            self.completed_units.append(units)
                            self.currentWorkerProduction = []

            if(self.raceType == Race.PROTOSS or (self.raceType == Race.TERRAN and self.isOrbital)):
                if(self.energy < self.maxenergy):
                    self.energy += self.energyRegenRate

            self.tickNum += 1
            self.tickUp(duration - 1)
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
        if(self.workersOnMinerals > 0 and self.builtGeysers > 0):
            self.workersOnMinerals -= 1
            self.workersBeingTransferredFromMinsToGas.append(
                self.timeToTransferMinsToGas)
            return True
        return False

    # This function will move 1 worker from Gas to minerals
    def transferGasToMins(self):
        # always take from which geyser has 3 workers on it first - it affects gas income least.
        for g in range(self.builtGeysers,self.amtGeysers):
            if self.geysers[g] > 2:
                self.geysers[g] -= 1
                self.workersBeingTransferredFromGasToMins.append(
                    self.timeToTransferMinsToGas)
                return True
            elif self.geysers[g] > 0:
                self.geysers[g] -= 1
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

    def build_supply(self):
        if self.raceType == Race.ZERG and self.currentlarva > 0:
            self.currentSupplyProduction.append(Unit("overlord"))
            return True
        elif self.raceType == Race.TERRAN and self.workersOnMinerals > 0:
            if(self.send_worker_to_make_building("supplydepot")):
                return True
        elif self.raceType == Race.PROTOSS and self.workersOnMinerals > 0:
            if(self.send_worker_to_make_building("pylon")):
                return True
        return False

    def buildGeyser(self):
        for g in range(self.builtGeysers,self.amtGeysers):
            if self.geysersUnderConstruction[g] == False:
                self.geysersUnderConstruction[g] = True
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

    def inject(self):
        if self.has_queen and not self.isInjected and self.queen_energy >= self.queen_inject_energy_cost:
            self.queen_energy -= self.queen_inject_energy_cost
            self.injectTimeRemaining = self.injectTime
            self.isInjected = True
            return True
        else:
            return False


    def send_worker_to_make_building(self, thing_to_build):
        if(self.workersOnMinerals > 0):
            self.workersOnMinerals -= 1
            worker_to_send = Unit("worker")
            worker_to_send.is_constructed = True
            worker_to_send.current_production = thing_to_build
            worker_to_send.current_production.build_time_remaining += self.workerTravelTimeToBuild * 2 # this factors in the to-and-from in building time.
            self.workersBeingSentToBuild.append(worker_to_send)
            return True
        return False

    # this will take all timers in this object and subtract them by 1 per tick.
    # It also will remove objects from the production queue if they are finished, and apply them to the base.

    def subtractTimeRemaining(self):
        if(self.raceType == Race.ZERG):
            if self.currentLarvaTimer > 0 and self.currentlarva < self.larvemax:
                self.currentLarvaTimer -= 1
            elif self.currentLarvaTimer <= 0 and self.currentlarva < self.larvaemax:
                self.currentlarva += 1
            else:
                self.currentLarvaTimer = self.larvatimer

            # Regen energy on queen if it exists
            if self.has_queen and self.queen_energy < self.queen_energy_max:
                self.queen_energy += self.energyRegenRate

            # Tell Queen to Inject if possible
            if self.has_queen and self.queen_energy >= self.queen_inject_energy_cost and not self.isInjected:
                self.queen_energy -= self.queen_inject_energy_cost
                self.injectTimeRemaining = self.injectTime
                self.isInjected = True

            # Inject Timer
            if self.isInjected and self.injectTimeRemaining > 0:
                self.injectTimeRemaining -= 1
            else:
                self.isInjected = False
                self.currentlarva += 3

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
                workers.tick()
                index += 1

        index = 0
        for workers in self.workersBeingTransferredToThisBase:
            if(workers <= 0):
                self.workersBeingTransferredToThisBase.pop(index)
                self.workersOnMinerals += 1
            else:
                workers -= 1
                index += 1

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
            if(workers.build_time_remaining <= 0):  # if the timer is over
                self.currentWorkerProduction.pop(index)
                self.workersBeingTransferredToThisBase.append(
                    self.timeToTransferMinsToGas)  # about 5 seconds before you factor in income
            else:
                workers.tick()
                index += 1

        for workers in self.workersBeingSentToBuild:

            # if the amt of travel time has been factored in
            if(self.raceType == Race.ZERG and workers.current_production.build_time_remaining == (workers.current_production.build_time_remaining - self.workerTravelTimeToBuild)):
                self.supply_to_add += 1 # do this only once
            elif(self.raceType == Race.PROTOSS and workers.current_production.build_time_remaining == (workers.current_production.build_time_remaining - self.workerTravelTimeToBuild)):
                self.workersBeingTransferredToThisBase.append(self.workerTravelTimeToBuild) # do this only once - probes go straight back to min line while building constructs.

            if workers.current_production.build_time_remaining > 0:
                workers.current_production.build_time_remaining -= 1
            else:
                self.completed_units.append(workers.current_production) # add the completed unit to list of completed units
                if CONFIG[workers.current_production]["providedsupply"] > 0: # if the building provides supply, let's add it.
                    self.supply_to_add += CONFIG[workers.current_production]["providedsupply"]
                self.workersBeingSentToBuild.remove(workers)
                if self.raceType == Race.TERRAN:
                    self.workersBeingTransferredToThisBase.append(self.workerTravelTimeToBuild) # send back to mining only after construction is done

    def debug(self):
        return None

    def get_production(self):
        if self.current_research == None and len(self.currentWorkerProduction) <= 0:
            return None
        elif len(self.currentWorkerProduction) > 0:
            return {"worker": self.currentWorkerProduction[0].build_time_remaining}
        else:
            return {self.current_research.name: self.current_research.build_time_remaining}
