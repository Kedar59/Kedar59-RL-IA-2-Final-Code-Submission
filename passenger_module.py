
import secrets

import logging as log


class passenger:
    total_waiting_time = 0
    total_standing_time = 0
    passenger_count = 0

    def __init__(self, source: int, destination: int):
        self.source = source
        self.destination = destination
        self.waiting_time: int = 0
        self.standing_time: int = 0
        self.sitting_time: int = 0
        hex_string = secrets.token_hex(8)
        self.name = hex_string
        log.debug(
            f'New passenger {self.name} came at stop {self.source} who wants to go to  destination {self.destination}.')

    def end(self, time):
        log.debug(f'Passenger {self.name} from source {self.source} reached destination {self.destination} at time {time}. Waiting time: {self.waiting_time}, standing time: {self.standing_time}, sitting time: {self.sitting_time}')
        passenger.total_waiting_time += self.waiting_time
        passenger.total_standing_time += self.standing_time
        passenger.passenger_count += 1
        pass
