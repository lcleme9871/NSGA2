"""Module with main parts of NSGA-II algorithm.
Contains main loop"""

from nsga2.utils import NSGA2Utils
from nsga2.conf import Conf
from nsga2.population import Population

class Evolution(object):

    def __init__(self,conf):
        self.conf=conf
        self.utils = NSGA2Utils(conf.problem,conf.population_size)
        self.population = None
        self.on_generation_finished = []


    def register_on_new_generation(self, fun):
        """This method sets a function """
        self.on_generation_finished.append(fun)


    def evolve(self):
        """Performs the main function of the NSGA-2 non-dominated sorting algorithm """
        #create inital population
        self.population = create_initial_population()
        #sort by fast_nondominated_sort
        self.utils.fast_nondominated_sort(self.population)
        #Assign the crowding distance
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        #create child population
        children = []
            #length of children must be shorter than original population
        while len(children) < len(population):
            #select parent1 by tournament selection
            parent1 = self.utils.__tournament(population)
            parent2 = parent1
            #parent1 and parent2 must not be duplicates, so this predicated is needed
            while parent1.genes == parent2.genes:
                parent2 = self.utils.__tournament(population)
            #crossover
            child1, child2 = self.utils.__crossover(parent1, parent2)
            #mutation
            self.utils.__mutate(child1)
            self.utils.__mutate(child2)
            #calculate objective values
            self.conf.problem.calculate_objectives(child1)
            self.conf.problem.calculate_objectives(child2)
            #Append to list
            children.append(child1)
            children.append(child2)

        final_population = None
        #main loop
        for i in range(self.conf.num_of_generations):
            #create a union between both populations
            self.population.union(children)
            #sort the union by fast_nondominated_sort
            self.utils.fast_nondominated_sort(self.population)
            #initalise variables
            new_population = Population()
            front_num = 0
            #If there is space left over, it needs to be filled
            while len(new_population) + len(self.population.fronts[front_num]) <= self.conf.population_size:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.union(self.population.fronts[front_num])
                front_num += 1

            #sort the front by the crowding comparison operator
            sorted(self.population.fronts[front_num], cmp=self.utils.crowding_operator)
            new_population.union(self.population.fronts[front_num][0:self.conf.population_size-len(new_population)])
            #Assign populations
            final_population = self.population
            self.population = new_population
            children = create_children(self.population)
            # for all functions
            for fun in self.on_generation_finished:
                fun(final_population, i)
            # return the best individuals
        return final_population.fronts[0]

    def create_initial_population(self):
        """Creates an inital population """
        #A new population is created
        population = Population()
        #iteration till the end of the populations size
        for _ in range(self.conf.population_size):
            #An individual is created from the problem
            individual = self.conf.problem.generateIndividual()
            #objective values are calculated and individual is added to the new populaton
            self.conf.problem.calculate_objectives(individual)
            population.population.append(individual)

        return population
