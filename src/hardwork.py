import json
import os
import re
import time

import numpy as np
from tqdm import tqdm

from src.aco_mp import ACO_MPSolver
from src.instance import Instance

def hardwork(fe: int, seed: int, runs: int,  instances_path: str, profiles: dict, output_path: str):
	instances = [
		Instance.load_vrp(os.path.join(instances_path, file)) 
		for file in os.listdir(instances_path)
			if re.search(r'\.vrp$', file)
	]
	output_file = os.path.join(output_path, 'runs.csv')
	def runner():
		for instance in instances:
			for profile_name, profile in profiles.items():
				np.random.seed(seed)
				for i in range(runs):
					with ACO_MPSolver(instance, **profile) as solver:
							
						start = time.time()
						iterations = int(np.ceil(fe / instance.customers))
						
						best_solution = None
						
						for i, solution in enumerate(solver.run(iterations)):
							elapsed = time.time() - start
							is_new_best = best_solution is None or best_solution.value > solution.value
							if is_new_best:
								best_solution = solution
							yield instance, profile_name, profile, elapsed, i, solution, is_new_best
						
						solution_file = os.path.join(output_path, '_'.join([instance.name, profile_name]) + '.json' )
						if best_solution is None: continue
						best_solution.store_json(solution_file)

	with open(output_file, 'w') as out:
		out.write(','.join([
			'instance',
			'profile',
			'iteration',
			'cost',
			'elapsed'
		]))
		out.write('\n')
		for iteration in tqdm(runner()):
			instance, profile_name, profile, elapsed, i, solution, is_new_best = iteration
			if not is_new_best: continue
			out.write(",".join([
				instance.name,
				profile_name,			
				str(i),
				str(solution.value),
				str(elapsed)
			]))
			out.write('\n')
			out.flush()

					


