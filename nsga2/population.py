"""Module with part of the NSGA-2 definition
   This module contains the Population definition"""


class Population(object):
    """Represents a population.
       A Population contains a set of individuals
       - more individuals can be added, using Union """"

    def __init__(self):
        self.population = []
        self.fronts = []

    def __len__(self):
        """ This returns the length of the population """"
        return len(self.population)

    def __iter__(self):
        """Allows for iterating over Individuals"""

        return self.population.__iter__()

    def union(self,individuals_to_add):
        """Creates a union of old individuals and newer ones"""

        self.population.union(individuals_to_add)
