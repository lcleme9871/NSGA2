"""Module with part of the NSGA-2 definition
   This module contains the Individual definition"""

class Individual(object):
    """Represents one individual"""

    def __init__(self):
        self.rank = None
        self.crowding_distance = None
        self.dominated_solutions = set()
        self.genes = None
        self.objectives = None
        self.dominates = None

    def set_objectives(self, objectives):
        self.objectives = objectives
