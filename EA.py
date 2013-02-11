
import sys
from FitnessEval import FitnessEval
from EAOperators import Individual
from Plotting import Plotting
import random

class EA:
    
    population_size = 20 #Size of the population
    generations = 200 #Number of generations
    generation = 0 #Current generation nr
    fitness_goal = 40 #The fitness goal
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
        if best_individual.fitness == self.fitness_goal:
            print "SOLUTION FOUND: "+str(best_individual.phenotype)+ " " +str( best_individual.fitness )
            sys.exit()
            
        if((self.generation%2) == 0):
            print "GENERATION:: " +str(self.generation)
            print "Max fitness: " +str(best_individual.fitness) +": " + str(best_individual.phenotype)
            print "Avg fitness: " +str( (self.sum_population()/len(self.population)) )
        
        self.reproducers = self.selects.fitness_proportionate(self.population, self.sum_population())

    
    def reproduce(self):
        self.children = []
        for p in self.reproducers:
            self.children.append(p.crossover( self.reproducers[random.randint(0,len(self.reproducers)-1)] ))
    
    def operate(self):
        for p in self.children:
            p.mutate(self.mutation_probability)
        
    def replace(self):
        for p in self.children:
            p.development()
        self.generation += 1
        self.population = Selection().full_gen_replacement(self.population, self.children)
          
    def sorted_population(self):
        return sorted(self.population, lambda x, y: cmp(x.fitness, y.fitness))[::-1]
    
    def sorted_children(self):
        return sorted(self.children, lambda x, y: cmp(x.fitness, y.fitness))[::-1]        

    def sum_population(self):
        fitness_sum = 0
        for p in self.population:
            fitness_sum += p.fitness
        return fitness_sum
    
#Contains the different selection protocols
#and selection mechanisms  
class Selection:
    
    #Set which selection protocol to use
    def set_selection_protocol(self):
        return False
        
    #SELECTION PROTOCOLS
    def full_gen_replacement(self, population, children):
        return children
        
    def over_production(self):
        return False
    
    def generational_mixing(self):
        return False
        
        
        
    #Set which selection mechanism to use
    def set_selecton_mechanism(self):
        return False
    
    #SELECTION MECHANISMS    
    #Fitness proportionate scaling of fitness and spins the wheel
    def fitness_proportionate(self, population, sum_fitness):
        expected_mating = []
        average_fitness = sum_fitness/len(population)
        mating_wheel = []
        for p in population:
            expected_mating = int(round(p.fitness/average_fitness))
            for _ in range(0, expected_mating):
                mating_wheel.append(p) 
            
        #THEN SPIN ZE WHEEEEL
        reproducers = []
        for _ in range(0, len(population)):
            reproducers.append( mating_wheel[random.randint(0,len(mating_wheel)-1)] )
        
        return reproducers
       
    #Sigma scaling of fitness and spins the wheel 
    def sigma_scaling(self, population, sum_fitness):
        expected_mating = []
        average_fitness = sum_fitness/len(population)
        standard_deviation = sum( map(lambda x: (x - average_fitness)**2, sum_fitness) )
        mating_wheel = []
        for p in population:
            expected_mating = int(1 + ( (p.fitness-average_fitness) / 2*standard_deviation ))
            for _ in range(0, expected_mating):
                mating_wheel.append(p) #Indexes
        #THEN SPIN ZE WHEEEEL
        reproducers = []
        for _ in range(0, len(population)):
            reproducers.append( mating_wheel[random.randint(0,len(mating_wheel)-1)] )
        
        return reproducers
        
    #Rank scaling of fitness and spins the wheel
    #TODO
    def rank(self, population_fitness, sum_fitness):
        expected_mating = []
        average_fitness = sum(population_fitness)/len(population_fitness)
        mating_wheel = []
        for i in range(0, population_fitness):
            expected_mating = min + (max-min)*()
            for _ in range(0, expected_mating):
                mating_wheel.append(i) #Indexes
            
        #THEN SPIN ZE WHEEEEL
        reproducers = []
        for _ in range(0, len(population_fitness)):
            reproducers.append( mating_wheel[random.randint(0,len(mating_wheel)-1)] )
        
        return reproducers
    

    #Selects the index of the reproducers in the population by means of local k-tournament, currently only works on popsizes divisible by k
    def k_tournament(self, population, k, e):
        reproducers = []
        group_k = k
        for i in range(0, len(population)):
            if i == group_k-1:
                #FACE-OFF!
                tournament_group = population[(i-(k-1)):group_k]
                for _ in tournament_group:
                    if random.random()<e:
                        reproducers.append( population[random.randint(0, k-1) + (group_k-k)] )
                    else:
                        reproducers.append( population[tournament_group.index(max(tournament_group)) + (group_k-k)] )
                group_k = group_k + k
        return reproducers
    
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