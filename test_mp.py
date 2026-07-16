from argparse import ArgumentParser
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


if __name__ == "__main__":
    np.seterr('raise')

    seeds = [
        0xDEADBEEF,
        0x0BADF00D,
        0xCAFEBABE,
        0xDEADBEEF,
        0xC00FFEEE
    ]
    path = os.path.join('instances', "A-n45-k7.vrp")
    #path = os.path.join('instances', "CMT1.vrp.ignore")
    #path = os.path.join('instances', "B-n56-k7.vrp")

    instance = Instance.load_vrp(path)
    np.random.seed(0xdeadbeef)

    best_sol = None
    for seed in range(1):
        with ACO_MPSolver(
            instance,
            num_of_cores = 12,
            rho = .1,
            sigma = 'auto',
            alpha  = 3, #pheromone
            beta   = 5, #visibility
            gamma  = 2, #savings
            lambda_= 0.5, #capacity
            two_opt = True,
            placement_strategy = PlacementStrategy.CUSTOMER,
            trail_contribution_strategy = TrailContribuionStrategy.BEST_IN_EPOCH,
            mmas = True,
            mmas_smoothing = 1e-2
            ) as solver:

            epochs = int(3.5e5/instance.customers)
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

    show_solution(instance, best_sol)
