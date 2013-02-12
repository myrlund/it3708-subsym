import matplotlib.pyplot as plt
import numpy as np

class Plotting:
    ea = None
    
    def __init__(self, ea):
        self.ea = ea
        # [[ max_fitness, avg_fitness, std_deviation ]]
        self.generation = []
        self.max_fitness = []
        self.avg_fitness = []
        self.std_deviation = []
        
    def plot(self):
        
        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.generation, self.max_fitness, self.generation, self.avg_fitness)
        plt.ylabel("Max and average fitness")
        
        plt.subplot(212)
        plt.plot(self.generation, self.std_deviation)
        plt.ylabel("Standard deviation")
        plt.show()
    
    def update(self, generation, max_fitness, avg_fitness, std_deviation):
        self.generation.append(generation)
        self.max_fitness.append(max_fitness)
        self.avg_fitness.append(avg_fitness)
        self.std_deviation.append(std_deviation)
        
        
if __name__ == '__main__':
    plt.plot([1, 2, 3, 4, 5])
    plt.ylabel("STTAJIOFS")
    plt.show()