import logging as log
from main import run_iteration
log.basicConfig(filename="logs.log", filemode="w",
                format='%(message)s', level=log.DEBUG)

for i in range(0, 1):
    
    value = [2, 2, 2, 4, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2]
    # value = [2 for _ in range(15)]
    reward = run_iteration(value, numeps=100)


    print(reward)
