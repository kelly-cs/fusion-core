class GameState:
    def __init__():
        self.bases = [] # this will contain base objects, which contain workers. Income is based on amt of workers at a given base (it changes based on saturation)
        self.units = [] # all owned units/buildings/techs.
        self.mins = 50
        self.gas = 0
    
    def getIncomeThisTick():
        incomeThisTick = 0
        for base in self.bases: # check each base for workers
            incomeThisTick += base.getIncome()
        return incomeThisTick