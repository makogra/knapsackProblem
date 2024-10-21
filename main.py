from random import random

from Algorithms import crossover_executor, score, rullet_selection, one_point_crossover, mutation
from Chromosome import Chromosome
from KnapsackProblem import KnapsackProblem

def print_optimum_solution(file_name):
    direction, problem = file_name.split("/")
    direction += "-optimum"

    with open("./dane_AG/" + direction + "/" + problem, "r") as file:
        print("Optimal solution = " + file.readline())

# Extract data from file
def import_knapsack_problem_from_file(file_name):
    print_optimum_solution(file_name)

    with open("./dane_AG/" + file_name, "r") as file:
        size, weight = file.readline().split(" ")
        data = []
        for line in file.readlines():
            # print("line = " + line)
            value_weight_pair = [float(numeric_string) for numeric_string in line.split(" ")]
            # data.append(line.split(" "))
            data.append(value_weight_pair)

    return KnapsackProblem(size, weight, data)

def setup_population(population_size, knapsack_problem):
    population = []
    for _ in range(population_size):
        chromosome = Chromosome()
        chromosome.init_gens_including_max_weight(knapsack_problem)

        population.append(chromosome)
    return population


def get_best_score(population, score_function, knapsack_problem):
    best_score = 0
    for chromosome in population:
        best_score = max(best_score, score_function(knapsack_problem, chromosome))
    return best_score


def simulate(knapsack_problem, population_size, number_of_iterations, score, selection, crossover, crossover_procentage, mutation, mutation_procentage):
    population = setup_population(population_size, knapsack_problem)
    scores_log = []
    #score init population
    scores_log.append(get_best_score(population, score, knapsack_problem))
    for _ in range(number_of_iterations):
        current_best_score = 0
        for index, chromosome in enumerate(population):
            # look for crossover
            index_for_crossover = round(population_size * random()) -1
            population[index] = crossover_executor(crossover_procentage, crossover, chromosome, population[index_for_crossover])

            # look for mutation
            population[index] = mutation(mutation_procentage, population[index])

            # set scorres
            population[index].score = score(knapsack_problem,population[index])

            # find best score for logging
            current_best_score = max(current_best_score, population[index].score)

        # log best value for iteration
        scores_log.append(current_best_score)

        # exaciute selection
        population = selection(population)


    print("final score = " + str(scores_log[-1]))
    print("whole score log: " + str(scores_log))

def solve_problem():
    problem = import_knapsack_problem_from_file("low-dimensional/f10_l-d_kp_20_879")
    # problem = import_knapsack_problem_from_file("large_scale/knapPI_1_1000_1000_1")
    population_size = 200
    number_of_iterations = 200
    #chanse for each chromosome to perform crossover - one roll per chromosome
    crossover_procentage = 0.30
    # roll for every gene in every chromosome
    mutation_procentage = 0.01

    # Notes:
    # - jak masz jakieś sugestie czy coś to pisz tutaj i daj tylko znać na messangerze
    # - chcemy dodawać mieć możliwość dawania seed'a dzięki czemu algorytm będzie deterministyczny i będzie można
    # zobaczyć jak wpływają zmiany parametrów na niego?

    simulate(problem, population_size, number_of_iterations, score, rullet_selection,
             one_point_crossover, crossover_procentage, mutation, mutation_procentage)


if __name__ == '__main__':
    solve_problem()
