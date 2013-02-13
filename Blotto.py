from abc import*
from Individual import*

class Blotto(Individual):
    
    B = 5 #The number of battles to be fought
    S = 100 #The total number of resources at disposal
    strength_factor = 1.0 
    
    
    def __init__(self, genotype=None):
        self.genotype = []
        self.phenotype = []
        self.fitness = 0
        if genotype is None:
            self.random_genotype()
        
        
    #Increment or decrement a random list element in genotype
    @abstractmethod
    def mutate(self, mutation_prob):
        index = random.randint(1,self.B-1)
        probability = random.random()
        if probability<mutation_prob/2:
            if not self.genotype[index] is 0: 
                self.genotype[index]+=1
            else: 
                self.genotype[index]-=1
        elif probability<mutation_prob:
            if self.genotype[index] is 10:
                self.genotype[index]-=1
            else:
                self.genotype[index]+=1
        
    @abstractmethod
    def crossover(self, other):
        Individual.crossover(self, other)
        
    #Convert the 0-10 weights to resources, i.e. normalize then multiply by S
    @abstractmethod
    def development(self):
        genotype_sum = sum(self.genotype)
        self.phenotype = [(i*1.0/genotype_sum)*self.S for i in self.genotype]
       
    #The initial genotype is a list of B random weights from 0 to 10 
    def random_genotype(self):
        self.genotype = [random.randint(0,10) for _ in range(0,self.B)]
        
if __name__ == '__main__':
    blotto = Blotto()
    print blotto.genotype
    blotto.development()
    print blotto.phenotype
    blotto.mutate(0.8)
    print blotto.genotype
    