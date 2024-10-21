from passenger_module import passenger
from bus_module import bus
from bus_stop_module import bus_stop
from depot_module import depot
from initializer import initialize

import logging as log



def run_iteration(value, numeps):
    depot.var = value[:]
    depot.var.append(0)  # no bus after 8

    total_average_wait_time = 0
    total_average_stand_time = 0

    for episode in range(numeps):
        stop_list, arrival_day, day_type, main_depot = initialize()
        bus_list: list[bus] = []
        time = 0
        while time < 960:
            for stop_i in stop_list[:-1]:
                stop_i.advance(time, arrival_day)

            bus_list = main_depot.update_bus_lists(time)

            for bus_i in bus_list:
                bus_i.advance(time=time, day_type=day_type)

            time += 1
        for stop_i in stop_list[:-1]:
            stop_i.end(time)

        log.debug(f"Episode number {episode}")
        log.debug(
            f'Average waiting time: {passenger.total_waiting_time/passenger.passenger_count}')
        log.debug(
            f'Average standing time: {passenger.total_standing_time/passenger.passenger_count}')

        total_average_wait_time += passenger.total_waiting_time / passenger.passenger_count
        total_average_stand_time += passenger.total_standing_time / passenger.passenger_count
        passenger.total_waiting_time = 0
        passenger.total_standing_time = 0
        passenger.passenger_count = 0
    total_average_wait_time /= numeps
    total_average_stand_time /= numeps
    average_trips = depot.trips/numeps
    depot.trips = 0

    reward_value = 75-2*total_average_wait_time-average_trips
    # Define the content
    content = f"{depot.var},{total_average_stand_time},{total_average_wait_time},{average_trips},{reward_value}"
    log.info(content)

    return (reward_value, total_average_wait_time, average_trips)



