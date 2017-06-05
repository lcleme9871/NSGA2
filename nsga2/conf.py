class Conf(object):

    def __init__(self,problem,population_size,num_of_generations,mutation_rate,crossover_rate):
        self.problem=problem
        self.population_size=population_size
        self.num_of_generations=num_of_generations
        self.mutation_rate=mutation_rate
        self.crossover_rate=crossover_rate

    def hello(self,line):
        print("hello ",line)
