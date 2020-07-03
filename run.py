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
    for action in gamestate.possible_actions:
        # this will reach into GameState and run the function directly in its Player class.
        gamestate_copy = deepcopy(gamestate)
        action_name = str(action.__name__)
        action_function = getattr(gamestate_copy.player, action_name)
        # this has to be a copy or we don't branch correctly.
        if action_function():
            # print(action.__name__)
            settings.LOG.debug(action_name)
            if settings.LOG.level == settings.logging.DEBUG:
                gamestate_debug = gamestate_copy.debug_gamestate()
                player_debug = gamestate_copy.debug_player()
                bases_debug = gamestate_copy.debug_bases()
                # settings.LOG.debug(action.__name__)
                gamestate_copy.player.build_order.append({"completed_action": action.__name__, "gamestate": gamestate_debug, "player": player_debug, "bases": bases_debug}
                                                         )
            else:  # if NOT in debug mode, we get only practical information
                gamestate_copy.player.build_order.append(
                    {"completed_action": action.__name__, "gamestate": gamestate_debug})

            # regardless of logging level, we recurse normally.
            gamestate_copy.remaining_ticks -= 1
            gamestate_copy.player.tickUp()
            run_simulation(output, gamestate_copy)

    gamestate_copy = deepcopy(gamestate)
    # print(gamestate_copy.player.build_order)
    if settings.LOG.level == settings.logging.DEBUG:
        gamestate_debug = gamestate_copy.debug_gamestate()
        player_debug = gamestate_copy.debug_player()
        bases_debug = gamestate_copy.debug_bases()
        gamestate_copy.player.build_order.append({"completed_action": "wait", "gamestate": gamestate_debug, "player": player_debug, "bases": bases_debug}
                                                 )
    else:  # if NOT in debug mode, we get only practical information
        gamestate_copy.player.build_order.append(
            {"completed_action": "wait", "gamestate": gamestate_debug})

    gamestate_copy.remaining_ticks -= 1
    gamestate_copy.player.tickUp()
    run_simulation(output, gamestate_copy)
    """
        else:
        if gamestate.target():
            gamestate_copy = deepcopy(gamestate)
            if settings.LOG.level == settings.logging.DEBUG:
                gamestate_debug = dictgamestate_copy.debug_gamestate()
                player_debug = gamestate_copy.debug_player()
                bases_debug = gamestate_copy.debug_bases()
                gamestate_copy.player.build_order.append(
                    {"completed_action": gamestate.target.__name__, "gamestate": gamestate_debug, "player": player_debug, "bases": bases_debug})

            else:  # if NOT in debug mode, we get only practical information
                gamestate_copy.player.build_order.append(
                    {"completed_action": action.__name__, "gamestate": gamestate_debug})

            # regardless of logging level, we recurse normally.
            gamestate_copy.remaining_ticks -= 1
            gamestate_copy.player.tickUp()
            gamestate_copy.target = None
            run_simulation(output, gamestate_copy)

        else:  # retain target and only try this until successful.
            gamestate_copy = deepcopy(gamestate)
            if settings.LOG.level == settings.logging.DEBUG:
                gamestate_debug = gamestate_copy.debug_gamestate()
                player_debug = gamestate_copy.debug_player()
                bases_debug = gamestate_copy.debug_bases()
                gamestate_copy.player.build_order.append({"target": gamestate.target.__name__, "gamestate": gamestate_debug, "player": player_debug, "bases": bases_debug}
                                                         )
            else:  # if NOT in debug mode, we get only practical information
                gamestate_copy.player.build_order.append({"target": gamestate.target.__name__, "gamestate": gamestate_debug}
                                                         )
            gamestate_copy = deepcopy(gamestate)
            gamestate_copy.remaining_ticks -= 1
            gamestate_copy.player.tickUp()
            run_simulation(output, gamestate_copy) """


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
    gamestate = GameState(remaining_ticks=100,
                          player=player)
    # store results in output
    simulation = run_simulation(output, gamestate)
    # print(simulation)
    # print(output)
    # print(len(output))
    settings.LOG.info(json.dumps(output))
