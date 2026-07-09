import json
import os

import numpy as np

from src.aco import ACO
from src.instance import Instance
from src.base_solver import BaseSolver
from src.utils import show_solution

import matplotlib.pyplot as plt

def main():
    print("Hello from metaheuristics!")


if __name__ == "__main__":
    main()
    np.seterr('raise')
    np.random.seed(0xCAFEBABE)

    
    path = os.path.join('instances', "CMT1.vrp")

    instance = Instance.load_vrp(path)

    solver = ACO(instance, ants=50, alpha = 10, beta = 10, rho=.1)
    evaluations = int(1e4)
    cost, fitness, trucks = [],[], []
    for i, sol in enumerate(solver.run(evaluations=evaluations)):
        cost.append(sol.cost)
        fitness.append(sol.fitness)
        trucks.append(sol.number_of_trucks())
    
    fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(7*3,6))
    plt.title("Runs")
    
    ax1.set_title("Cost")
    ax1.plot(cost)
    ax2.set_title("Fitness")
    ax2.plot(fitness)
    ax3.set_title("Trucks")
    ax3.hist(trucks)
    print(f"Best cost {min(cost)}, best fitness {max(fitness)}")
    plt.show()

    show_solution(solver, sol)
    
