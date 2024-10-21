from main import run_iteration

import random

import logging as log
log.basicConfig(filename="genetic_algorithms_with_adaptive_fitness.txt", filemode="w",
                format='%(message)s', level=log.INFO)


# Define the parameters
population_size = 150
num_generations = 500
mutation_rate = 0.3
value_length = 15  # number of values in the array
num_values = 5
numeps = 100


def create_population(size, length, num_values):
    return [[random.randint(1, num_values-1) for _ in range(length)] for _ in range(size)]


def evaluate_population(population, generation: int):
    factor = generation//4
    factor = min(factor, 8)
    return [max((run_iteration(individual, numeps)[0]-factor), 0)**2 for individual in population]


def select_parents(population, fitness):
    selected = random.choices(population, weights=fitness, k=2)
    return selected


def crossover(parent1, parent2):
    crossover_point = random.randint(1, value_length - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        mutation_point = random.randint(1, value_length - 1)
        individual[mutation_point] = random.randint(1, num_values-1)
    return individual


# Step 1: Initialize population
population = create_population(population_size, value_length, num_values)

# Step 2-6: Evolve over generations
for generation in range(num_generations):
    # Step 2: Evaluate fitness
    fitness = evaluate_population(population, generation)

    print(fitness)

    # Step 3: Select parents
    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = select_parents(population, fitness)

        # Step 4: Crossover
        child1, child2 = crossover(parent1, parent2)

        # Step 5: Mutation
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)

        new_population.extend([child1, child2])

    # Replace the old population with the new one
    population = new_population

log.info("Finished evolving...")
# Step 7: Output the best solution
best_individual = max(population, key=lambda value: run_iteration(value, 100))
best_fitness = run_iteration(best_individual, numeps)
log.info(f"Best in current population is {best_fitness}")

log.info(f"Best individual: {best_individual}")
log.info(f"Best fitness: {best_fitness}")
