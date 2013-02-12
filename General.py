from abc import*
from EA import*
from Individual import*

class General(Individual):
    
    def __init__(self, genotype=None):
        if genotype is None:
            self.random_genotype()
        
        
        
    def random_genotype(self):
        self.genotype = None