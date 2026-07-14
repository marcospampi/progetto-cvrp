from functools import partial
from itertools import batched
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import os
from copy import copy
import numpy as np

from src.aco import ACOSolver


def _aco_mp_init(solver_):
	global solver
	solver = solver_

def _aco_mp_run(args):
	global solver
	tau , ants, seed= args
	np.random.seed(seed)
	return solver._run_ants(tau, ants)


class ACO_MPSolver(ACOSolver):
	"""
	  Multiprocessing ACO Solver for parallel computing of the Ant System algorithm.
	"""
	def __init__(self, instance, **params):
		
		super().__init__(instance, **params)

		self.num_of_cores = params.get('num_of_cores',os.cpu_count())
		self.dummy = ACOSolver(instance, **params)

	def __enter__(self):
		self.pool = Pool(self.num_of_cores, initializer=partial(_aco_mp_init, self.dummy))
		return self
		
	#def _run_ants_parallel(self, tau: np.ndarray, args: tuple[list, int]):
	#		ants, seed = args
	#		np.random.seed(seed)
	#		return ACOSolver._run_ants(self, tau, ants)


	def _run_ants(self, tau, ants):

		# work around to have deterministic runs
		batches = list(batched(ants, int(self.num_of_cores)))
		seeds = np.random.uniform(0, 2**32 - 1, size= len(batches)).astype(int)
		#bounded = partial(ACO_MPSolver._run_ants_parallel, self.dummy, tau)
		
		
		results = self.pool.map(_aco_mp_run, list(zip([tau] * len(batches),batches, seeds)))

		costs = np.concat([ cost for (cost,_,_) in results ])
		trails = np.concat([ trail for (_,trail,_) in results ])
		routes = [ tours for (_,_,routes) in results for tours in routes ]

		return costs, trails, routes
	
	def __exit__(self, exc_type, exc, tb):
		if self.pool is not None:
			self.pool.terminate()
		return False
			