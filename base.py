class Base:
    def __init__(self, race, mineraltype, gastype, geysers, underconstruction):
        self.mineraltype = mineraltype # can be "normal" or "rich"
        self.gasType = gastype # can be "normal" or "rich"
        self.amtGeysers = geysers # amount of gas geysers
        self.amtMinerals = 8 # standard amt. Reduce to 6 for rich fields.
        self.workersOnMinerals = [] # list of workers on minerals at this base
        self.builtGeysers = [] # list of built geysers (which contain workers)
        self.isUnderConstruction = underconstruction # true or false
        self.constructionTime = 71 # amt of time to build a base
        self.constructionTimeRemaining = 0 # amt of time remaining to construct this base
        self.raceType = race # "z, t, or p" to represent zerg, terran, or protoss.

        self.energyRegenRate =  0.7875 # every second, add this to energy.
        self.energy = 0
        self.maxenergy = 200

        # ZERG
        if(self.raceType = "z"):
            self.currentlarvae = 3 # start the game with 3 active.
            self.larvemax = 3 # max that can produce normally (via larvatimer)
            self.larvainjectmax = 19 # max that can exist (with the help of a queen)
            self.larvatimer = 11 # this is how long it takes to make a larvae, when below larvamax.
            self.currentLarvaTimer = 0 # this is the current time before making another larva.
            self.injectAmt = 3 # this is 4 in HotS and WoL, but I don't care. This is how much a queen adds when injecting.

            self.isInjected = 0 # 0 or 1. 
            self.injectTime = 40 # this is how long it takes for an inject to procuce injectAmt of larva here.
            self.injectTimeRemaining = 0  # this is how long is remaining to produce injectAmt of larva, but only if isInjected is active (1)
        # TERRAN
        if(self.raceType = "t"):
        
            self.isOrbital = false
            self.isTurningIntoOrbital = 0
            self.orbitalConstructionTime = 25
            self.orbitalConstructionTimeRemaining = 0
        # PROTOSS
        if(self.raceType = "p"):

            self.energy = 50 # starting energy for protoss nexus
            self.chronoCost = 50 # cost for chrono boost

        self.currentlyBuildingWorker = 0 # 0 if not building, 1 if building one
        self.workerBuildingTime = 12 # amt of time it takes to build a worker. 12 standard
        self.buildingWorkerTimeRemaining = 0
        self.tick = 0 # amt of elapsed game time
        
        try:
            if(self.mineraltype = "rich"):
                self.amtMinerals = 6
            elif(self.mineraltype != "normal"):
                raise Exception("Incorrect Mineral Type -> " + str(self.mineralType))
        except Exception as e:
            print("An error occurred while initializing Base: " + str(e))

        try:
            if(self.isUnderConstruction)
                self.constructionTimeRemaining = self.constructionTime
        except:
            print("Something happened when initializing UnderConstruction for Base: " + str(e))


    # updates 1 game second for everything in this object
    def tick(self):
        if(self.raceType = "p" or (self.raceType ="t" and self.isOrbital)):
            self.energy += self.energyRegenRate

        for worker in self.workersOnMinerals:
            worker.tick()
        for geyser in self.builtGeysers:
            for worker in geyser:
                worker.tick()

    # returns an array [minerals, gas] for all income gained this tick.
    def getIncomeThisTick(self): 
        mineralincome = 0
        gasincome = 0
        
        for worker in self.workersOnMinerals:
            income += worker.getIncomeThisTick() # add up all minerals from workers
        for geyser in self.builtGeysers:
            for worker in geyser:
                income += worker.getIncomeThisTick()
        income = [mineralincome, gasincome]
        return income # return as array
