
import sys
from FitnessEval import FitnessEval
from EAOperators import Selection
from EAOperators import Population
from EAOperators import Development
from EAOperators import GeneticOperators
from Plotting import Plotting

class EA:
    
    population_size = 20
    generations = 200
    generation = 0
    nr_of_bits = 30
    k = 4
    e = 0.2
    mutation_probability = 0.8
    population_genotype = []
    population_fitness = []
    mutated_genotypes = []
    new_generation = []
    reproducers = []
    population = []
    
    develops = None
    selects = None
    operates = None
    populates = None
    fitness = None
    
    def __init__(self):
        self.develops = Development()
        self.selects = Selection()
        self.operates = GeneticOperators(self.mutation_probability)
        self.populates = Population(self.nr_of_bits, self.population_size)
        self.fitness = FitnessEval()
        self.plotter = Plotting(self)
        
    def create(self):
        self.population_genotype = self.populates.create_population()
    
    def develop(self):
        for p in self.population_genotype:
            self.population.append(self.develops.development(p, self.nr_of_bits))
    
    
    def select(self):
        self.population_fitness = []
        for p in self.population:
            self.population_fitness.append(self.fitness.calc_fitness(p))
            
        solution = max(self.population_fitness)
        if solution == self.nr_of_bits:
            print "SOLUTION FOUND: "+str(solution)+ " " +str( self.population[ self.population_fitness.index(solution)] )
            sys.exit()
            
        if((self.generation%10) == 0):
            print "GENERATION:: " +str(self.generation)
            print "Max fitness: " +str(solution) +": " + str(self.population[self.population_fitness.index(solution)])
            print "Avg fitness: " +str( (sum(self.population_fitness)/len(self.population_fitness)) )
        
    
        self.reproducers = self.selects.k_tournament(self.population_fitness, self.k, self.e)
    
    def reproduce(self):
        self.children_genotypes = []
        for _ in range(0, self.k):
            for i in self.reproducers:
                self.children_genotypes.append(self.population_genotype[i])
        print self.children_genotypes
    
    def operate(self):
        self.mutated_genotypes = []
        for i in self.children_genotypes:
            self.mutated_genotypes.append(self.operates.mutate(i, self.nr_of_bits))
            
    
    def replace(self):
        new_generation = []
        for i in self.mutated_genotypes:
            new_generation.append(self.develops.development(i, self.nr_of_bits))
        self.generation += 1
        self.population = Selection().full_gen_replacement(self.population, new_generation)
        self.population_genotype = self.children_genotypes
        
    
        
        
    
if __name__ == '__main__':
    ea = EA()
    ea.create()
    ea.develop()
    for _ in range(0, ea.generations):
        ea.select()
        ea.reproduce()
        ea.operate()
        ea.replace()
#        if((ea.generation%10) == 0):
#            ea.plotter.plot()