#Class for evaluation the fitness of a given phenotuype.

class FitnessEval:
    
    #A specimen is a list of integers
    #fitness gets higher(worse) if there are many zero's
    def calc_fitness(self, specimen):
        fitness = 0;
        for i in specimen:
            if i == 1:
                fitness += 1
        return fitness
        