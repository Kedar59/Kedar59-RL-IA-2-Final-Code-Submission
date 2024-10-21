import random
import pandas as pd
from bus_stop_module import bus_stop
from depot_module import depot

import logging as log


def initialize():

    arrival_day_probability = get_arrival_day_probability()

    arrival_day = random.choices(
        population=arrival_day_probability[:][0], weights=arrival_day_probability[:][1])[0]
    log.debug(f"Today is a day with rush factor {arrival_day}")

    traffic_day_probability = get_traffic_day_probability()
    traffic_day = random.choices(
        population=traffic_day_probability[:][0], weights=traffic_day_probability[:][1])[0]
    log.debug(f"Today is a day with traffic factor {traffic_day}")

    sprawn_probability_matrix = get_sprawn_probability_matrix()

    travel_time_probability_matrix = get_travel_time_probability_matrix()

    destination_probability_matrix = get_destination_probability_matrix()

    max_capacity = 75
    log.debug(f"Max capacity of the bus is {max_capacity}")

    sitting_capacity = 35
    log.debug(f"Bus has {sitting_capacity} seats.")

    total_buses = 8

    log.debug(f"Total there are {total_buses} buses.")

    stop_list: list[bus_stop] = []

    for i in range(len(sprawn_probability_matrix)):
        stop_list.append(bus_stop(stop_number=i, sprawn_probability_matrix=sprawn_probability_matrix,
                         destination_probability_matrix=destination_probability_matrix))
    main_depot = depot(max_capacity=max_capacity, sitting_capacity=sitting_capacity, stops_list=stop_list,
                       travel_time_matrix=travel_time_probability_matrix, total_busses=total_buses)
    return stop_list, arrival_day, traffic_day,    main_depot


def get_arrival_day_probability():
    df = pd.read_csv('data/arrival_day_types.csv')
    arrival_day_probability = df.iloc[:, 1:].values.tolist()
    # Transpose the list of lists
    arrival_day_probability = list(map(list, zip(*arrival_day_probability)))

    return arrival_day_probability


def get_traffic_day_probability():
    df = pd.read_csv('data/traffic_day_types.csv')
    traffic_day_probability = df.iloc[:, 1:].values.tolist()

    # Transpose the list of lists
    traffic_day_probability = list(map(list, zip(*traffic_day_probability)))
    return traffic_day_probability


def get_sprawn_probability_matrix():
    df = pd.read_csv('data/sprawn_probability_matrix.csv')
    sprawn_probability_matrix = df.iloc[:, 2:].values.tolist()
    sprawn_probability_matrix = list(
        map(list, zip(*sprawn_probability_matrix)))

    return sprawn_probability_matrix


def get_travel_time_probability_matrix():
    df = pd.read_csv('data/travel_time_matrix.csv')
    travel_time_probability_matrix = df.iloc[:, 2:-1].values.tolist()

    return travel_time_probability_matrix


def get_destination_probability_matrix():
    df = pd.read_csv('data/destination_probability_matrix.csv')
    destination_probability_matrix = df.iloc[:, 1:].values.tolist()
    # Transpose the matrix
    destination_probability_matrix = list(
        map(list, zip(*destination_probability_matrix)))
    # Replace "-" with 0 and convert to float
    destination_probability_matrix = [
        [float(0) if cell == "-" else float(cell) for cell in row]
        for row in destination_probability_matrix
    ]
    return destination_probability_matrix


