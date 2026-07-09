import numpy as np
import matplotlib.pyplot as plt
from .base_solver import BaseSolver
from .solution import Solution
def show_solution(solver: BaseSolver, solution: Solution):
	plt.title("Solution")
	
	x_coords, y_coords = np.unstack(solver.coordinates, axis=1)

	plt.plot(x_coords, y_coords, 'o')

	for route in solution.routes:
		plt.plot(x_coords[route], y_coords[route])

	plt.show()