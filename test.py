import json
import os

import numpy as np
from tqdm import tqdm

from src.aco2 import ACOSolver
from src.instance import Instance
from src.base_solver import BaseSolver
from src.solution import Solution
from src.utils import show_solution

import matplotlib.pyplot as plt

def main():
    print("Hello from metaheuristics!")


if __name__ == "__main__":
    main()
    instance = Instance.load_vrp('instances/CMT1.vrp')
    sol = Solution.from_solution('/home/marco/Scaricati/CMT1.sol', instance.distances)
    print(sol.validate(instance))
    show_solution(instance,sol)
    
