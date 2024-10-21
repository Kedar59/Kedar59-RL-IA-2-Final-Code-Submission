import numpy as np
from passenger_module import passenger

import random
import logging as log


class bus_stop:

    def __init__(self, stop_number: int, sprawn_probability_matrix: list[list[float]], destination_probability_matrix: list[list[float]]):
        self.number = stop_number
        self.sprawn_probability: list[float] = sprawn_probability_matrix[stop_number]
        self.destination_probability: list[float] = destination_probability_matrix[stop_number]
        self.sprawn_variance = self.sprawn_probability[-1]
        self.queue: list[passenger] = []

    def add_passenger(self, destination) -> None:
        new_passenger = passenger(source=self.number,
                                  destination=destination)
        self.queue.append(new_passenger)

    def sprawn_passengers(self, time: int, arrival_day: float) -> None:
        mean: float = arrival_day+self.sprawn_probability[time//60]
        no_passengers_arriving = np.random.poisson(mean/60)

        log.debug(
            f"{no_passengers_arriving} passengers arrived at bus stop #{self.number} at time {time}")
        for i in range(0, no_passengers_arriving):
            random_destination: int = random.choices(
                population=range(len(self.destination_probability)), weights=self.destination_probability)[0]
            self.add_passenger(destination=random_destination)

    def fill_passengers(self, bus) -> None:
        # choose random passengers from queue and add them to the bus
        capacity = bus.get_capacity()
        k = min(capacity, len(self.queue))
        passengers = random.sample(population=self.queue, k=k)
        count = 0
        for passenger_i in passengers:
            self.queue.remove(passenger_i)
            count += 1
            bus.add_passenger(passenger_i)
        log.debug(
            f"Bus #{bus.bus_number} filled in {count} passengers at stop number {self.number}")

    def advance(self, time: int, arrival_day):
        self.sprawn_passengers(time, arrival_day)
        for passenger_i in self.queue:
            passenger_i.waiting_time += 1

    def end(self, time: int):
        # last passengers who remain waiting till the end
        for passenger_i in self.queue:
            passenger_i.end(time)
