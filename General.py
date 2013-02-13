from abc import*
from EA import*
from Individual import*

class General(Individual):
    
    def __init__(self, genotype=None):
        if genotype is None:
            self.random_genotype()
        
    @abstractmethod
    def mutate(self, mutation_prob):
        Individual.mutate(self, mutation_prob)
        
    @abstractmethod
    def crossover(self, other):
        Individual.crossover(self, other)
        
    @abstractmethod
    def development(self):
        Individual.development(self)
        
    def random_genotype(self):
        self.genotype = None