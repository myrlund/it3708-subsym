
import sys
from FitnessEval import FitnessEval
from Individual import OneMaxIndividual
from Plotting import Plotting
from Blotto import Blotto
import random

class EA:
    
    population_size = 28 #Size of the population
    generations = 200 #Number of generations
    generation = 0 #Current generation number
    fitness_goal = 40 #The fitness goal
    crossover_rate = 1 #The rate of which to perform crossover
    k = 4 #Group size in k_tournament
    e = 0.2 #Probability of selecting random in k_tournament
    mutation_probability = 0.3 #Probability that mutation of a specimen will occur
    mutation_count = 1 #Number of bits mutated when mutating

    population_genotype = []
    population_fitness = []
    new_generation = []
    children = []
    reproducers = []
    population = []
    
    develops = None
    adult_selection_fn = None
    parent_selection_fn = None
    fitness = None
    
    def __init__(self, individual_type, fitness_fn, adult_selection_fn, parent_selection_fn):
        self.adult_selection_fn = adult_selection_fn
        self.parent_selection_fn = parent_selection_fn
        self.fitness = fitness_fn
        self.plotter = Plotting(self)
        self.individual_type = individual_type
        self.overproduction_factor = 1
        self.rank_max = 2
        self.rank_min = 0
        
    def create(self):
        for _ in range(0, self.population_size):
            self.population.append(self.individual_type())
    
    def develop(self):
        for p in self.population:
            p.development()
    
    def select(self):
        self.population_fitness = []
        self.fitness(self.population)
            
        population_fitness = [p.fitness for p in self.population]   
        average_fitness = self.sum_population()/len(self.population)
        best_individual = self.sorted_population()[0]
        if best_individual.fitness == self.fitness_goal:
            print "SOLUTION FOUND: "+str(best_individual.phenotype)+ " " +str( best_individual.fitness )
            self.plotter.update(self.generation, best_individual.fitness, average_fitness, sum( map(lambda x: (x - average_fitness)**2, population_fitness) )  )
            self.plotter.plot()
            sys.exit()
        
        if((self.generation%2) == 0):
            print "GENERATION:: " +str(self.generation)
            print "Max fitness: " +str(best_individual.fitness) +": " + str(best_individual.phenotype)
            print "Avg fitness: " +str( average_fitness )
        self.plotter.update(self.generation, best_individual.fitness, average_fitness, sum( map(lambda x: (x - average_fitness)**2, population_fitness) )  )
        
        if self.parent_selection_fn is Selection.rank:
            self.rank_max = int( raw_input("Rank selection Max: ") )
            self.rank_min = int( raw_input("Rank selection Min: ") )
        if self.adult_selection_fn is Selection.over_production and self.overproduction_factor is 1:
            self.overproduction_factor = int( raw_input("Over production factor: ") )
        self.reproducers = self.parent_selection_fn(self.population, self.sum_population(), self.overproduction_factor, self.rank_min, self.rank_max, self.k, self.e)
        
    
    def reproduce(self):
        self.children = []
        for p in self.reproducers:
            self.children.append(p.crossover( self.reproducers[random.randint(0,len(self.reproducers)-1)], self.crossover_rate ))
    
    def operate(self):
        for p in self.children:
            p.mutate(self.mutation_probability, self.mutation_count)
        
    def replace(self):
        for p in self.children:
            p.development()
        self.generation += 1
        self.population = self.adult_selection_fn(self.population, self.children, self.population_size)
          
          
    
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
    
    
        
    #SELECTION PROTOCOLS
    @staticmethod
    def full_gen_replacement(population, children, pop_size):
        return children
    
    @staticmethod
    def over_production(population, children, pop_size):
        sorted_population = sorted(children, lambda x, y: cmp(x.fitness, y.fitness))[::-1]
        return sorted_population[0:pop_size]
    
    @staticmethod
    def generational_mixing(population, children, pop_size):
        population.extend(children)
        sorted_population = sorted(population, lambda x, y: cmp(x.fitness, y.fitness))[::-1]
        return sorted_population[0:pop_size]
        
        
        

    #SELECTION MECHANISMS    
    #Fitness proportionate scaling of fitness and spins the wheel
    @staticmethod
    def fitness_proportionate(population, sum_fitness, op, rank_min, rank_max,  k=0, e=0):
        expected_mating = []
        average_fitness = sum_fitness/len(population)
        mating_wheel = []
        for p in population:
            if average_fitness is 0:
                expected_mating = 1
            else:
                expected_mating = int(round(p.fitness/average_fitness))
            for _ in range(0, expected_mating):
                mating_wheel.append(p) 
            
        #THEN SPIN ZE WHEEEEL
        reproducers = []
        for _ in range(0, int(len(population)*op) ):
            reproducers.append( mating_wheel[random.randint(0,len(mating_wheel)-1)] )
        
        return reproducers
       
    #Sigma scaling of fitness and spins the wheel 
    @staticmethod
    def sigma_scaling(population, sum_fitness, op, rank_min, rank_max, k=0, e=0):
        expected_mating = []
        population_fitness = [p.fitness for p in population]
            
        average_fitness = sum_fitness/len(population)
        standard_deviation = sum( map(lambda x: (x - average_fitness)**2, population_fitness) )
        mating_wheel = []
        for p in population:
            if standard_deviation is 0:
                expected_mating = 1
            else:
                expected_mating = int(1 + ( (p.fitness-average_fitness) / 2*standard_deviation ))
            for _ in range(0, expected_mating):
                mating_wheel.append(p) #Indexes
        #THEN SPIN ZE WHEEEEL
        reproducers = []
        for _ in range(0, int(len(population)*op)):
            reproducers.append( mating_wheel[random.randint(0,len(mating_wheel)-1)] )
        
        return reproducers
        
    #Rank scaling of fitness and spins the wheel
    #TODO
    @staticmethod
    def rank(population, sum_fitness, op, rank_min, rank_max, k=0, e=0):
        expected_mating = []
        sorted_population = sorted(population, lambda x, y: cmp(x.fitness, y.fitness))[::-1]
        mating_wheel = []
        for p in population:
            rank = (sorted_population.index(p)+1)
            expected_mating = int( rank_min+(rank_max-rank_min)*((rank-1)/(len(population))) )
            print rank
            for _ in range(0, expected_mating):
                mating_wheel.append(p)
            
        #THEN SPIN ZE WHEEEEL, make own method? and proper! this is crap
        reproducers = []
        for _ in range(0, int(len(population)*op) ):
            reproducers.append( mating_wheel[random.randint(0,len(mating_wheel)-1)] )
        
        return reproducers 
    

    #Selects the index of the reproducers in the population by means of local k-tournament, currently only works on popsizes divisible by k
    #TODO: Doesn't work i thinks
    @staticmethod
    def k_tournament(population, sum_fitness, op, rank_min, rank_max, k, e):
        reproducers = []
        group_k = k
        for i in range(0, len(population)):
            if i == group_k-1:
                #FACE-OFF!
                tournament_group = population[(i-(k-1)):group_k]
                for _ in range(int(len(tournament_group)*op)):
                    if random.random()<e:
                        reproducers.append( tournament_group[random.randint(0, k-1)] )
                    else:
                        tournament_group = sorted(tournament_group, lambda x, y: cmp(x.fitness, y.fitness))[::-1]
                        reproducers.append( tournament_group[0] )
                group_k = group_k + k
        return reproducers
    
   
    
