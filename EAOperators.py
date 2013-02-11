import random
from FitnessEval import FitnessEval
import sys
#Create and contain the population for the EA
class Population:
    
    nr_of_bits = 20;
    population_size = 0;
    population = []
    
    def __init__(self, nr_of_bits, population_size):
        if(nr_of_bits):
            self.nr_of_bits = nr_of_bits
        self.population_size = population_size
        
        
    #Create a random population of solutions as bitstrings (genotype)
    def create_population(self):
        for i in range(0, self.population_size):
            specimen = random.getrandbits(self.nr_of_bits)
            self.population.append(specimen)
        return self.population


#Develop the individuals from genotype to phenotype  
class Development:
    
    def development(self, genotype, nr_of_bits):
        phenotype = []
        genotype = int(genotype)
        for _ in range(0, nr_of_bits):
            phenotype.insert(0, genotype % 2)
            genotype = genotype/2
        return phenotype
        

#Contains the different selection protocols
#and selection mechanisms  
class Selection:
    

    #Set which selection protocol to use
    def set_selection_protocol(self):
        return False
        
    #SELECTION PROTOCOLS
    def full_gen_replacement(self, population, new_generation):
        return new_generation
        
    def over_production(self):
        return False
    
    def generational_mixing(self):
        return False
        
        
        
    #Set which selection mechanism to use
    def set_selecton_mechanism(self):
        return False
    
    #SELECTION MECHANISMS    
    def fitness_proportionate(self, population_fitness):
        expected_mating = []
        average_fitness = sum(population_fitness)/len(population_fitness)
        mating_wheel = []
        for i in range(0, population_fitness):
            expected_mating = round(population_fitness[i]/average_fitness)
            for n in range(0, expected_mating):
                mating_wheel.append(i) #Indexes
            
        #THEN SPIN ZE WHEEEEL
        reproducers = []
        for _ in range(0, len(population_fitness)):
            reproducers.append( mating_wheel[random.randint(0,len(mating_wheel)-1)] )
        
        
                
    def sigma_scaling(self, population_fitness):
        return False
        
    def boltzman(self):
        return False
        
    def rank(self):
        return False
    
    #Selects the index of the reproducers in the population by means of local k-tournament, currently only works on popsizes divisible by k
    #TODO: with propability e, pick another winner in group
    def k_tournament(self, population_fitness, k, e):
        reproducers = []
        group_k = k
        for i in range(0, len(population_fitness)):
            if i == group_k-1:
                #FACE-OFF!
                tournament_group = population_fitness[(i-(k-1)):group_k]
                if random.random()<e:
                    reproducers.append( random.randint(0, k-1) + (group_k-k) )
                else:
                    reproducers.append( tournament_group.index(max(tournament_group)) + (group_k-k) )
                group_k = group_k + k
        return reproducers
        

#Perform genetic operations on the genotype
class GeneticOperators:

    mutation_prob = 0
    
    def __init__(self, mutation_prob):
        self.mutation_prob = mutation_prob
        
    #Randomly mutate the genotype,
    #i.e. pick a random bit and flip it
    def mutate(self, genotype, nr_of_bits):
        if random.random() < self.mutation_prob:
            mutated_genotype = genotype ^ (1 << random.randint(0, nr_of_bits))
        else:
            mutated_genotype = genotype
        return mutated_genotype
        
    #Perform crossover on genotypes
    def crossover(self):
        return False


if __name__ == '__main__':
    
    Development().development(0b11111101111111111111, 20)
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

    