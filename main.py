from functools import cmp_to_key
from itertools import product
from random import random

from Algorithms import crossover_executor, score, roulette_selection, one_point_crossover, mutation, ranking_selection, \
    tournament_selection
from Chromosome import Chromosome
from KnapsackProblem import KnapsackProblem

def print_optimum_solution(file_name):
    direction, problem = file_name.split("/")
    direction += "-optimum"

    with open("./dane_AG/" + direction + "/" + problem, "r") as file:
        result = "Optimal solution = " + file.readline()
    return result

# Extract data from file
def import_knapsack_problem_from_file(file_name):
    # print(print_optimum_solution(file_name))

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


def elites(population, no_elites):
    # Handle cases where no_elites is 0 or more than population length
    if no_elites <= 0:
        return []
    if no_elites >= len(population):
        return sorted(population, key=lambda item: item.score, reverse=True)

    # Select top `no_elites` items with the highest score
    chosen_elites = sorted(population, key=lambda item: item.score, reverse=True)[:no_elites]
    return chosen_elites


def simulate(knapsack_problem, population_size, number_of_iterations, score, selection, crossover, crossover_percentage, mutation, mutation_percentage, no_elites):
    population = setup_population(population_size, knapsack_problem)
    scores_log = []
    numbers_of_chromosomes_with_score_0 = []
    #score init population
    scores_log.append(get_best_score(population, score, knapsack_problem))
    # print("----------------------------------------------------------------------------------------")
    # print("Setup population: ")
    # for chro in population:
    #     print(chro)
    # print("----------------------------------------------------------------------------------------")
    first_iteration = True
    for _ in range(number_of_iterations):
        current_best_score = 0
        number_of_chromosomes_with_score_0_in_current_population = 0
        new_population = []

        update_population_scores(population, score, knapsack_problem)
        #save {no_elites} best scored chromosomes
        new_population.extend(elites(population, no_elites))
        look_for_crossover(crossover, crossover_percentage, population)
        look_for_mutation(mutation, mutation_percentage, population)
        update_population_scores(population, score, knapsack_problem)

        # exaciute selection
        population = new_population + selection(population)[:population_size - no_elites]

        # logging
        current_best_score, number_of_chromosomes_with_score_0_in_current_population = logging(current_best_score,
                                                                                               number_of_chromosomes_with_score_0_in_current_population,
                                                                                               population)
        # log best value for iteration
        scores_log.append(current_best_score)

        numbers_of_chromosomes_with_score_0.append(number_of_chromosomes_with_score_0_in_current_population)

    # print("final score = " + str(scores_log[-1]))
    # print("whole score log: " + str(scores_log))
    return ("whole score log: " + str(scores_log))
    # print("Nummer of chromosomes with score equals to 0 throughout each population: " + str(numbers_of_chromosomes_with_score_0))


def logging(current_best_score, number_of_chromosomes_with_score_0_in_current_population, population):
    for chromosome in population:
        current_best_score = max(current_best_score, chromosome.score)
        if chromosome.score == 0:
            number_of_chromosomes_with_score_0_in_current_population += 1
    return current_best_score, number_of_chromosomes_with_score_0_in_current_population


def look_for_mutation(mutation, mutation_procentage, population):
    for index in range(len(population)):
        population[index] = mutation(mutation_procentage, population[index])


def look_for_crossover(crossover, crossover_procentage, population):
    for index in range(len(population)):
        # Ensure index_for_crossover is within range and not equal to index
        index_for_crossover = index
        while index_for_crossover == index:
            index_for_crossover = int(len(population) * random())

        # Perform crossover and assign results to the population
        new_pair = crossover_executor(crossover_procentage, crossover, population[index], population[index_for_crossover])
        population[index], population[index_for_crossover] = new_pair[0], new_pair[1]


def update_population_scores(population, score, knapsack_problem):
    for index in range(len(population)):
        # print(f"last score for chromosome at index {index} = {population[index].score}")
        population[index].score = score(knapsack_problem, population[index])


