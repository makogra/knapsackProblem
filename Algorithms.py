from random import random

from Chromosome import Chromosome


def score(knapsack_problem = None, chromosome = None):
    total_value = 0
    total_weight = 0

    for index, gene in enumerate(chromosome.gens):
        if gene:
            total_value += knapsack_problem.data[index][0]
            total_weight += knapsack_problem.data[index][1]

    if total_weight > knapsack_problem.weight:
       return 0
    return total_value


def mutation(procentage = None, chromosome = None):
    if 0 > procentage > 1:
        print("Procentage must be in (0,1)")
        return chromosome

    mutated_chromosome = []
    for i in range(len(chromosome.gens)):
        mutated_chromosome.append(chromosome.get(i))
        if procentage > random():
            mutated_chromosome[i] = not mutated_chromosome[i]

    return Chromosome(mutated_chromosome)


def one_point_crossover(chromosome1 = None, chromosome2 = None):
    index = round(len(chromosome1.gens) * random())
    crossover_product = chromosome1.gens[:index] + chromosome2.gens[index:]

    return Chromosome(gens=crossover_product)

def crossover_executor(procentage = None, crossover_implementation = None, chromosome1 = None, chromosome2 = None):
    if procentage > random():
        return crossover_implementation(chromosome1, chromosome2)
    return chromosome1

def rullet_selection(population = None):
    new_population = []
    total_score = 0
    for chromosome in population:
        total_score += chromosome.score

    for _ in range(len(population)):
        rullet_spin = total_score * random()
        i = 0
        while rullet_spin > 0:
            rullet_spin -= population[i].score
            i += 1
        new_population.append(population[i-1])

    return new_population

class Algorithms:
    pass