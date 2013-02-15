from copy import copy
import random

#Class for evaluation the fitness of a given phenotuype.

class FitnessEval:
    

    @staticmethod
    def one_max_fitness(population):
        goal_bits = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        print goal_bits
        for individual in population:
            fitness = 0
            for p,g in zip(individual.phenotype, goal_bits):
                if p==g:
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
                points_commander = 0
                points_opponent = 0
                battle_nr = 0
                for i,j in zip(commander.phenotype, opposing_commander.phenotype):
                    i = i*commander.get_strength()
                    j = j*opposing_commander.get_strength()

                    if i>j:
                        points_commander+=2
                        commander.re_deploy(battle_nr, i-j)
                        opposing_commander.decrement_strength()
                    if i<j:
                        points_opponent+=2
                        opposing_commander.re_deploy(battle_nr, j-i)
                        commander.decrement_strength()
                    battle_nr += 1
                    
                #WAR done, increment fitness of winner based on points
                if points_commander>points_opponent:
                    commander.increment_fitness(2)
                if points_commander<points_opponent:
                    opposing_commander.increment_fitness(2)
                if points_commander==points_opponent:
                    commander.increment_fitness(1)
                    opposing_commander.increment_fitness(1)
                commander.reset()
                opposing_commander.reset()
                