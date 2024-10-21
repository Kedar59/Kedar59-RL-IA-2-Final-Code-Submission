from passenger_module import passenger
from bus_module import bus
from bus_stop_module import bus_stop

import logging as log


class depot:
    var = []
    trips = 0

    def __init__(self, max_capacity: int, sitting_capacity: int, stops_list: list[bus_stop], travel_time_matrix: list[list[int]], total_busses: int):

        self.running_bus_list: list[bus] = []
        self.available_bus_list: list[bus] = []
        self.total_busses: int = total_busses
        for i in range(self.total_busses):
            new_bus = bus(i, max_capacity=max_capacity, sitting_capacity=sitting_capacity,
                          stops_list=stops_list, travel_time_matrix=travel_time_matrix)
            self.available_bus_list.append(new_bus)

    def policy(self, time: int):
        hour: int = time//60
        if (depot.var[hour] == 0):
            return False
        review_time = 60 // depot.var[hour]
        return time % review_time == 0

    def update_bus_lists(self, time) -> list[bus]:

        for bus_i in self.running_bus_list:
            # once bus returns, remove it from running list and put it in the available list
            if bus_i.finished == True:
                self.running_bus_list.remove(bus_i)
                self.available_bus_list.append(bus_i)
                log.debug(f"Bus #{bus_i.bus_number} has arrived at the depot at time {time}. It has has {len(bus_i.passenger_sitting_list)} passengers sitting and {len(bus_i.passenger_standing_list)} passengers standing")

        # logic to send buses from available_list
        if (self.policy(time) and len(self.available_bus_list) > 0):
            bus_to_be_sent = self.available_bus_list.pop(0)
            bus_to_be_sent.reset()
            self.running_bus_list.append(bus_to_be_sent)
            log.debug(
                f'Sending bus #{bus_to_be_sent.bus_number} at time {time}.')
            depot.trips += 1

        return self.running_bus_list
