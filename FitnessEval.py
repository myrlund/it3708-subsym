#Class for evaluation the fitness of a given phenotuype.

class FitnessEval:
    
    #TODO: Change the fitness calculation to a likeness function!
    
    
    #Receives list of a population of binary lists
    #fitness gets higher(worse) if there are many zero's
    @staticmethod
    def one_max_fitness(population):
        for individual in population:
            fitness = 0;
            for i in individual.phenotype:
                if i == 1:
                    fitness += 1
            individual.set_fitness(fitness)
            
    #Receives list of a population of blotto strategies
    @staticmethod
    def blotto_fitness(population):
        return 0
        
        