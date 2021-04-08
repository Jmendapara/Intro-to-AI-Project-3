import numpy as np
#from .MineVisualization import game
import random 
from random import randrange


import math
import matplotlib.pyplot as plt

class ImprovedAgent():

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

    def show(self):
        for row in self.currentBelief:
            print(row)

    def getManDistance(self, selectedCell, nextCellToSearch):
        return math.fabs(selectedCell[0] - nextCellToSearch[0]) + math.fabs(selectedCell[1] - nextCellToSearch[1])

    def getTotalPerformance(self):
        return self.totalNbrOfSearches + self.totalManDistance

    def calculateNewProbability(self, previousSelectCellProbability, falseNegativeProbability):
        # P(T != Cj) = { P(Ta = Cj) X P(T != Cj)   +  P(Ta != Cj) X P(T != Cj)
        #                 Prior     X P_false_neg  +  (1 - Prior) X 1
        return previousSelectCellProbability * falseNegativeProbability + (1 - previousSelectCellProbability) * 1

    def update(self, current_cell, searched_cell, previousSelectCellProbability, falseNegativeProbability):

        if current_cell == searched_cell:
            posterior = previousSelectCellProbability * falseNegativeProbability / self.calculateNewProbability(previousSelectCellProbability, falseNegativeProbability)
        else:
            previousProbability = self.currentBelief[current_cell[0]][current_cell[1]]
            posterior = previousProbability / self.calculateNewProbability(previousSelectCellProbability, falseNegativeProbability)
        self.currentBelief[current_cell[0]][current_cell[1]] = posterior

    
    #checks to see if position (i,j) is a valid position
    def inGrid(self, i,j):

        maxGridPosition = self.env.gridSize - 1
        if((i < 0) or (i > maxGridPosition) or (j < 0) or (j > maxGridPosition)):
            return False
        return True


    def selectHighestBeliefCell(self, selectedCell):

        utility = np.zeros((self.env.gridSize, self.env.gridSize))

        util_cells = {}
        max_util = -1
        nextBestCell = None
        for i in range(self.env.gridSize):
            for j in range(self.env.gridSize):
                prob = self.currentBelief[i,j]
                if selectedCell == (i, j):
                    continue
                utility[i][j] = prob / self.getManDistance(selectedCell, (i, j))

                if utility[i][j] > max_util:
                    if max_util in util_cells:
                        util_cells.pop(max_util)
                    # add this new max
                    max_util = utility[i][j]
                    if max_util not in util_cells:
                        util_cells[max_util] = []
                    util_cells[max_util].append((i, j))

                if utility[i][j] == max_util:
                    util_cells[max_util].append((i, j))

        nextBestCell = random.choice(util_cells[max_util])
        distance = self.getManDistance(selectedCell, nextBestCell)
        #if distance != 1:
            #print(f"Distance: {distance}")
        self.totalManDistance += distance
        return nextBestCell


    def execute(self):

        previousCell = (randrange(self.env.gridSize), randrange(self.env.gridSize))

        while True:

            selectedCell = self.selectHighestBeliefCell(previousCell)
            terrain = self.env.get_terrain(*selectedCell)
            #print(f"selectedCell: {selectedCell}, terrain: {terrain}")

            found = self.search(*selectedCell)

            if found:
                break

            self.highestBelief = -1
            previousSelectCellProbability = self.currentBelief[selectedCell[0]][selectedCell[1]]
            for i in range(self.env.gridSize):
                for j in range(self.env.gridSize):
                    self.update((i, j), selectedCell, previousSelectCellProbability, self.env.getFalseNegativeRateFromTerrain(terrain))
                    if self.currentBelief[i][j] > self.highestBelief:
                        self.highestBelief = self.currentBelief[i][j]

            # Normalize the probability values
            sumOfAllProbabilities = np.sum(self.currentBelief)
            self.currentBelief /= sumOfAllProbabilities
            self.highestBelief /= sumOfAllProbabilities

            previousCell = selectedCell
            # Update the visualization matrix
            #self.update_visualization(*selectedCell)

            #plt.imshow(self.currentBelief, interpolation='none')
            #plt.pause(0.00001)

            # input()
        return self.getTotalPerformance(), self.FLAT_SEARCHES, self.HILLY_SEARCHES, self.FORESTED_SEARCHES, self.MAZE_SEARCHES