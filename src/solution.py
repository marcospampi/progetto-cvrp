import numpy as np

from src.instance import Instance

class Solution:


	def __init__(self, 
							routes: list[list[int]], 
							value: float,
							epoch: int = -1):
		self.routes_wno_depot = routes
		self.value = value
		
		self.routes = [
			[0,*route,0] for route in routes
		]
		
		self.fitness = 1 / value if value > 0 else 0


	def recompute(self, d: np.ndarray):
		cost = 0
		for tour in self.routes:
			cost += sum( d[i,j] for i,j in zip(tour[:-1], tour[1:]) )
		return cost

	def set_epoch(self, epoch: int): 
		self.epoch = epoch

	def validate(self, instance: Instance):
		cost_cond = abs(self.recompute(instance.distances) - self.value) <= 1e3
		
		demands = ([
			sum(map(lambda n: instance.node_demand[n], route))
			for route in self.routes
		])

		demands_cond = all([ d <= instance.capacity for d in demands])

		valid = cost_cond and demands_cond
		if valid == False:
			print("Solution not valid")
			print(demands)
			print(cost_cond)
		
		return valid
		

	
	@staticmethod
	def from_solution(path: str, distances: np.ndarray):
		routes = []
		cost = 0
		with open(path) as file:
			for line in file:
				match line[:5]:
					case 'Route':
						line = line.split(': ')[1]
						tour = [
							int(idx) for idx in line.split(' ')
						]
						routes.append(tour)
					case 'Cost ':
						cost = float(line[5:])

		sol = Solution(routes, cost)
		computed = sol.recompute(distances)
		error = np.abs(np.round(computed, 3) - cost)
		if error > 0:
			print(routes)
			print(sol.routes_wno_depot)
			print(sol.routes)
			raise Exception("Invalid compute, cost claimed to be {:.3f}, computed {:.3f}".format(cost, computed))
		
		return sol