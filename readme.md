# RL-IA2_Final-Code-Submission
## Team members
```
Aatmaj Mhatre - 16010121110
Sushant Nair - 16010121121
Aditya Ved - 16010121208
Atharva Balajiwale - 16010121802
Kedar Shidhaye - 16010121187
```

Run code files - 

mc.py

mc_on_policy.py

ga.py

ga_extreme.py

tester.py (to test the schedule)

DONT TOUCH OTHER FILES

all outputs are present in txt files.

main.run_iteration returns a tuple (reward_value, total_average_wait_time, average_trips)

reward_value =75-2*total_average_wait_time-average_trips but you can change it if you want in RL code

main.run_iteration takes in no of episodes. (ep=1 will give you fast but uncertain results due to stochastic nature of the simulation. ep must be minimum 10 for certainity)
