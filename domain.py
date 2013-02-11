
import random

def likeness(number1, number2):
    """Returns the likeness between two bitstrings."""
    s1, s2 = map(num_to_bitstring, (number1, number2))
    n1, n2 = map(bitstring_to_numbers, (s1, s2))
    numbers = zip(n1, n2)
    return reduce(
        lambda acc, (x, y): acc + (x ^ y ^ 1),
        numbers,
        0
    )

def genotype_fitness(genotype, genotype_length=20):
    return likeness(genotype, 2**(genotype_length + 1) - 1)

def fitness(individual):
    return genotype_fitness(individual.genotype, individual.genotype_length)

def num_to_bitstring(n):
    return bin(n)[2:]

def bitstring_to_numbers(s):
    return map(int, s)


class Individual:
    fitness_fn = fitness
    genotype_length = 20
    
    def __init__(self, genotype=None):
        if genotype is None:
            genotype = Individual.random_genotype()
        
        self.genotype = genotype
    
    @staticmethod
    def random_genotype():
        return random.randint(0, 2**20)
    
    @staticmethod
    def random_mutation():
        n_mutated_genes = 3
        return reduce(
            lambda acc, x: acc | x,
            [2**random.randint(0,20) for x in range(n_mutated_genes)],
            0
        )
    
    @staticmethod
    def merge_genotypes(g1, g2):
        return g1 & g2
    
    def combine_with(self, other):
        return Individual(Individual.merge_genotypes(self.mutated_genotype(), other.mutated_genotype()))
    
    def mutated_genotype(self):
        return self.genotype ^ Individual.random_mutation()
    
    @property
    def fenotype(self):
        return str(self.genotype)
    
    @property
    def fitness(self):
        return self.fitness_fn()
    
    def __str__(self):
        return "%s(%d)" % (self.__class__.__name__, self.fitness) # bin(self.genotype)[2:].zfill(self.genotype_length)
    
    def __repr__(self):
        return self.__str__()

class World:
    
    # World settings
    max_fitness = 20
    generations = 0
    
    def __init__(self, population_size=20):
        self.population_size = population_size
        
        # Generate a population
        self.population = [Individual() for _ in range(self.population_size)]
    
    def reproduction_for_fitness(self, fitness, max_fitness=20, max_dominance=0.3):
        """Gives back number of offspring for a given fitness rating."""
        # max_fitness == 20, population_size == 20, max_dominance ~ 0.3
        return 1.0 * fitness / max_fitness * self.population_size * max_dominance
    
    def select_parents(self):
        """Parent selection algorithm. Returns tuples of individuals."""
        
        # Sort the population by fitness
        p = sorted_individuals = self.sorted_population()
        pairs = [(p[i], p[i+1]) for i in range(0, self.population_size, 2)]
        
        return pairs
    
    def tick(self):
        """A generation tick."""
        
        self.generations += 1
        
        parents = self.select_parents()
        
        new_individuals = []
        for parent1, parent2 in parents:
            
            # Combine the parents' fitnesses...
            combined_fitness = parent1.genotype & parent2.genotype
            
            # ...calculate the number of offspring they deserve
            n_offspring = min(
                int(self.reproduction_for_fitness(combined_fitness)),
                self.population_size - len(new_individuals)
            )
            
            # ...and copulate!
            new_individuals += [parent1.combine_with(parent2) for _ in range(n_offspring)]
        
        # Generation shift
        self.population = new_individuals
    
    def sorted_population(self):
        return sorted(self.population, lambda x, y: cmp(x.fitness, y.fitness))[::-1]

if __name__ == '__main__':
    w = World()
    print w.sorted_population()
    w.tick()
    print w.sorted_population()
    
