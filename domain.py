
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

def fenotype_fitness(genotype, genotype_length=20):
    return likeness(genotype, 2**(genotype_length + 1) - 1)

def fitness(fenotype):
    return fenotype_fitness(fenotype, Individual.genotype_length)

def num_to_bitstring(n, l=20):
    return bin(n)[2:].zfill(l)

def bitstring_to_numbers(s):
    return map(int, s)

class Individual:
    fitness_fn = fitness
    genotype_length = 20
    
    def __init__(self, genotype=None):
        if genotype is None:
            genotype = Individual.random_genotype()
        
        self.genotype = genotype ^ Individual.random_mutation()
    
    def combine_with(self, other):
        crossover_range = (2, 5)
        splits = [(i % 2, random.randint(*crossover_range)) for i in range(self.genotype_length / crossover_range[0])]
        
        genotypes = (num_to_bitstring(self.genotype), num_to_bitstring(other.genotype))
        
        new_genotype = []
        index = 0
        for individual, n_genes in splits:
            to_index = min(index+n_genes, self.genotype_length)
            new_genotype.append(genotypes[individual][index:to_index])
            
            if to_index >= self.genotype_length:
                break
            
            index += n_genes
        
        return Individual(int("".join(new_genotype), 2))
    
    @property
    def fenotype(self):
        return self.genotype
    
    @property
    def fitness(self):
        return self.fitness_fn.__func__(self.fenotype)
    
    def __str__(self):
        return "%s(%d)" % (self.__class__.__name__, self.fitness) # bin(self.genotype)[2:].zfill(self.genotype_length)
    
    def __repr__(self):
        return self.__str__()

    @staticmethod
    def random_genotype():
        return random.randint(0, 2**20)
    
    @staticmethod
    def random_mutation():
        n_mutated_genes = random.randint(0, 1)
        return reduce(
            lambda acc, x: acc ^ x,
            [2**random.randint(0,20) for x in range(n_mutated_genes)],
            0
        )
    
    @staticmethod
    def merge_genotypes(g1, g2):
        return g1 & g2
    
class World:
    
    # World settings
    max_fitness = 20
    
    def __init__(self, population_size=20):
        self.generations = 0
        self.population_size = population_size
        
        # Generate a population
        self.population = [Individual() for _ in range(self.population_size)]
    
    def reproduction_for_fitness(self, fitness, max_fitness=20, max_dominance=0.1):
        """Gives back number of offspring for a given fitness rating."""
        # max_fitness == 20, population_size == 20, max_dominance ~ 0.1
        return 2.0 * fitness / max_fitness * self.population_size * max_dominance
    
    def select_parents(self):
        """Parent selection algorithm. Returns tuples of individuals."""
        
        # Sort the population by fitness
        p = sorted_individuals = self.sorted_population()
        pairs = [(p[i], p[i+1]) for i in range(0, len(p) - 1, 2)]
        
        return pairs
    
    def tick(self):
        """A generation tick."""
        
        self.generations += 1
        
        parents = self.select_parents()
        
        new_individuals = []
        for parent1, parent2 in parents:
            
            # Combine the parents' fitnesses...
            combined_fitness = (parent1.fitness + parent2.fitness) / 2
            
            # ...calculate the number of offspring they deserve
            n_offspring = min(
                int(self.reproduction_for_fitness(combined_fitness)),
                self.population_size - len(new_individuals)
            )
            
            print parent1, "and", parent2, "get %i kids" % n_offspring
            
            # ...and copulate!
            new_individuals += [parent1.combine_with(parent2) for _ in range(n_offspring)]
        
        # Generation shift
        self.population = new_individuals
    
    def sorted_population(self):
        return sorted(self.population, lambda x, y: cmp(x.fitness, y.fitness))[::-1]

if __name__ == '__main__':
    w = World()
    # i1 = Individual(0b10101010101010101010)
    # i2 = Individual(0b10101010101010101010)
    # print num_to_bitstring(i1.combine_with(i2).genotype)
    n = 200
    print w.sorted_population()
    for _ in range(n):
        w.tick()
        print w.sorted_population()
    
