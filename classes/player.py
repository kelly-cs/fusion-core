"""Module representation of the player class."""

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
from enum import Enum

# local
from classes.gamestate import WORKER_COST


class Race(Enum):
    ZERG = 'ZERG'
    TERRAN = 'TERRAN'
    PROTOSS = 'PROTOSS'


# ============================================================== #
#  SECTION: Classes                                              #
# ============================================================== #


class Player:
    def __init__(self, race , minerals, gas, goal_units, current_units, buildings, bases, build_order, supply, required_tech):
        self.race = race
        self.minerals = minerals
        self.gas = gas
        self.goal_units = goal_units
        self.current_units = current_units
        self.buildings = buildings
        self.bases = bases
        self.build_order = build_order
        self.supply = supply
        self.required_tech = required_tech
        self.allowedTransitions = 6


    # def remainingTechToBuild(self):
    #     tech = self.required_tech
    #     for requirements in tech:
    #         if requirements in self.current_units:
    #             tech.remove(requirements)
    #     return tech


    def modify_income_this_tick(self):
        income_this_tick = [0, 0]

        for base in self.bases:  # check each base for income
            base.tickNum += 1
            # [ minerals, gas ]
            self.minerals += base.getIncomeThisTick()[0]
            # we'll pare this down later because this is stupid
            self.gas += base.getIncomeThisTick()[1]

        return income_this_tick  # as a list [ mins, gas ]

    def canTransition(self):
        if self.allowedTransitions > 0:
            return True
        else:
            return False

    #######################################
    # player actions
    #######################################

    def make_worker(self):
        if self.minerals >= 50 and self.supply >= 1:
            for base in self.bases:
                if base.makeWorker():
                    self.supply -= 1
                    self.minerals -= WORKER_COST
                    return True
        return False

    def build_geyser(self):
        for base in self.bases:  # check all bases
            if self.race == Race.ZERG:
                if base.builtGeysers < 2 and self.minerals >= 25:
                    if base.buildGeyser():
                        self.minerals -= 25
                        return True
                return False
            else:
                if base.builtGeysers < 2 and self.minerals >= 75:
                    if base.buildGeyser():
                        self.minerals -= 75
                        return True
                return False
        return False

    def convert_to_gas(self):
        for base in self.bases:
            # if the geysers aren't all occupied
            if base.builtGeysers > 0 and (base.geysers[0] < 3 or base.geysers[1] < 3):
                base.transferMinsToGas()
                return True
        return False

    def convert_to_minerals(self):
        for base in self.bases:
            # if there is at least 1 worker in a geyser
            if base.builtGeysers > 0 and (base.geysers[0] > 0 or base.geysers[1] > 0):
                base.transferGasToMins()
                return True
        return False


    def build_supply(self):
        if self.race == Race.ZERG and self.minerals >= 100:
            for base in self.bases:
                if base.hasFreeProduction():
                    base.useLarva()

                    return True
        return None


    def build_unit(self):
        return False


    def convert_to_base(self):
        return False


    def chronoboost(self):
        return False
