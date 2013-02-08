
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

def fitness(individual):
    return likeness(individual.genotype, 2**(individual.genotype_length + 1) - 1)

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
    
    def mutated_genotype(self):
        return self.genotype ^ Individual.random_mutation()
    
    @property
    def fenotype(self):
        return str(self.genotype)
    
    def fitness(self):
        return self.fitness_fn()
    
    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, bin(self.genotype)[2:].zfill(self.genotype_length))

if __name__ == '__main__':
    i = Individual(0b10101010101010101010)
    print num_to_bitstring(i.genotype)
    print num_to_bitstring(i.mutated_genotype())
