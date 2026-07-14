import json
import os

import numpy as np
from tqdm import tqdm

from src.aco import ACOSolver, PlacementStrategy, TrailContribuionStrategy
from src.aco_mp import ACO_MPSolver
from src.instance import Instance
from src.base_solver import BaseSolver
from src.solution import Solution
from src.utils import show_solution

import matplotlib.pyplot as plt

def main():
    print("Hello from metaheuristics!")


if __name__ == "__main__":
    main()
    np.seterr('raise')

    seeds = [
        0xDEADBEEF,
        0x0BADF00D,
        0xCAFEBABE,
        0xDEADBEEF,
        0xC00FFEEE
    ]
    #path = os.path.join('instances', "A-n45-k7.vrp")
    path = os.path.join('instances', "CMT1.vrp.ignore")
    #path = os.path.join('instances', "B-n56-k7.vrp")

    instance = Instance.load_vrp(path)
    np.random.seed(0xcafebabe)

    best_sol = None
    for seed in range(1):
        solver = ACOSolver(
            instance,
            num_of_cores = 12,
            rho = .25,
            sigma = instance.customers,
            alpha  = 2, #pheromone
            beta   = 5, #visibility
            gamma  = 0, #savings
            lambda_= 0, #capacity
            two_opt = True,
            placement_strategy = PlacementStrategy.CUSTOMER,
            trail_contribution_strategy = TrailContribuionStrategy.SUM,
            mmas = True,
            mmas_smoothing = 0
            )

        epochs = 10#; int(3.5e5/instance.customers)
        print(f"Running for {epochs} epochs")
        y = np.zeros(epochs)
        for i, sol in tqdm(enumerate(solver.run(epochs))):
            y[i] = sol.value
            if i > 0 and y[i] < y[i-1]:
                if not sol.validate(instance):
                    tqdm.write("Trovata soluzione non valida :C")
                else:
                    tqdm.write(f"Epoch {i} trovata soluzione: {y[i]:.3f} [BKS: {instance.optimal_value}]")
                if best_sol is None or y[i] < best_sol.value:
                    best_sol = sol

        #print(f"Ottimo trovato: {sol.value}")
        #
        #plt.title("Cost plot")
        #plt.plot(y)
        #plt.xlabel("Generations")
        #plt.ylabel("Solution cost")
        
        #plt.show()
    show_solution(instance, best_sol)
        

    #solver = ACO(instance, ants=50, alpha = 10, beta = 10, rho=.1)
    #evaluations = int(1e4)
    #cost, fitness, trucks = [],[], []
    #for i, sol in enumerate(solver.run(evaluations=evaluations)):
    #    cost.append(sol.cost)
    #    fitness.append(sol.fitness)
    #    trucks.append(sol.number_of_trucks())
    #
    #fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(7*3,6))
    #plt.title("Runs")
    #
    #ax1.set_title("Cost")
    #ax1.plot(cost)
    #ax2.set_title("Fitness")
    #ax2.plot(fitness)
    #ax3.set_title("Trucks")
    #ax3.hist(trucks)
    #print(f"Best cost {min(cost)}, best fitness {max(fitness)}")
    #plt.show()
#
    #show_solution(solver, sol)
    
