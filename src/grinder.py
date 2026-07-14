import json
import os
import re
import time

import numpy as np
from tqdm import tqdm

from src.aco_mp import ACO_MPSolver
from src.instance import Instance

def grinder(fe: int, seed: int, runs: int,  instances_path: str, profiles: dict, output_file: str):
	instances = [
		Instance.load_vrp(os.path.join(instances_path, file)) 
		for file in os.listdir(instances_path)
			if re.search(r'\.vrp$', file)
	]
	output_file = os.path.join(output_file)
	def runner():
		for instance in instances:
			tqdm.write(f"Current instance: {instance.name}")
			for profile_name, profile in profiles.items():
				tqdm.write(f"\tCurrent profile: {profile_name}")
				np.random.seed(seed)
				for run in range(runs):
					with ACO_MPSolver(instance, **profile) as solver:

						start = time.time()
						iterations = int(np.ceil(fe / instance.customers))
						
						best_solution = None
						
						for i, solution in enumerate(solver.run(iterations)):
							elapsed = time.time() - start
							is_new_best = best_solution is None or best_solution.value > solution.value
							if is_new_best:
								best_solution = solution
							yield instance, profile_name, profile,run, elapsed, i, iterations, solution, is_new_best
						
						#solution_file = os.path.join(output_path, '_'.join([instance.name, profile_name]) + '.json' )
						#if best_solution is None: continue
						#best_solution.store_json(solution_file)

	with open(output_file, 'w') as out:
		out.write(','.join([
			'instance',
			'profile',
			'run',
			'iteration',
			'total_iterations',
			'cost',
			'k',
			'optimal_cost',
			'optimal_k',
			'elapsed',
			'routes'
		]))
		out.write('\n')
		for iteration in tqdm(runner()):
			instance, profile_name, profile,run, elapsed, i,total_iterations, solution, is_new_best = iteration
			if not is_new_best: continue
			out.write(",".join([
				instance.name,
				profile_name,
				str(run),
				str(i),
				str(total_iterations),
				str(solution.value),
				str(solution.trucks),
				str(instance.optimal_value or 0),
				str(instance.optimal_trucks or 0),
				str(elapsed),
				'"'+str(json.dumps(solution.routes))+'"'
			]))
			out.write('\n')
			out.flush()

					


