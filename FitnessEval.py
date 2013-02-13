from copy import copy

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
            
    #Receives list of a population of blotto strategies, pits every commanders against
    #each other, awards fitness points when winning war against another commander
    @staticmethod
    def blotto_fitness(population):
        for p in population:
            p.reset_fitness()
        population_copy = copy(population)
        for commander in population:
            population_copy.remove(commander)
            for opposing_commander in population_copy:
                
                #Execute a WAR!
#                print "WAR: "+str(commander)+" vs. "+str(opposing_commander)
                points_commander = 0
                points_opponent = 0
                battle_nr = 0
                for i,j in zip(commander.phenotype, opposing_commander.phenotype):
                    i = i*commander.get_strength()
                    j = j*opposing_commander.get_strength()
                    if i>j:
#                        print "BATTLE "+str(battle_nr)+" WINNER: "+str(commander)
                        points_commander+=2
                        commander.re_deploy(battle_nr, i-j)
                        opposing_commander.decrement_strength()
                    if i<j:
#                        print "BATTLE "+str(battle_nr)+" WINNER: "+str(opposing_commander)
                        points_opponent+=2
                        opposing_commander.re_deploy(battle_nr, j-i)
                        commander.decrement_strength()
                    battle_nr += 1
                    
                #WAR done, increment fitness of winner based on points
                if points_commander>points_opponent:
#                    print "WAR WINNER: "+str(commander)
                    commander.increment_fitness(2)
                if points_commander<points_opponent:
#                    print "WAR WINNER: "+str(opposing_commander)
                    opposing_commander.increment_fitness(2)
                if points_commander==points_opponent:
#                    print "DRAW"
                    commander.increment_fitness(1)
                    opposing_commander.increment_fitness(1)
                commander.reset()
                opposing_commander.reset()
    