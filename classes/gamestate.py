""""Holds the state of a Star Craft 2 game."""

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
from builtins import *

# third party library

# local
from classes.settings import CONFIG
from classes.settings import LOG
from classes.player import Race

# ============================================================== #
#  SECTION: Global Definitions                                   #
# ============================================================== #

STARTING_WORKERS = 12

# ============================================================== #
#  SECTION: Helpers Static                                       #
# ============================================================== #


def get_all_required_tech(composition):
    requiredtech = []  # return a list of all required items, using the config file for help
    for unitname in composition:  # for all things you want to make
        if unitname in CONFIG:  # if these things are things you can actually make
            # if there's any requirements
            if len(CONFIG[unitname]["requires"]) > 0:
                # check each requirement for that unit
                for each_requirement in CONFIG[unitname]["requires"]:
                    if each_requirement not in requiredtech:
                        # print(each_requirement)
                        requiredtech.append(each_requirement)
                        # if there's more nested requirements
                        if len(CONFIG[each_requirement]["requires"]) > 0:
                            requiredtech.extend(  # let's just call this function again
                                get_all_required_tech([each_requirement]))

    # this gets rid of duplicates from nested tech tree because I was lazy
    # this will cause issues later when we have units that morph from other units
    # (i.e. banelings). I can probably just fix this after the fact by requiring
    # the zerglings to be produced to be at least the same as the expected baneling count,
    # or the amount of templars to be at least double the amount of expected archons.
    return list(dict.fromkeys(requiredtech))

# ============================================================== #
#  SECTION: Classes                                              #
# ============================================================== #


class GameState:

    def __init__(self, remaining_ticks, player):

        self.remaining_ticks = remaining_ticks

        self.player = player
        # these are direct references to the functions in the Player class.
        self.possible_actions = [self.player.make_worker,
                                 self.player.build_supply,
                                 self.player.build_unit,
                                 self.player.build_geyser]

        if player.race == Race.PROTOSS:
            self.possible_actions.append(self.player.chronoboost)

    # ============================================================== #
    #  SECTION: Helpers Static                                       #
    # ============================================================== #
    # returns a dictionary containing all current gamestate data


    def tick(self):
        self.player.tickUp()
        if not self.player.transfer_to_base in self.possible_actions and len(self.player.bases) > 1:
            self.possible_actions.append(self.player.transfer_to_base)
        if not self.player.transfer_to_gas in self.possible_actions:
            for bases in self.player.bases:
                if bases.builtGeysers > 0:
                    self.possible_actions.append(self.player.transfer_to_gas)
                    self.possible_actions.append(self.player.transfer_to_minerals)
        return True

    def debug_gamestate(self):
        return {
            "remaining_ticks": self.remaining_ticks,
        }

    # returns a dictionary containing all player data - except build order, because we output this information to that
    def debug_player(self):
        output_units = []
        for units in self.player.current_units:
            output_units.append(units.name) 
        output_buildings = []
        for buildings in self.player.buildings:
            output_buildings.append(buildings.name)
        return{
            "race": str(self.player.race),
            "minerals": self.player.minerals,
            "gas": self.player.gas,
            "goal_units": self.player.goal_units,
            "current_units": output_units,
            "buildings": output_buildings,
            "supply": self.player.supply,
            "required_tech": self.player.required_tech,
            "allowed_transitions": self.player.allowedTransitions
        }

    # returns a dictionary containing all useful data at the current tick for the player's bases
    def debug_bases(self):
        base_dictionary = {}
        index = 0
        for base in self.player.bases:
            base_dictionary["base" + str(index)] = {
                "geysersRemainingTime": base.geysersRemainingTime,
                "geysersUnderConstruction": base.geysersUnderConstruction,
                "workersOnMinerals": base.workersOnMinerals,
                "workersBeingSentToBuildGas": base.workersBeingSentToBuildGas,
                "workersBeingTransferredFromGasToMins": base.workersBeingTransferredFromGasToMins,
                "workersBeingTransferredFromMinsToGas": base.workersBeingTransferredFromMinsToGas,
                "workersBeingTransferredToThisBase": base.workersBeingTransferredToThisBase,
                "production": base.get_production(),
                "isHatchery": base.isHatchery,
                "isLair": base.isLair,
                "isHive": base.isHive
            }
            index += 1

        return base_dictionary

# ============================================================== #
#  SECTION: Main                                                 #
# ============================================================== #
