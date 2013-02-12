import random
from FitnessEval import FitnessEval
import sys
from abc import*

class Individual:
    
    @abstractmethod
    def mutate(self, mutation_prob): pass
    
    @abstractmethod
    def crossover(self, other): pass
    
    @abstractmethod
    def development(self): pass
    
    @abstractmethod
    def set_fitness(self, fitness):
        self.fitness = fitness

#A Individual in the population
class OneMaxIndividual(Individual):

    nr_of_bits = 40
    
    def __init__(self, genotype=None):
        self.fitness = 0
        self.phenotype = []
        if genotype is None:
            self.random_genotype()
        else:
            self.genotype=genotype
            
    def __str__(self):
        return str(self.phenotype)
        
    def __repr__(self):
        return self.__str__()
    
    def random_genotype(self):
        self.genotype = random.getrandbits(self.nr_of_bits)
                 
    #Mutate the genotypes, with a probability of mutation_prob  
    def mutate(self, mutation_prob):
        if random.random() < mutation_prob:
            self.genotype = self.genotype ^ (1 << random.randint(0, self.nr_of_bits))
        else:
            self.genotype = self.genotype
        return self.genotype
        
    #Perform crossover on genotypes
    def crossover(self, other):
        crossover_range = (2, 5)
        splits = [(i % 2, random.randint(*crossover_range)) for i in range(self.nr_of_bits / crossover_range[0])]
        
        genotypes = (self.num_to_bitstring(self.genotype), self.num_to_bitstring(other.genotype))
        
        new_genotype = []
        index = 0
        for individual, n_genes in splits:
            to_index = min(index+n_genes, self.nr_of_bits)
            new_genotype.append(genotypes[individual][index:to_index])
            
            if to_index >= self.nr_of_bits:
                break
            
            index += n_genes
        
        return Individual(int("".join(new_genotype), 2))
    

    #Develop the individual from genotype to phenotype  
    def development(self):
        gtype = int(self.genotype)
        
        for _ in range(0, self.nr_of_bits):
            self.phenotype.insert(0, gtype % 2)
            gtype = gtype/2
            
    def num_to_bitstring(self, n, l=20):
        return bin(n)[2:].zfill(l)


#if __name__ == '__main__':
#    
#    
#    # 1. Create initial random population, develop to phenotype
#    # 2. Evaluate the fitness of each individual in the Population, do we have solution?
#    # 3. Select the individuals to reproduce
#    # 4. Create offspring genotypes
#    # 5. Mutate and crossover
#    # 6. Make new population i.e. develop new generation and kill old one
#    # 7. Back to step 2.
#        
#    nr_of_bits = 20
#    population_size = 10000
#    #Create initial population genotype
#    population_genotype = Population(nr_of_bits, population_size).create_population()
#    
#    #Develop
#    population = []
#    for p in population_genotype:
#        population.append(Development().development(p, nr_of_bits))
#    
#    for i in range(0, 600):
#        #Fitness
#        population_fitness = []
#        for p in population:
#            population_fitness.append(FitnessEval().calc_fitness(p))
#            
#        solution = max(population_fitness)
#        if solution ==nr_of_bits:
#            print "SOLUTION FOUND"
#            sys.exit()
#            
#        if((i%10) == 0):
#            print "GENERATION:: " +str(i)
#            print "Max fitness: "+str(max(population_fitness))
#            print "Avg fitness: "+str( (sum(population_fitness)/len(population_fitness)) )
#        
#        #Selection of reproducing adults
#        k = 5
#        reproducers = Selection().k_tournament(population_fitness, k)
#        
#        #Reproduce: Create children genotypes from reproducing adults, reproducers get to reproduce alot here!
#        children_genotypes = []
#        for n in range(0, k):
#            for i in reproducers:
#                children_genotypes.append(population_genotype[i])
#        
#        #Mutate & Crossover
#        mutated_genotypes = []
#        for i in children_genotypes:
#            mutated_genotypes.append(GeneticOperators().mutate(i, nr_of_bits))
#            
#        #Develop
#        new_generation = []
#        for i in mutated_genotypes:
#            new_generation.append(Development().development(i, nr_of_bits))
#        
#        #Selection Protocol
#        population = Selection().full_gen_replacement(population, new_generation)
#        population_genotype = children_genotypes
#        
#        #START OVER MAKE A FOR FFS! GTG!