from random import random
from tokenize import group

from Chromosome import Chromosome
from KnapsackProblem import KnapsackProblem


def score(knapsack_problem: KnapsackProblem, chromosome: Chromosome):
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
    crossover_product1 = chromosome1.gens[:index] + chromosome2.gens[index:]
    crossover_product2 = chromosome2.gens[:index] + chromosome1.gens[index:]

    return [Chromosome(gens=crossover_product1), Chromosome(gens=crossover_product2)]


def two_point_crossover(chromosome1 = None, chromosome2 = None):
    one_point = one_point_crossover(chromosome1, chromosome2)
    return one_point_crossover(one_point[0], one_point[1])


def crossover_executor(procentage = None, crossover_implementation = None, chromosome1 = None, chromosome2 = None):
    if procentage > random():
        return crossover_implementation(chromosome1, chromosome2)
    return [chromosome1, chromosome2]

def roulette_selection(population = None):
    new_population = []
    total_score = sum(chromosome.score for chromosome in population)

    for _ in range(len(population)):
        rullet_spin = total_score * random()
        i = 0
        while rullet_spin > 0 and i < len(population):
            rullet_spin -= population[i].score
            i += 1
        new_population.append(population[i-1])

    return new_population

def ranking_selection(population = None):
    new_population = []
    sorted_population = sorted(population, key=lambda item: item.score, reverse=True)

    for index, chromosome in enumerate(sorted_population):
        # https://www.desmos.com/calculator/e8acc8mzfz
        for _ in range(round(4*(1-2*index)/(1+len(population)))):
            new_population.append(chromosome)
    new_population = new_population[0:len(population)]
    return new_population

def tournament_selection(population = None):
    new_population = []
    group_size = 10

    while len(new_population) < len(population):
        tournament_group = []
        for _ in range(group_size):
            tournament_group.append(int(len(population) * random()))
        new_population.append(max(tournament_group))
    return new_population


class Algorithms:
    pass