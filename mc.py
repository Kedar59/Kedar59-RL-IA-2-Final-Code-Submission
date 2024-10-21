# initial policy
from main import run_iteration
import random
import logging as log

log.basicConfig(filename="monte_carlo.log", filemode="w",
                format='%(message)s', level=log.CRITICAL)


def initialize_arrays():
    V = [[0.25 for i in range(0, 4)] for _ in range(15)]
    R = [[0 for i in range(0, 4)] for _ in range(15)]  # rewards
    return V, R


def choose_actions(V,epsillon):
    value = []
    if(random.random() < epsillon):
        for state in V: #exploration
            #off policy - we are using a policy P2 for generating training data
            #P2 - choose every action equally (0.25,0.25,0.25,0.25)
            # No importance sampling done
            value.append(random.choices(range(0, 4), k=1)[0]) 
    else:
        value = greedy(V) #exploitation

    return value


def update_policy(rewards_obtained, old_policy):

    # Flatten the list to find the min and max values
    flat_list = [item for sublist in rewards_obtained for item in sublist]

    # Find min and max values
    min_value = min(flat_list)
    max_value = max(flat_list)

    # Normalize the data
    normalized_data = [
        [(value - min_value) / (max_value - min_value) for value in sublist]
        for sublist in rewards_obtained
    ]

    # Calculate the new policy using weighted averages
    new_policy = [
        [(1 - lr) * old_val + lr * new_val for old_val,
         new_val in zip(old_row, new_row)]
        for old_row, new_row in zip(old_policy, normalized_data)
    ]

    return new_policy


max_buses_to_be_sent = 5
min_buses_to_be_sent = 1

offset = max_buses_to_be_sent - 4

def greedy(V):

    result = []

    for row in V:
        max_value = max(row)  # Find the maximum value in the row
        max_index = row.index(max_value)  # Find the index of the maximum value
        result.append(max_index)

    return result


lr = 0.01
V, R = initialize_arrays()
numeps = 50
days = 50
epsillon = 0.8
for process in range(0, 1000):
    epsillon = max(epsillon*0.995, 0.1)

    for episodes in range(numeps):
        move = choose_actions(V, epsillon)
        reward,_,_ = run_iteration([i+offset for i in move], days)
        for k in range(15):
            R[k][move[k]] += reward  

        # print(R)

    V = update_policy(rewards_obtained=R, old_policy=V)
    R = [[0 for i in range(0, 4)] for _ in range(15)]  # clear rewards

    temp_reward, temp_wait, temp_trips = run_iteration(
        [i+offset for i in greedy(V)], 10)
    log_to_print = f"Process no. {process}. Policy = {[i+offset for i in greedy(V)]}. Reward = {temp_reward}. Waiting Time = {temp_wait}. Trips = {temp_trips}\n"
    # Write the content to mc.txt
    print(log_to_print)
    with open("monte_carlo_off_policy.txt", "a") as file:
        file.write(log_to_print)

# for 50 samples per run_iteration
