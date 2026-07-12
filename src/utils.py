import numpy as np
import matplotlib.pyplot as plt
from .solution import Solution
from .instance import Instance

def show_solution(instance: Instance, solution: Solution):
	plt.title("Solution")
	
	x_coords, y_coords = np.unstack(instance.node_coords, axis=1)

	plt.plot(x_coords, y_coords, 'o')

	for i, route in enumerate(solution.routes):
		plt.plot(x_coords[route], y_coords[route], '-', label=f'Tour {i+1}')
	plt.legend()
	txt=f"Solution cost = {solution.value:.3f}" 
	if instance.optimal_value:
		txt += f"( Best known = {instance.optimal_value:.3f} )"
	plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
	plt.show()

def dict_coalesce(dictionary, keys: list, default = None):
	for key in keys:
		if key in dictionary:
			return dictionary[key]
	return default