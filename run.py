from classes import settings
from classes.gamestate import GameState
#from classes.settings import init

# insert at 1, 0 is the script path (or '' in REPL)
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder


if __name__ == "__main__":
    race = "z"
    goalUnits = [
        "zergling",
        "zergling",
        "zergling",
        "zergling"
    ]

    settings.init()  # runs settings
    # print(str(settings.CONFIG))
    simulation = GameState("z", 100, 0, goalUnits)  # run 100 seconds as zerg
    print(simulation.simulationResults)
