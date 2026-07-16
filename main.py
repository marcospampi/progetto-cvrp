from argparse import ArgumentParser
import json
import os
from time import time

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
    cwd = os.path.abspath(os.getcwd())
    argparser = ArgumentParser()
    argparser.add_argument("instance", help="File di istanza .vrp")
    argparser.add_argument("--iterations", help="Numero di iterazioni", default=100, type=int)
    argparser.add_argument("--runs", help="Numero di prove", default=1, type=int)
    argparser.add_argument("--seed", help="Seed per il generatore pseudorandom", default=int(time()), type=int)
    
    argparser.add_argument("--alpha", help="Influenza del feromone", default=1, type=float)
    argparser.add_argument("--beta", help="Influenza della visibilità", default=5, type=float)
    argparser.add_argument("--gamma", help="Influenza del risparmio", default=0, type=float)
    argparser.add_argument("--lambda", help="Influenza della capacità", default=0, type=float)
    argparser.add_argument("--rho", help="Costante di evaporazione", default=.25, type=float)
    argparser.add_argument("--sigma", help="Numero di formiche elitarie. Default numero di clienti.", default=-1, type=float)
    argparser.add_argument("--mmas", help="Applica MAX-MIN", default=True, type=bool)
    argparser.add_argument("--mmas-smoothing", help="Applica MAX-MIN smoothing", default=0, type=float)
    argparser.add_argument("--two-opt", help="Applica 2-Opt", default=True, type=bool)
    argparser.add_argument("--save", help="Salva la soluzione in formato JSON", default=None, type=str)
    argparser.add_argument("--show-plot", help="Mostra la soluzione a schermo.", default=True, type=bool)
    
    args = vars(argparser.parse_args())

    
    instance = Instance.load_vrp(args['instance'])
    iterations = args['iterations']
    runs = args['runs']
    seed = args['seed']
    alpha = args['alpha']
    beta = args['beta']
    gamma = args['gamma']
    lambda_ = args['lambda']
    rho = args['rho']
    sigma = args['sigma'] if args['sigma'] > 0 else 'auto'
    mmas = args['mmas']
    mmas_smoothing = args['mmas_smoothing']
    two_opt = args['two_opt']
    show_plot = args['show_plot']
    
    np.random.seed(seed)
    
    global_best_idx = (0,0)
    global_best = None

    for run in range(runs):
        desc = (f"Esecuzione run {run+1}...")
        run_best = None
        best_idx = 0
        with ACO_MPSolver(
            instance,
            alpha= alpha,
            beta= beta,
            gamma= gamma,
            lambda_= lambda_,
            rho= rho,
            sigma = sigma,
            mmas= mmas,
            mmas_smoothing= mmas_smoothing,
            two_opt= two_opt,
            placement_strategy = PlacementStrategy.CUSTOMER,
            trail_contribution_strategy = TrailContribuionStrategy.BEST_IN_EPOCH
        ) as solver:
            for i, sol in enumerate(tqdm(solver.run(iterations), total=iterations, desc=desc)):
                if run_best is None or sol.value < run_best.value:
                    best_idx = i
                    run_best = sol
                    err = (sol.value -  instance.optimal_value) / instance.optimal_value 

                    tqdm.write(f"Iterazione {i+1} trovata soluzione: {sol.value:.3f} [KBS: {instance.optimal_value}, Err: {err*100:.2f}%]")

        if global_best is None or run_best.value < global_best:
            global_best = run_best
            global_best_idx = ( run, best_idx )

    run, it = global_best_idx
    err = (global_best.value -  instance.optimal_value) / instance.optimal_value 
    tqdm.write(f"""
Migliore soluzione trovata: {global_best.value:.3f} [KBS: {instance.optimal_value}, Err: {err*100:.2f}%]
run = {run+1}, iterazione = {it+1}, seed = {seed}
    """)

    if show_plot:
        show_solution(instance, global_best)
    if 'save' in args and args['save'] is not None:
        global_best.store_json(args['save'])


if __name__ == "__main__":
    np.seterr('raise')
    main()
