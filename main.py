import matplotlib.pyplot as plt

from agents.baseAgent1 import BaseAgent1
from enviornment.enviornment import Enviornment


TOTAL_MAPS = 1
TRIALS_PER_MAP = 1



baseAgent1FinalPerformance = 0

for i in range(TOTAL_MAPS):

    env = Enviornment()
    tempBaseAgent1 = BaseAgent1(env)

    for i in range(TRIALS_PER_MAP):
        baseAgent1FinalPerformance += tempBaseAgent1.execute()


print(baseAgent1FinalPerformance)