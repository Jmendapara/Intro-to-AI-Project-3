import numpy as np
from random import randrange

class Enviornment():

    def __init__(self):

        self.gridSize = 15

        self.grid = np.zeros((self.gridSize, self.gridSize), dtype = object)

        self.falseNegativeOfFlat = .1
        self.falseNegativeOfHilly = .3
        self.falseNegativeOfForested = .7
        self.falseNegativeOfMaze = .9

        self.terrainTypes = np.array(['FLAT','HILLY','FORESTED','MAZE'])
        self.nbrOfTerrainTypes = len(self.terrainTypes)

        self.createEnviornment()

        self.target = (0,0)
        self.putTarget()

    def createEnviornment(self):
        
        for x in range(self.gridSize):
            for y in range(self.gridSize):

                self.grid[x,y] = self.terrainTypes[randrange(self.nbrOfTerrainTypes)]


    def putTarget(self):
        self.target = (randrange(self.gridSize), randrange(self.gridSize))


    def getFalseNegativeRateFromTerrain(self, terrainType):

        if(terrainType == 'FLAT'):
            return self.falseNegativeOfFlat

        elif(terrainType == 'HILLY'):
            return self.falseNegativeOfHilly

        elif(terrainType == 'FORESTED'):
            return self.falseNegativeOfForested

        elif(terrainType == 'MAZE'):
            return self.falseNegativeOfMaze

        
    def searchCell(self, r, c):

        if (r, c) != self.target:
            return False

        falseNegativeRate = self.getFalseNegativeRateFromTerrain(self.grid[r, c])

        if np.random.binomial(1, 1-falseNegativeRate, 1):
            return True
        else:
            return False

    def get_terrain(self, row, col):
        return self.grid[row, col]