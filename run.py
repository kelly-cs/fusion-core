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
    # run 100 seconds as zerg
    output = []
    simulation = GameState("z", 300, 0, goalUnits).runSimulation(
        output)  # store results in output
    print(simulation)
    print(output[0])
    print(len(output))
    # print(simulation.simulationResults)
