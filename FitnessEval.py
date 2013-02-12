#Class for evaluation the fitness of a given phenotuype.

class FitnessEval:
    
    
    #A specimen is a list of integers
    #fitness gets higher(worse) if there are many zero's
    def calc_fitness(self, population):
        for individual in population:
            fitness = 0;
            for i in individual.phenotype:
                if i == 1:
                    fitness += 1
            individual.set_fitness(fitness)
        