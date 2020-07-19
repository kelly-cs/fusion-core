"""Module representation of the player class."""

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
from enum import Enum

# local
from classes.settings import CONFIG
from classes.settings import LOG


class Race(Enum):
    ZERG = 'ZERG'
    TERRAN = 'TERRAN'
    PROTOSS = 'PROTOSS'


# ============================================================== #
#  SECTION: Classes                                              #
# ============================================================== #


class Player:
    def __init__(self, race, minerals, gas, goal_units, current_units, buildings, bases, build_order, supply, required_tech, remaining_ticks):
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
        self.remaining_ticks = remaining_ticks

    def remainingTechToBuild(self):
        tech = self.required_tech
        for requirements in tech:
            if requirements in self.current_units:
                tech.remove(requirements)
        return tech

    def tickUp(self):
        income_this_tick = [0, 0]

        for base in self.bases:  # check each base for income
            base.tickUp(1)
            # [ minerals, gas ]
            self.minerals += base.getIncomeThisTick()[0]
            # we'll pare this down later because this is stupid
            self.gas += base.getIncomeThisTick()[1]
            self.supply += base.supply_to_add
            base.supply_to_add = 0
            for units in base.completed_units:
                self.current_units.append(units)
                base.completed_units.remove(units) # remove after added

            for buildings in self.buildings:
                for units in buildings.completed_units:
                    self.current_units.append(units)
                    buildings.completed_units.remove(units) # remove after added

        #LOG.debug("ticking up player")
        return income_this_tick  # as a list [ mins, gas ]

    def canTransition(self):
        if self.allowedTransitions > 0:
            LOG.debug("transition IS allowed")
            return True
        else:
            LOG.debug("transition not allowed")
            return False

    #######################################
    # player actions
    #######################################

    def make_worker(self):
        if self.minerals >= 50 and self.supply >= 1:
            for base in self.bases:
                if base.makeWorker():
                    self.supply -= 1
                    self.minerals -= CONFIG["worker"]["mincost"]
                    LOG.debug("making a worker")
                    return True
        return False

    def build_geyser(self):
        for base in self.bases:  # check all bases
            if self.race == Race.ZERG:
                if base.builtGeysers < base.amtGeysers and self.minerals >= 25 and base.workersOnMinerals >= 1:
                    if base.buildGeyser():
                        self.minerals -= CONFIG["extractor"]["mincost"]
                        self.supply += 1
                        LOG.debug("building zerg extractor")
                        return True
                return False
            else:
                if base.builtGeysers < base.amtGeysers and self.minerals >= 75:
                    if base.buildGeyser():
                        self.minerals -= CONFIG["assimilator"]["mincost"]
                        LOG.debug("building terran/protoss geyser")
                        return True
                return False
        return False

    # build the first unit in the queue for now
    # add logic to consider addon swapping
    def build_unit(self):
        success = False # by doing this flag, we allow multiple things to be built in one go.
        if len(self.goal_units) > 0: # if there is still stuff to build
            thing_to_build = self.goal_units[0]
            mineral_cost = CONFIG[thing_to_build]["mincost"]
            gas_cost = CONFIG[thing_to_build]["gascost"]
            supply_cost = CONFIG[thing_to_build]["supply"]
            built_from = CONFIG[thing_to_build]["builtfrom"]

            if not CONFIG[thing_to_build]["isbuilding"] in CONFIG and not CONFIG[thing_to_build]["isbuilding"]: # if the next target is a UNIT
                for buildings in self.buildings: # find an appropriate building to build it from
                    if buildings.building_name == built_from: # if we have at least 1 building made that this unit is built from
                        if self.minerals > mineral_cost and self.gas > gas_cost and self.supply > supply_cost: # if we have the resources
                            if buildings.build(thing_to_build): # if the building has free capacity, build the unit
                                success = True
                for units in self.current_units: # if we didn't find a building to build the unit from, find a unit to morph from instead.
                    if units.name == built_from: # if we have a unit made that morphs into a goal unit
                        if self.minerals > mineral_cost and self.gas > gas_cost and self.supply > supply_cost: # if we have the resources
                            if units.morph(thing_to_build): # try morphing the unit
                                success = True
            elif CONFIG[thing_to_build]["isbuilding"] in CONFIG and CONFIG[thing_to_build]["isbuilding"]: # if it is a building
                if built_from == "worker":
                    if self.minerals > mineral_cost and self.gas > gas_cost and self.supply > supply_cost: # if we have the resources
                        if(self.bases[0].send_worker_to_make_building(thing_to_build)):
                            success = True
                # consider what it can morph into
                for buildings in self.buildings:
                    if buildings.building_name == built_from:
                        if buildings.morph(thing_to_build): # morph the building into another building.
                            return True
                # add addon logic here later
        return success

    def transfer_to_gas(self):
        for base in self.bases:
            # if the geysers aren't all occupied
            if base.builtGeysers > 0:
                for g in base.geysers:
                    if g < 3:
                        LOG.debug("transfer to gas in progress...")
                        return base.transferMinsToGas()
        return False

    def transfer_to_minerals(self):
        for base in self.bases:
            # if there is at least 1 worker in a geyser
            if base.builtGeysers > 0:
                for g in base.geysers:
                    if g > 0:
                        LOG.debug(
                            "transfer to minerals in progress...")
                        return base.transferGasToMins()
        return False

    def build_supply(self):
        if self.race == Race.ZERG and self.minerals >= CONFIG["overlord"]["mincost"]:
            for base in self.bases:
                if base.build_supply():
                    self.minerals -= CONFIG["overlord"]["mincost"]
                    return True
        elif self.race == Race.TERRAN and self.minerals >= CONFIG["supplydepot"]["mincost"]:
            for base in self.bases:
                if base.build_supply():
                    self.minerals -= CONFIG["supplydepot"]["mincost"]
                    return True
        elif self.race == Race.PROTOSS and self.minerals >= CONFIG["pylon"]["mincost"]:
            for base in self.bases:
                if base.build_supply():
                    self.minerals -= CONFIG["pylon"]["mincost"]
                    
        LOG.debug("building supply failed")
        return False

    def current_buildable_units(self):
        output = []
        if self.race == Race.ZERG:
            for units in self.remainingTechToBuild():
                if self.minerals >= CONFIG[units.name]["mincost"] and self.gas >= CONFIG[units.name]["gascost"] and self.supply >= CONFIG[units.name]["supply"]:
                    for current in self.current_units:
                        if CONFIG[current.name]["builtfrom"] == units.name:
                            output.append(units.name)

        return output

    def transfer_to_base(self):
        return False

    def chronoboost(self):
        return False

    # add multiple bases later
    def debug(self):
        base_debug = self.bases[0].debug()
        return (self.race,
                self.minerals,
                self.gas,
                self.goal_units,
                self.current_units,
                self.buildings,
                base_debug,
                self.build_order,
                self.supply,
                self.required_tech,
                self.allowedTransitions
                )
