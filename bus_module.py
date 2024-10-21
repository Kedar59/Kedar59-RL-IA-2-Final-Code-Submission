import random
from passenger_module import passenger
from bus_stop_module import bus_stop
import logging as log


class bus:

    def __init__(self, bus_number: int, max_capacity: int, sitting_capacity: int, stops_list: list[bus_stop], travel_time_matrix: list[list[int]]):
        self.passenger_standing_list: list[passenger] = []
        self.passenger_sitting_list: list[passenger] = []
        self.max_capacity: int = max_capacity
        self.sitting_capacity: int = sitting_capacity
        self.time_till_next_stop: int = 0
        self.bus_number: int = bus_number
        self.stops_list: list[bus_stop] = stops_list
        self.next_stop: bus_stop = self.stops_list[0]
        self.travel_time_matrix: list[list[int]] = travel_time_matrix
        self.finished = False

    def reset(self):
        self.next_stop: bus_stop = self.stops_list[0]
        self.finished = False
        self.time_till_next_stop: int = 0

    def depart(self, stop: bus_stop, time: int):
        stop_number: int = stop.number
        counter = 0
        for passenger_i in self.passenger_standing_list[:]:
            if passenger_i.destination == stop_number:
                counter += 1
                self.passenger_standing_list.remove(passenger_i)
                passenger_i.end(time=time)

        for passenger_i in self.passenger_sitting_list[:]:
            if passenger_i.destination == stop_number:
                counter += 1
                self.passenger_sitting_list.remove(passenger_i)
                passenger_i.end(time=time)

        log.debug(
            f"{counter} passengers departed from bus #{self.bus_number} to stop number {stop_number} ")
        self.fill_seats()

    def fill_seats(self):

        # randomly make passengers in the standing list sit based on the capacity
        k = min(self.sitting_capacity - len(self.passenger_sitting_list),
                len(self.passenger_standing_list))
        passengers = random.sample(
            population=self.passenger_standing_list, k=k)
        for passenger in passengers:
            self.passenger_standing_list.remove(passenger)
            self.passenger_sitting_list.append(passenger)

    def add_passenger(self, passenger: passenger) -> None:
        self.passenger_standing_list.append(passenger)

    def get_capacity(self) -> int:
        return self.max_capacity - len(self.passenger_standing_list) - len(self.passenger_sitting_list)

    def calculate_time_till_next_stop(self, stop: bus_stop, time: int, day_type: int) -> int:

        mean: float = day_type+self.travel_time_matrix[time//60][stop.number]
        variance: float = self.travel_time_matrix[-1][stop.number]
        minimum: float = self.travel_time_matrix[-2][stop.number]
        time_till_next_stop: int = int(day_type*max(
            random.gauss(mean, variance), minimum))
        return time_till_next_stop

    def advance(self, time: int, day_type: int) -> None:
        # whenever this function is called, then the state changes.
        if (self.time_till_next_stop == 0):

            # bus comes at stop, passengers alight and new passegers come in.
            log.debug(
                f"Bus #{self.bus_number} arrived at stop number {self.next_stop.number} at time {time} where {len(self.next_stop.queue)} people are waiting")

            self.depart(self.next_stop, time)

            log.debug(
                f"Bus #{self.bus_number} has {len(self.passenger_sitting_list)} passengers sitting and {len(self.passenger_standing_list)} passengers standing")

            if self.next_stop.number == len(self.stops_list)-1:

                self.finished = True
                return
            else:
                self.next_stop.fill_passengers(self)

                self.time_till_next_stop = self.calculate_time_till_next_stop(
                    self.next_stop, time, day_type)
                self.next_stop = self.stops_list[self.next_stop.number + 1]

        else:
            self.time_till_next_stop -= 1

            for passenger in self.passenger_sitting_list[:]:
                passenger.sitting_time += 1
            for passenger in self.passenger_standing_list[:]:
                passenger.standing_time += 1
