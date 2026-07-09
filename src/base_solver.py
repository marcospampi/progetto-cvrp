from abc import abstractmethod,ABC
from typing import Generator

import numpy as np


from .instance import Instance
from .solution import Solution


class BaseSolver(ABC):
	def __init__(self, instance: Instance):
		self.instance = instance
		dim,i2p,p2i,cmat,qmat,dmat = self._compute_tables()
		self.dim = dim
		self.i2p = i2p
		self.p2i = p2i
		self.coordinates = cmat
		self.demands = qmat
		self.distances = dmat
		self.depot_index = i2p[instance.depot_node]
		self.initial_capacity = instance.capacity
	

	@abstractmethod
	def run(self, evaluations: int ) -> Generator[Solution, None, int]:
		pass

	def _compute_tables(self):
		dim = self.instance.dimension
		
		# instance to problem lookup table
		i2p_mat = np.arange(-1, dim+1, dtype=np.int32)
		# problem to instance lookup table
		p2i_mat = np.arange(1, dim +1, dtype=np.int32)
		# coordinates mat
		cmat = np.ndarray((dim, 2), dtype=np.float32)
		# demand mat
		qmat = np.ndarray((dim), dtype=np.float32)
		# distances mat
		dmat = np.ndarray((dim, dim), dtype=np.float32)

		# copy coordinates mat
		for ii in p2i_mat:
			pi = i2p_mat[ii]
			cmat[pi] = self.instance.node_coords[ii]
			qmat[pi] = self.instance.node_demand[ii]

		# compute distance
		for i in range(0,dim):
			for j in range(i, dim):
				d = 0 if i == j else np.linalg.norm(cmat[i]-cmat[j])
				dmat[i,j] = dmat[j,i] = d
		return (
			dim,
			i2p_mat,
			p2i_mat,
			cmat,
			qmat,
			dmat
		)

		
			