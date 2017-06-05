"""NSGA-2 related utility functions
   These are used in module evolution.py"""

import functools
from nsga2.population import Population
import random

class NSGA2Utils(object):

    def __init__(self, problem,population_size, mutation_rate=0.2, num_of_genes_to_mutate=5,tournament_size=2):

        self.problem = problem
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.number_of_genes_to_mutate = num_of_genes_to_mutate
        self.tournament_size = tournament_size

    def fast_nondominated_sort(self, population):
        """This functions is used to sort the population into non dominated frontiers """
        population.fronts = []
        population.fronts.append([])
        #assign domination count and set dominated solutions to empty set
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()

            for other_individual in population:
                #if individual dominates other indiv
                if individual.dominates(other_individual):
                    #add it to the list of domianted individuals
                    individual.dominated_solutions.add(other_individual)
                #if the other individual dominates the individual
                elif other_individual.dominates(individual):
                #increment the domination count
                    individual.domination_count += 1
            #if the domination count is zero - it is appeneded to the first front
            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0
        i = 0
        #the rest of the fronts are built
        while len(population.fronts[i]) > 0:
            front = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        front.append(other_individual)
            i = i+1
            population.fronts.append(front)

    def __sort_objective(self, val1, val2, m):
        return cmp(val1.objectives[m], val2.objectives[m])

    def calculate_crowding_distance(self, front):
        """Sets the crowding distance for each individual in a frontier """
        #Check if front length is more than 1, if it is the length is stored in a variable
        if len(front) > 0:
            solutions_num = len(front)
            #This sets the crowding distance for all individuals to 0
            for individual in front:
                individual.crowding_distance = 0
            #for each objective, the crowding distance is assigned to the individuals
            for m in range(len(front[0].objectives)):
                front = sorted(front, cmp=functools.partial(self.__sort_objective, m=m))
                #the first and last individuals are assigned their maximum values
                front[0].crowding_distance = self.problem.max_objectives[m]
                front[solutions_num-1].crowding_distance = self.problem.max_objectives[m]
                for index, value in enumerate(front[1:solutions_num-1]):
                    diff=front[index+1].crowding_distance - front[index-1].crowding_distance
                    obj_diff=self.problem.max_objectives[m] - self.problem.min_objectives[m]
                    front[index].crowding_distance = diff/obj_diff

    def crowding_operator(self, individual, other_individual):
        """ This is a crowding operator """"
        #variables to hold individual comparisons
        rank_less=(individual.rank < other_individual.rank)
        ranks_equal=(individual.rank == other_individual.rank)
        crowd_more=(individual.crowding_distance > other_individual.crowding_distance)
        #if the individuals rank is less than the others, it is considered to have higher order
        #if the ranks are equal and the crowding distance is higher - this also merits higher order
        if rank_less or ((ranks_equal and crowd_more)):
            return 1
        else:
            return -1


    def __crossover(self, individual,other_individual):

        #check whether individuals are empty or not
        if individual == None:
            raise ValueError

        if other_individual==None:
            raise ValueError

        #Generate children
        child1 = self.problem.generateIndividual()
        child2 = self.problem.generateIndividual()
        #Generate list of gene indexes
        genes_indexes = range(len(child1.genes))
        half_genes_indexes = random.sample(genes_indexes, 1)
        #compare gene index with sublist of indexes to simulate crossover
        for i in genes_indexes:
            if i in half_genes_indexes:
                #swap genes
                child1.genes[i] = individual2.genes[i]
                child2.genes[i] = individual1.genes[i]
            else:
                #swap genes
                child1.genes[i] = individual1.genes[i]
                child2.genes[i] = individual2.genes[i]
        return child1, child2


    def __mutate(self, child):
        #select the genes to mutute
        genes_to_mutate = random.sample(range(0, len(child.genes)), self.number_of_genes_to_mutate)
        #mutation forumla to subtract from child genes
        formula= self.mutation_rate/2 + random.random() * self.mutation_rate
        #mutation
        for gene in genes_to_mutate:
            child.genes[gene] = child.genes[gene] - formula
            if child.genes[gene] < 0:
                child.genes[gene] = 0
            elif child.genes[gene] > 1:
                child.genes[gene] = 1

    def __tournament(self, population):
        #select individuals from the population up to tournament sie
        participants = random.sample(population, self.tournament_size)
        best = None
        #tournament selection
        for participant in participants:
            if best is None or self.crowding_operator(participant, best) == 1:
                best = participant

        return best
