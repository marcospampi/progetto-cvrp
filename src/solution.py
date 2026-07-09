import numpy as np

class Solution:
	routes: list[list[int]]
	cost: int
	fitness: float

	def __init__(self, routes: list[list[int]], distances: np.ndarray):
		self.routes = routes

		cost = 0
		for route in routes:
			for i in range(len(route)- 1) :
				j = route[i+1]
				cost+= distances[i,j]
		self.cost = cost
		self.fitness = 1 / float(cost) if cost > 0 else 0

	def route_edges(self):
		for route in self.routes:
			for i in range(len(route)- 1) :
				j = route[i+1]
				yield (i,j)
	def number_of_trucks(self):
		return len(self.routes)







