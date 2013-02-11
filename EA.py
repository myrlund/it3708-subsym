
import sys
from FitnessEval import FitnessEval
from EAOperators import Selection
from EAOperators import Individual
from Plotting import Plotting

class EA:
    
    population_size = 20 #Size of the population
    generations = 200 #Number of generations
    generation = 0 #Current generation nr
    nr_of_bits = 20 #Bitlength 
    k = 4 #Group size in k_tournament
    e = 0.2 #Probability of selecting random in k_tournament
    mutation_probability = 0.8 #Probability that mutation of a specimen will occur
    mutation_count = 1 #Number of bits mutated when mutating
    population_genotype = []
    population_fitness = []
    new_generation = []
    children = []
    reproducers = []
    population = []
    
    develops = None
    selects = None
    operates = None
    populates = None
    fitness = None
    
    def __init__(self):
        self.selects = Selection()
        self.fitness = FitnessEval()
        self.plotter = Plotting(self)
        
    def create(self):
        for _ in range(0, self.population_size):
            self.population.append(Individual())
    
    def develop(self):
        for p in self.population:
            p.development()
    
    
    def select(self):
        self.population_fitness = []
        for p in self.population:
            p.calc_fitness()
            
        best_individual = self.sorted_population()[0]
        if best_individual.fitness == self.nr_of_bits:
            print "SOLUTION FOUND: "+str(best_individual.phenotype)+ " " +str( best_individual.fitness )
            sys.exit()
            
        if((self.generation%10) == 0):
            print "GENERATION:: " +str(self.generation)
            print "Max fitness: " +str(best_individual.fitness) +": " + best_individual.phenotype
            print "Avg fitness: " +str( (self.sum_population()/len(self.population)) )
        
        self.reproducers = self.selects.k_tournament(self.population, self.k, self.e)
    
    def reproduce(self):
        self.children = []
        for _ in range(0, self.k):
            for p in self.reproducers:
                self.children.append(p)
        print self.children
    
    def operate(self):
        for p in self.children:
            p.mutate(self.mutation_probability)
        
        for p in self.children:
            p.crossover()
    
    def replace(self):
        new_generation = []
        for i in self.mutated_genotypes:
            new_generation.append(self.develops.development(i, self.nr_of_bits))
        self.generation += 1
        self.population = Selection().full_gen_replacement(self.population, new_generation)
        self.population_genotype = self.children_genotypes
        
    
    def sorted_population(self):
        return sorted(self.population, lambda x, y: cmp(x.fitness, y.fitness))[::-1]

    def sum_population(self):
        fitness_sum = 0
        for p in self.population:
            fitness_sum += p.fitness
        return fitness_sum
    
if __name__ == '__main__':
    ea = EA()
    ea.create()
    ea.develop()
    for _ in range(0, ea.generations):
        ea.select()
        ea.reproduce()
        ea.operate()
        ea.replace()
    
    ea.plotter.plot()