def run_simulations():
    # Define parameter ranges
    population_sizes = [500]
    crossover_percentages = [0.5]
    mutation_percentages = [0.1]
    no_elites_values = [3]
    selection = [roulette_selection, ranking_selection, tournament_selection]

    # Define the knapsack problem instances
    knapsack_problems = [
        # Large-scale problems
        "large_scale/knapPI_1_10000_1000_1", "large_scale/knapPI_1_100_1000_1", "large_scale/knapPI_1_200_1000_1",
        "large_scale/knapPI_1_500_1000_1",
        "large_scale/knapPI_2_100_1000_1", "large_scale/knapPI_2_200_1000_1",
        "large_scale/knapPI_1_1000_1000_1", "large_scale/knapPI_1_2000_1000_1", "large_scale/knapPI_1_5000_1000_1",
        "large_scale/knapPI_2_1000_1000_1", "large_scale/knapPI_2_2000_1000_1", "large_scale/knapPI_2_500_1000_1",
        # # Low-dimensional problems
        "low-dimensional/f10_l-d_kp_20_879", "low-dimensional/f1_l-d_kp_10_269", "low-dimensional/f2_l-d_kp_20_878",
        "low-dimensional/f3_l-d_kp_4_20", "low-dimensional/f4_l-d_kp_4_11", "low-dimensional/f5_l-d_kp_15_375",
        "low-dimensional/f6_l-d_kp_10_60", "low-dimensional/f7_l-d_kp_7_50", "low-dimensional/f8_l-d_kp_23_10000",
        "low-dimensional/f9_l-d_kp_5_80"
    ]

    # Iterate over every combination of parameters
    for problem_file in knapsack_problems:
        problem = import_knapsack_problem_from_file(problem_file)
        lines = []
        lines.append(print_optimum_solution(problem_file))

        # Generate all parameter combinations
        for population_size, crossover_percentage, mutation_percentage, no_elites, selection in product(
                population_sizes, crossover_percentages, mutation_percentages, no_elites_values, selection):
            # Define the number of iterations and any other static parameters
            number_of_iterations = 100

            # Run the simulation for the current parameter combination
            result = simulate(
                knapsack_problem=problem,
                population_size=population_size,
                number_of_iterations=number_of_iterations,
                score=score,
                selection=selection,
                crossover=one_point_crossover,
                crossover_percentage=crossover_percentage,
                mutation=mutation,
                mutation_percentage=mutation_percentage,
                no_elites=no_elites
            )
            lines.append(result)

            # Optional: Print or log the current configuration to track progress
            print(f"Completed simulation for {problem_file} with {selection} and parameters:")
            print(f"Population Size: {population_size}, Crossover %: {crossover_percentage}, "
                  f"Mutation %: {mutation_percentage}, Number of Elites: {no_elites}")

            lines.append(f"Population Size: {population_size}, Crossover %: {crossover_percentage}, "
                  f"Mutation %: {mutation_percentage}, Number of Elites: {no_elites}")
        with open("./results/" + problem_file, "w") as file:
            for line in lines:
                file.write(line)
                file.write("\n")


def solve_problem():
    problem = import_knapsack_problem_from_file("low-dimensional/f1_l-d_kp_10_269")
    # problem = import_knapsack_problem_from_file("large_scale/knapPI_1_1000_1000_1")
    population_size = 10
    number_of_iterations = 200
    #chanse for each chromosome to perform crossover - one roll per chromosome
    crossover_procentage = 0.5
    # roll for every gene in every chromosome
    mutation_procentage = 0.1
    no_elites = 3

    # Notes:
    # - jak masz jakieś sugestie czy coś to pisz tutaj i daj tylko znać na messangerze
    # - chcemy dodawać mieć możliwość dawania seed'a dzięki czemu algorytm będzie deterministyczny i będzie można
    # zobaczyć jak wpływają zmiany parametrów na niego?

    simulate(problem, population_size, number_of_iterations, score, roulette_selection,
             one_point_crossover, crossover_procentage, mutation, mutation_procentage, no_elites)


if __name__ == '__main__':
    run_simulations()
