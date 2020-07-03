""""Main script for fusion-core."""

# ============================================================== #
#  SECTION: Imports                                              #
# ============================================================== #

# standard library
from copy import deepcopy
from builtins import *
import json
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

    gamestate_copy = deepcopy(gamestate)

    # Only try all possibilities if there is not target yet.
    if gamestate.target_action == None:
        for action in gamestate.possible_actions:
            if action():  # this will reach into GameState and run the function directly in its Player class.

                if settings.LOG.level == settings.logging.DEBUG:
                    gamestate_debug = gamestate_copy.debug_gamestate()
                    player_debug = gamestate_copy.debug_player()
                    bases_debug = gamestate_copy.debug_bases()

                    gamestate_copy.player.build_order.append({"completed_action": action.__name__, "gamestate": gamestate_debug, "player": player_debug, "bases": bases_debug}
                                                             )
                else:  # if NOT in debug mode, we get only practical information
                    gamestate_copy.player.build_order.append({"completed_action": action.__name__, "gamestate": gamestate_debug}
                                                             )
                # regardless of logging level, we recurse normally.
                gamestate_copy.remaining_ticks -= 1
                gamestate_copy.player.tickUp()
                gamestate_copy.target_action = None
                # Putting None here signifies that we can try a new action the next tick.
                run_simulation(output, gamestate_copy)

            else:  # if the action fails, set it as a target and recurse there.
                gamestate_copy.remaining_ticks -= 1
                gamestate_copy.player.tickUp()
                gamestate_copy.target_action = action
                run_simulation(output, gamestate_copy)

    else:  # if we have a target action to do
        if gamestate.target_action():  # if the action is successful
            gamestate_copy.player.build_order.append((target_action.__name__,
                                                      gamestate_copy.remaining_ticks,
                                                      gamestate_copy.player.minerals,
                                                      gamestate_copy.player.gas,
                                                      gamestate_copy.player.supply))
            gamestate_copy.remaining_ticks -= 1
            gamestate_copy.player.tickUp()
            gamestate_copy.target_action = None
            # branch out at next tick
            run_simulation(output, gamestate_copy)
        else:  # if it still fails, keep trying.
            gamestate_copy.remaining_ticks -= 1
            gamestate_copy.player.tickUp()
            # branch out at next tick
            run_simulation(output, gamestate_copy)


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
                    bases=[Base(12, Race.ZERG, "normal",
                                "normal", 2, False)],
                    build_order=[],
                    supply=3,
                    required_tech=get_all_required_tech(goal_units) + goal_units)
    gamestate = GameState(remaining_ticks=10,
                          player=player, target_action=None)
    # store results in output
    simulation = run_simulation(output, gamestate)
    # print(simulation)
    print(len(output))
    settings.LOG.info(json.dumps(output))
