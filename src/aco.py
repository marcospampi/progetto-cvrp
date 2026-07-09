import numpy as np

from .base_solver import BaseSolver
from .solution import Solution

class ACO(BaseSolver):
	def __init__(self, instance, ants: int, *, rho: float = 0.5, alpha: float = 1.0, beta: float = 2.0, tau_min: float = 1e-5, tau_max: float = 1 ):
		super().__init__(instance)
		self.ants = ants
		self.rho = rho	
		self.alpha = alpha
		self.beta = beta
		self.tau_max = tau_max
		self.tau_min = tau_min
	
	def run(self, evaluations):

		matshape = (self.dim, self.dim)

		generations = int(np.ceil(float(evaluations) / self.ants))

		# feromone
		tau = np.ndarray(matshape) # np.random.uniform(0.1,.2, size=matshape)
		tau[:] = 1 / (self.dim - 1)
		# reciproco della distanza
		eta = np.zeros(matshape)
		np.reciprocal(self.distances, where= self.distances != 0, out=eta )
		# il deposito non è visitabile
		eta[:,0] = 0
		best_so_far = 0
		for gen in range(generations):
			best_solution, tau, eta = self._run_generation(tau, eta, best_so_far)
			best_so_far = max([best_so_far, best_solution.fitness])
			yield best_solution

	def _run_generation(self, tau: np.ndarray, eta: np.ndarray, best_so_far: float):
			solutions = []
			fitnesses = np.zeros((self.ants))
			dtau = []
			for ant in range(self.ants):
				solution, dtau_ = self._run_ant(tau, eta)
				solutions.append(solution)
				fitnesses[ant] = solution.fitness
				dtau.append(dtau_)
			# strategia best fitness
			best_solution_idx = np.argmax(fitnesses)
			best_solution: Solution = solutions[best_solution_idx]
			
			# trail update
			tau = (1.0 - self.rho) * tau + dtau[best_solution_idx] * best_solution.fitness / (best_so_far if best_so_far > 0 else 1)
			tau = np.clip(tau, self.tau_min, self.tau_max)
			
			
			return best_solution, tau, eta
	
	def _run_ant(self, tau: np.ndarray, eta: np.ndarray ):
		capacity = self.initial_capacity
		# il vettore dei nodi non visitati
		unvisited_nodes = np.array([ i > 0 for i in range(self.dim)], dtype=bool)
		
		# i percorsi ( si inizia da 0 e si finisce a 0 )
		routes = [[0]]

		# il nodo corrente
		i, j = 0,0

		dtau = np.zeros(tau.shape)
		
		while np.sum(unvisited_nodes) > 0:
			i = j
			# calcola Pij ( numeratore ) , moltiplica per unvisited_nodes per selezionare solo nodi da visitare
			Pij = self._compute_pij_numerator(tau, eta, i, capacity) * unvisited_nodes.astype(np.float32)
			
			# normalizza Pij ( divide le componenti per la somma )
			Pij_denominator = np.sum(Pij)
			Pij = Pij / Pij_denominator  if Pij_denominator > 0 else Pij

			# scelgo il massimo argomento su Pij
			j = np.random.choice(self.dim, p=Pij if Pij_denominator > 0 else None)
			# carico la domanda j
			j_demand = self.demands[j]				
			
			# se la domanda è maggiore della capacità, torna al deposito e ricarica il furgone
			if j_demand > capacity:
				# torna al deposito
				routes[-1].append(0)
				j = 0

				# ricarica il furgone
				capacity = self.initial_capacity
				
				# crea un nuovo percorso
				routes.append([0])
			# altrimenti
			else:
				# aggiungi il nodo al route in corso
				routes[-1].append(j)
				# aggiorna la capacità
				capacity -= j_demand
				# setta il nodo corrente
				# rimuovi il nodo dalla lista dei nodi non visitati
				unvisited_nodes[j] = False
			
			dtau[i,j]+=1
		# soluzione
		routes[-1].append(0)
		dtau[i,0]+=1
		solution = Solution(routes, self.distances)
		dtau = dtau * solution.fitness 
		return solution, dtau

	def _compute_pij_numerator(self, tau: np.ndarray, eta: np.ndarray, i: int, capacity: float):
		return (tau[i] ** self.alpha) * (eta[i] ** self.beta)


		

				



