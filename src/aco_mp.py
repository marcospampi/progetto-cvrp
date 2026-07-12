from functools import partial
from itertools import batched
from multiprocessing import Pool
import os
from copy import copy
import numpy as np

from src.aco import ACOSolver


class ACO_MPSolver(ACOSolver):
	def __init__(self, instance, num_of_cores: int = None , **params):
		
		super().__init__(instance, **params)

		self.num_of_cores = num_of_cores or os.cpu_count()  or 2
		self.dummy = copy(self)
		self.pool = Pool(self.num_of_cores)

	def _run_ants(self, tau, ants):

		fn = partial(ACOSolver._run_ants, self.dummy, tau)
		batches = batched(ants, int(self.num_of_cores))
		
		#results = [fn(batch) for batch in batches]
		results = self.pool.map(fn, batches)
		# combine results
		costs = np.concat([ cost for (cost,_,_) in results ])
		trails = np.concat([ trail for (_,trail,_) in results ])
		routes = [ tours for (_,_,routes) in results for tours in routes ]

		return costs, trails, routes