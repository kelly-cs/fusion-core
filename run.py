from classes.gamestate import GameState

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

    simulation = GameState("z", 100, goalUnits)  # run 100 seconds as zerg
