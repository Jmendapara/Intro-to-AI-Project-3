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

        
    def search(self, row, col):
        self.totalNbrOfSearches += 1
        return self.env.searchCell(row, col)

    def show(self):
        for row in self.currentBelief:
            print(row)

    #def update_visualization(self, row, col):
    #    if self.visualize:
    #        self.visualization.update(row, col, self.currentBelief[row][col])

    def getManDistance(self, current, dest):
        return math.fabs(current[0] - dest[0]) + math.fabs(current[1] - dest[1])

    def getTotalPerformance(self):
        return self.totalNbrOfSearches + self.totalManDistance

    def P_data(self, prior, falseNegativeProbability):
        # P(T != Cj) = { P(Ta = Cj) X P(T != Cj)   +  P(Ta != Cj) X P(T != Cj)
        #                 Prior     X P_false_neg  +  (1 - Prior) X 1
        return prior * falseNegativeProbability + (1 - prior) * 1

    def update(self, current_cell, searched_cell, prior, falseNegativeProbability):

        if current_cell == searched_cell:
            posterior = prior * falseNegativeProbability / self.P_data(prior, falseNegativeProbability)
        else:
            prior_current_cell = self.currentBelief[current_cell[0]][current_cell[1]]
            posterior = prior_current_cell / self.P_data(prior, falseNegativeProbability)
        self.currentBelief[current_cell[0]][current_cell[1]] = posterior

    def selectHighestBeliefCell(self, current):
        max_belief_cells = []
        for i in range(self.env.gridSize):
            for j in range(self.env.gridSize):
                if self.currentBelief[i][j] == self.highestBelief:
                    max_belief_cells.append((i, j))

        dest = random.choice(max_belief_cells)
        distance = self.getManDistance(current, dest)
        self.totalManDistance += distance
        return dest

    def execute(self):
        prev_cell = (randrange(self.env.gridSize), randrange(self.env.gridSize))
        while True:
            # self.show()
            current = self.selectHighestBeliefCell(prev_cell)
            terrain = self.env.get_terrain(*current)
            print(f"current: {current}, terrain: {terrain}")

            found = self.search(*current)

            if found:
                break

            self.highestBelief = -1
            prior = self.currentBelief[current[0]][current[1]]
            for i, row in enumerate(self.currentBelief):
                for j, prob in enumerate(row):
                    self.update((i, j), current, prior, self.env.getFalseNegativeRateFromTerrain(terrain))
                    if self.currentBelief[i][j] > self.highestBelief:
                        self.highestBelief = self.currentBelief[i][j]
            # Normalize the probability values
            total_prob = np.sum(self.currentBelief)
            self.currentBelief /= total_prob
            self.highestBelief /= total_prob
            # prev cell searched -> used for selectHighestBeliefCell
            prev_cell = current
            # Update the visualization matrix
            #self.update_visualization(*current)
            print(self.currentBelief)
            #plt.imshow(self.currentBelief, interpolation='none')
            #plt.pause(0.00001)

            # input()
        print(self.totalNbrOfSearches)
        return self.getTotalPerformance()