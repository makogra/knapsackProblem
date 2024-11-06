from random import random, Random


class Chromosome:
    def __init__(self, gens = None, score = 0.0):
        self.gens = gens
        self.score = score

    def get(self, index):
        return self.gens[index]

    def init_gens(self, size):
        gens = []
        for _ in range(size):
            gens.append(bool(random()>=0.5))
        self.gens = gens

    def init_gens_including_max_weight(self, knapsack_problem):
        gens = []
        total_weight = 0
        max_weight = knapsack_problem.weight
        for index in range(knapsack_problem.size):
            gen = bool(random() >= 0.5)
            if total_weight + knapsack_problem.data[index][1] <= max_weight:
                total_weight += knapsack_problem.data[index][1]
                gens.append(gen)
            else:
                gens.append(False)
        self.gens = gens

    def init_gens_including_max_weight_by_repetition(self, knapsack_problem):
        gens = []
        max_weight = knapsack_problem.weight
        total_weight = max_weight + 1
        while total_weight > max_weight:
            total_weight = 0
            gens = []
            total_weight = 0
            for index in range(knapsack_problem.size):
                gen = bool(random() >= 0.5)
                if gen:
                    total_weight += knapsack_problem.data[index][1]
                gens.append(gen)
        self.gens = gens

    def __str__(self):
        return f"Last updated score: {self.score}, genomes: {str(self.gens)}"

