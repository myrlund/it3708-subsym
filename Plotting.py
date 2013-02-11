import matplotlib.pyplot as plt
import numpy as np

class Plotting:
    ea = None
    
    def __init__(self, ea):
        self.ea = ea
        
    def plot(self):
        plt.plot(self.ea.population_fitness, "ro")
        plt.show()
    
    def update(self):
        return False
        
        
if __name__ == '__main__':
    plt.plot([1, 2, 3, 4, 5])
    plt.ylabel("STTAJIOFS")
    plt.show()