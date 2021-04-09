import numpy as np
#from .MineVisualization import game
import random 
from random import randrange


import math
import matplotlib.pyplot as plt

class BaseAgent1():

    def __init__(self, env):

        self.env = env
        self.totalNbrOfSearches = 0
        self.totalManDistance = 0

        initialBelief = 1 / env.gridSize ** 2
        self.currentBelief = np.zeros((env.gridSize, env.gridSize))

        for x in range(env.gridSize):
            for y in range(env.gridSize):
                self.currentBelief[x,y] = initialBelief

        self.highestBelief = initialBelief

        self.FLAT_SEARCHES = 0
        self.HILLY_SEARCHES = 0
        self.FORESTED_SEARCHES = 0
        self.MAZE_SEARCHES = 0

        
    def search(self, row, col):
        self.totalNbrOfSearches += 1

        terrainType = self.env.grid[row,col]

        if(terrainType == 'FLAT'):
            self.FLAT_SEARCHES += 1

        elif(terrainType == 'HILLY'):
            self.HILLY_SEARCHES += 1

        elif(terrainType == 'FORESTED'):
            self.FORESTED_SEARCHES += 1

        elif(terrainType == 'MAZE'):
            self.MAZE_SEARCHES += 1

        return self.env.searchCell(row, col)

    def getManDistance(self, selectedCell, nextCellToSearch):
        return math.fabs(selectedCell[0] - nextCellToSearch[0]) + math.fabs(selectedCell[1] - nextCellToSearch[1])

    def getTotalPerformance(self):
        return self.totalNbrOfSearches + self.totalManDistance

    def updateBelief(self, tempCurrentCell, selectedCell, previousSelectCellProbability, falseNegativeProbability):

        #total probability of getting data
        totalProb = (previousSelectCellProbability * falseNegativeProbability + (1 - previousSelectCellProbability) * 1)

        if (tempCurrentCell != selectedCell):
            previousCurrentCellProb = self.currentBelief[tempCurrentCell[0]][tempCurrentCell[1]]
            postBelief = previousCurrentCellProb / totalProb

        elif tempCurrentCell == selectedCell:
            postBelief = previousSelectCellProbability * falseNegativeProbability / totalProb
        
        self.currentBelief[tempCurrentCell[0]][tempCurrentCell[1]] = postBelief

    
    #checks to see if position (i,j) is a valid position
    def inGrid(self, i,j):

        maxGridPosition = self.env.gridSize - 1
        if((i < 0) or (i > maxGridPosition) or (j < 0) or (j > maxGridPosition)):
            return False
        return True


    def selectHighestBeliefCell(self, selectedCell):

        shortestDistance = 1000000

        tempMaxBeliefCells = []
        tempShortestDistanceMaxBeliefCells = []

        #get the cell with the highest belief
        for i in range(self.env.gridSize):
            for j in range(self.env.gridSize):
                if self.currentBelief[i][j] == self.highestBelief:
                    tempMaxBeliefCells.append((i, j))

        #get random cell with the shortest distance that has the highest belief
        for cell in tempMaxBeliefCells:
            tempDistance = self.getManDistance(selectedCell, cell)
            if(tempDistance == shortestDistance):
                tempShortestDistanceMaxBeliefCells.append(cell)
            elif(tempDistance < shortestDistance):
                shortestDistance = tempDistance
                tempShortestDistanceMaxBeliefCells = []
                tempShortestDistanceMaxBeliefCells.append(cell)

        nextCell = random.choice(tempShortestDistanceMaxBeliefCells)
        self.totalManDistance += shortestDistance
        return nextCell

    def execute(self):

        previousCell = (randrange(self.env.gridSize), randrange(self.env.gridSize))
        while True:

            selectedCell = self.selectHighestBeliefCell(previousCell)
            terrain = self.env.grid[selectedCell[0], selectedCell[1]]

            targetFound = self.search(selectedCell[0], selectedCell[1])

            if targetFound:
                break

            self.highestBelief = -1
            previousSelectCellProbability = self.currentBelief[selectedCell[0]][selectedCell[1]]
            for i in range(self.env.gridSize):
                for j in range(self.env.gridSize):
                    self.updateBelief((i, j), selectedCell, previousSelectCellProbability, self.env.getFalseNegativeRateFromTerrain(terrain))
                    if self.currentBelief[i][j] > self.highestBelief:
                        self.highestBelief = self.currentBelief[i][j]

            #normalize the probability values
            sumOfAllProbabilities = np.sum(self.currentBelief)
            self.highestBelief /= sumOfAllProbabilities
            self.currentBelief /= sumOfAllProbabilities

            previousCell = selectedCell

            #plt.imshow(self.currentBelief, interpolation='none')
            #plt.pause(0.00001)

            # input()
        return self.getTotalPerformance(), self.FLAT_SEARCHES, self.HILLY_SEARCHES, self.FORESTED_SEARCHES, self.MAZE_SEARCHES