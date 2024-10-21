import random
from main import run_iteration

num = 50000
size = 15
num_values = 6
# for 50 samples per run_iteration
for i in range(num):
    random_sample = [random.randint(2, num_values-1) for _ in range(size)]
    print(run_iteration(random_sample,100))
    # print(i)
    # print(random_sample)
    # print(run_iteration(random_sample))
    
