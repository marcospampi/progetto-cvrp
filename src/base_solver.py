from abc import abstractmethod,ABC
from typing import Generator

import numpy as np


from .instance import Instance
from .solution import Solution


class BaseSolver(ABC):
	def __init__(self, instance: Instance):
		self.instance = instance
		self.dimension = instance.dimension
		self.customers = instance.customers
		self.capacity = instance.capacity
		self.demands = instance.node_demand
		self.coords = instance.node_coords
		self.distances = instance.distances.copy()

	@abstractmethod
	def run(self, evaluations: int ) -> Generator[Solution, None, int]:
		pass


			