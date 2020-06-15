import itertools

workers =  2 # 44 2 base, 66 3 base
makesupply = 0 # 25
movetogas = 0 # arbitrary
movetomins = 0 # arbitrary
buildgeyser = 0 # based on how many bases (2 per base)
units = ["marine","marine"]
expand = 0
possible_actions = []

while workers > 0:
    possible_actions.append("w")
    workers-=1
while makesupply > 0:
    possible_actions.append("")
    makesupply-=1
while movetogas > 0:
    possible_actions.append("mg")
    movetogas-=1
while movetomins > 0:
    possible_actions.append("mm")
    movetomins-=1
while buildgeyser > 0:
    possible_actions.append("g")
    buildgeyser-=1
while len(units) > 0:
    possible_actions.append(units.pop(-1)) #remove last unit, it returns into the append function
while expand > 0:
    possible_actions.append("e")
    expand-=1

permutations_object = itertools.permutations(possible_actions)
ls = list(permutations_object)

print("SIZE" + str(len(ls)))
print(str(ls))