""""Main script for fusion-core."""

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
from copy import deepcopy
from builtins import *

# third party library

# local
from classes import settings
from classes.gamestate import GameState
from classes.player import Player, Race
from classes.gamestate import get_all_required_tech
from classes.base import Base

# ============================================================== #
#  SECTION: Helpers                                              #
# ============================================================== #


def run_simulation(output, gamestate):
    if not gamestate.remaining_ticks:
        output.append(gamestate.player.build_order)
        return output
    for action in gamestate.possible_actions:
        if action():
            gamestate_copy = deepcopy(gamestate)
            gamestate_copy.player.build_order.append((action.__name__,
                                                      gamestate_copy.remaining_ticks,
                                                      gamestate_copy.player.minerals,
                                                      gamestate_copy.player.gas,
                                                      gamestate_copy.player.supply))
            gamestate_copy.remaining_ticks -= 1
            gamestate_copy.player.modify_income_this_tick()
            run_simulation(output, gamestate_copy)

    # required to create the tree, otherwise only 1 object is made and the data is mangled
    gamestate_copy = deepcopy(gamestate)
    gamestate_copy.player.build_order.append((None,
                                              gamestate_copy.remaining_ticks,
                                              gamestate_copy.player.minerals,
                                              gamestate_copy.player.gas,
                                              gamestate_copy.player.supply))
    gamestate_copy.remaining_ticks -= 1
    gamestate_copy.player.modify_income_this_tick()
    return run_simulation(output, gamestate_copy)


# ============================================================== #
#  SECTION: Main                                                 #
# ============================================================== #

if __name__ == "__main__":
    goal_units = [
        "zergling",
        "zergling",
        "zergling",
        "zergling"
    ]

    settings.init()  # runs settings, makes it available across all files (init only needs to be ran here)
    output = []
    player = Player(Race.ZERG,
                    minerals=50,
                    gas=0,
                    goal_units=goal_units,
                    current_units=[],
                    buildings=[],
                    bases=[Base(12, Race.ZERG, "normal", "normal", 2, False)],
                    build_order=[],
                    supply=3,
                    required_tech=get_all_required_tech(goal_units) + goal_units)
    gamestate = GameState(remaining_ticks=10, player=player)
    simulation = run_simulation(output, gamestate)  # store results in output
    # print(simulation)
    print(output[0])
    print(len(output))
