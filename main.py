import matplotlib.pyplot as plt

from agents.baseAgent1 import BaseAgent1
from agents.baseAgent2 import BaseAgent2
from agents.improvedAgent import ImprovedAgent

import pandas as pd 

from enviornment.enviornment import Enviornment


TOTAL_MAPS = 10
TRIALS_PER_MAP = 10


baseAgent1FinalPerformance = 0
baseAgent2FinalPerformance = 0
improvedAgentFinalPerformance = 0

Flat1 = 0
Flat2 = 0
FlatImproved = 0

Hilly1 = 0
Hilly2 = 0
HillyImproved = 0

Forested1 = 0
Forested2 = 0
ForestedImproved = 0

Maze1 = 0
Maze2 = 0
MazeImproved = 0

for i in range(TOTAL_MAPS):

    env = Enviornment()
    tempBaseAgent1 = BaseAgent1(env)
    tempBaseAgent2 = BaseAgent2(env)
    tempImprovedAgent = ImprovedAgent(env)

    for j in range(TRIALS_PER_MAP):

        print('Map = ' + str(i) + ' -- Trial = ' + str(j))

        base1, flat, hilly, forested, maze = tempBaseAgent1.execute()
        baseAgent1FinalPerformance += base1/TRIALS_PER_MAP
        Flat1 += flat/TRIALS_PER_MAP
        Hilly1 += hilly/TRIALS_PER_MAP
        Forested1 += forested/TRIALS_PER_MAP
        Maze1 += maze/TRIALS_PER_MAP

        base2, flat, hilly, forested, maze = tempBaseAgent2.execute()
        baseAgent2FinalPerformance += base2/TRIALS_PER_MAP
        Flat2 += flat/TRIALS_PER_MAP
        Hilly2 += hilly/TRIALS_PER_MAP
        Forested2 += forested/TRIALS_PER_MAP
        Maze2 += maze/TRIALS_PER_MAP

        improved, flat, hilly, forested, maze = tempImprovedAgent.execute()
        improvedAgentFinalPerformance += improved/TRIALS_PER_MAP
        FlatImproved += flat/TRIALS_PER_MAP
        HillyImproved += hilly/TRIALS_PER_MAP
        ForestedImproved += forested/TRIALS_PER_MAP
        MazeImproved += maze/TRIALS_PER_MAP    

Flat1 /= TOTAL_MAPS
Flat2 /= TOTAL_MAPS
FlatImproved /= TOTAL_MAPS

Hilly1 /= TOTAL_MAPS
Hilly2 /= TOTAL_MAPS
HillyImproved /= TOTAL_MAPS

Forested1 /= TOTAL_MAPS
Forested2 /= TOTAL_MAPS
ForestedImproved /= TOTAL_MAPS

Maze1 /= TOTAL_MAPS
Maze2 /= TOTAL_MAPS
MazeImproved /= TOTAL_MAPS

data=[["Flat", Flat1, Flat2, FlatImproved ],
      ["Hilly", Hilly1 , Hilly2 , HillyImproved],
      ["Forested",Forested1,Forested2,ForestedImproved],
      ["Maze",Maze1,Maze2,MazeImproved]
     ]

df=pd.DataFrame(data,columns=["Terrain Type","Base Agent 1","Base Agent 2","Improved Agent"])
df.plot(x="Terrain Type", y=["Base Agent 1", "Base Agent 2", "Improved Agent"], kind="bar")
plt.show()

print('Average total performane for Basic Agent 1: ' + str(baseAgent1FinalPerformance/TOTAL_MAPS))
print('Average total performane for Basic Agent 2: ' + str(baseAgent2FinalPerformance/TOTAL_MAPS))
print('Average total performane for Improved Agent: ' + str(improvedAgentFinalPerformance/TOTAL_MAPS))