FITNESS_FUNCTIONS = {1: FitnessEval.one_max_fitness,
                     2: FitnessEval.blotto_fitness}

PARENT_SELECTION_FUNCTIONS = {1: Selection.fitness_proportionate, 
                              2: Selection.sigma_scaling, 
                              3: Selection.rank, 
                              4: Selection.k_tournament}

ADULT_SELECTION_FUNCTIONS = {1: Selection.full_gen_replacement, 
                             2: Selection.over_production, 
                             3: Selection.generational_mixing}

INDIVIDUAL_TYPE = {1: OneMaxIndividual,
                   2: Blotto}    
    #TODO: implement input
if __name__ == '__main__':
    fitness_nr = int( raw_input("Fitness function: ") )
    parent_selection_nr = int( raw_input("Parent Selection: ") )
    adult_selection_nr = int( raw_input("Adult selection: ") )
    individual_type = OneMaxIndividual
    
    ea = EA(individual_type, FITNESS_FUNCTIONS[fitness_nr], ADULT_SELECTION_FUNCTIONS[adult_selection_nr], PARENT_SELECTION_FUNCTIONS[parent_selection_nr])
    ea.create()
    ea.develop()
    for _ in range(0, ea.generations):
        ea.select()
        ea.reproduce()
        ea.operate()
        ea.replace()
    ea.plotter.plot()
 
   
