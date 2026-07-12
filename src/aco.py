
from enum import Enum
from typing import Literal

import numpy as np

from src.two_opt import two_opt
from src.solution import Solution

from .utils import dict_coalesce

from .base_solver import BaseSolver
from .instance import Instance
class PlacementStrategy(Enum):
  DEPOT = 0
  CUSTOMER = 1
  RANDOM = 2
class TrailContribuionStrategy(Enum):
  BEST_IN_EPOCH = 0
  SUM = 1
#class UpdateStrategy(Enum):
#  DEPOT = 0
#  CUSTOMER = 1
#  RANDOM = 2
class ACOSolver(BaseSolver):
  def __init__(self, instance: Instance, **params):
    """Inizializza i parametri dell'algoritmo Ant Colony Optimization (ACO).

        Configura la dimensione della colonia di formiche, il tasso di evaporazione,
        le strategie di rinforzo elitarie e i pesi degli esponenti (alpha, beta, gamma, lambda)
        utilizzati nella regola di transizione probabilistica per il routing.

        Args:
            instance (Instance): L'oggetto istanza contenente i dati del problema (es. coordinate,
                matrice delle distanze, numero di clienti).
            **params: Parametri di configurazione opzionali passati come keyword arguments.

        Attributes:
            number_of_ants (int): Numero di formiche della colonia. Di default è pari al numero di 
                clienti dell'istanza (`instance.customers`).
            rho (float): Tasso di evaporazione del feromone (0 < rho < 1). Controlla la velocità 
                con cui la traccia di feromone decade a ogni iterazione. Supporta anche l'alias `'evaporation'`.
                Default: `0.1`.
            sigma (float): Numero di formiche elitarie (*elitist ants*). Determina quante formiche associate 
                alla soluzione *best-so-far* rilasciano un surplus di feromone per intensificare la ricerca. 
                Supporta anche l'alias `'elitist_ants'`. Default: `0`.
            alpha (float): Esponente alpha per la traccia di feromone. Regola l'importanza della memoria 
                storica collettiva nella scelta del prossimo nodo. Default: `0`.
            beta (float): Esponente beta per l'informazione euristica (visibilità). Regola l'importanza della 
                componente greedy (es. vicinanza geometrica) nella scelta del prossimo nodo. Default: `1`.
            gamma (float): Esponente gamma per la componente euristica legata alla misura di savings. Default: `0`.
            lambda_ (float): Esponente lambda per la componente euristica legata alla misura della capacità residua. Default: `0`.
            placement_strategy (PlacementStrategy): Strategia di posizionamento iniziale delle formiche 
                sui nodi del grafo all'inizio di ogni iterazione. Default: `PlacementStrategy.CUSTOMER`.
            two_opt (bool): Usa two-opt sulla soluzione di ogni formica.
            initial_tau (float): Valore iniziale di feromone. Default: `.5`
            wind (bool): Aggiunge stocasticamente un rumore normale, con deviazione pari al reciproco della soluzione migliore.
            trail_contribution_strategy (TrailContribuionStrategy): 
              strategia di contributo del feromone, per ogni generazione, di default `BEST_IN_EPOCH`
        """
    super().__init__(instance)

    self.number_of_ants: int = params.get('number_of_ants', instance.customers)
    self.rho: float = dict_coalesce(params, ['rho','evaporation'], .1)
    self.sigma: float = dict_coalesce(params, ['sigma','elitist_ants'], 0)
    self.alpha : float = params.get('alpha', 0)
    self.beta : float = params.get('beta', 1)
    self.gamma : float = params.get('gamma', 0)
    self.lambda_ : float = params.get('lambda_', 0)
    self.placement_strategy: PlacementStrategy = params.get('placement_strategy', PlacementStrategy.CUSTOMER)
    self.two_opt: bool = params.get('two_opt', False)
    
    self.zero = np.zeros((self.distances.shape))
    
    self.eta = self.distances.copy()
    self.eta[ self.eta > 0 ] = 1.0 / self.eta[self.eta > 0]
    
    self.best_solution = None
    self.initial_tau = np.full(self.zero.shape, params.get('initial_tau', .5))
    D = self.distances
    self.mu = D[:, [0]] + D[0, :] - D
    self.wind = params.get('wind', False)

    self.initial_capacity = instance.capacity
    self.trail_contribution_strategy = params.get('trail_contribution_strategy', TrailContribuionStrategy.BEST_IN_EPOCH)
  

  def _run_single_ant(self, tau: np.ndarray, initial_position: int):
    # inizializzo lo stato iniziale della singola formica

    i = initial_position
    eta = self.eta
    capacity = self.initial_capacity
    unvisited_nodes = np.ones(self.dimension, dtype=bool)
    unvisited_nodes[0] = unvisited_nodes[i] = False
    unvisited_count = np.sum(unvisited_nodes)
    trail = self.zero.copy()
    cost = 0

    # è importante che nei singoli tour non appaia il nodo di deposito!
    tours = [[]]
    
    """
      Se la posizione iniziale non è il deposito, aggiungiamo il nodo del primo tour,
      inoltre aggiorniamo il costo e il deposito di feromone.
    """
    if i > 0: 
      tours[-1].append(i)
      cost += self.distances[0,i]
      capacity -= self.demands[i]
      trail[0,i]+=1
    
    # eseguiamo la simulazione Ant System
    while unvisited_count > 0:

      kappa = 1 - (capacity - self.demands) / self.initial_capacity

      epsilon = 1e-6

      """
        Invece di calcolare direttamente la classica matrice Pij in letteratura, la quale è prona a instabilità numerica,
        calcoliamo, per componente, il logaritmo di Pij, cui successivamente normaliziamo.
      """
      log_tau, log_eta, log_kappa, log_mu = (
        np.log(tau[i] + epsilon),
        np.log(eta[i] + epsilon),
        np.log(kappa  + epsilon),
        np.log(self.mu[i]  + epsilon)
      )

      log_pij = (
        self.alpha * log_tau +
        self.beta *  log_eta +
        self.gamma * log_kappa +
        self.lambda_ * log_mu
      )

      Pij = np.exp(log_pij) * unvisited_nodes

      # normaliziamo Pij
      Pij = Pij / np.sum(Pij)

      # sceliamo il prossimo noto da visitare
      j = np.random.choice(self.dimension, p=Pij)
      
      demand_j = self.demands[j]
      
      # se la domanda è maggiore della capacità residua, torniamo al deposito e ricarichiamo la formica
      if demand_j > capacity:
        tours.append([])
        j, capacity = 0, self.initial_capacity
      # altrimenti scarichiamo la capacità, aggiungiamo al tour il nodo e lo segniamo come visitato
      else:
        tours[-1].append(j)
        capacity-=demand_j
        unvisited_nodes[j] = False
        unvisited_count-=1


      # aggiorniamo  feromone e costo con il percorso eseguito
      trail[i,j]=1
      cost += self.distances[i,j]
      
      # spostiamo la formica al nodo j
      i = j
    
    # se la formica non è al deposito, aggiungiamo il costo per tornarci
    if i > 0:
      cost += self.distances[i,0]

    # eseguiamo 2opt sui mini tour
    if self.two_opt:
      cost, trail = self._run_single_ants_two_opt(tours, cost, trail)
    
    # normaliziamo 
    # trail = trail * cost
    # trail[trail > 0] = 1.0 / (trail[trail > 0] * cost) 
    
    #trail = trail * ( 1 / (cost**2) )
    trail = trail * ( 1 / (cost) )
    return cost, trail, tours

  def _run_single_ants_two_opt(self, tours, cost, trail):
      new_cost = cost
      for i, route in enumerate(tours):
        route, savings = two_opt(route, self.distances)
        if savings >  0:
          tours[i] = route
          new_cost -= savings
      # trail = self.zero.copy()
      for tour in [ [0,*tour,0] for tour in tours]:
        for i,j in zip(tour[:1],tour[:-1]):
          trail[i,j] = 1
  
      return cost, trail #, trail
    

  def _run_ants(self, tau: np.ndarray, ants: np.ndarray):
    """
    Genera `number_of_ants` soluzioni, secondo l'algoritmo Ant System.
    Args:
      tau(np.ndarray): matrice dei feromoni
      ants(np.ndarray): vettore delle posizioni iniziali delle formiche
    Returns:
      (costs, trails, routes) (np.ndarray, np.ndarray, list[list[int]]):
      Le soluzioni generate dalle formiche:
        - Vettore dei costi delle soluzioni
        - Matrice/Tensore dei depositi di feromone delle soluzioni/formiche
        - La soluzione delle singole formiche, ogni elemento della lista è una lista di mini-tours conformi al CVRP
    """
    number_of_ants = len(ants)

    costs = np.zeros(number_of_ants)
    trails = np.zeros((number_of_ants,*self.zero.shape))
    routes = [ None for _ in range(number_of_ants) ]

    for i, ant in enumerate(ants):
      cost, trail, tours = self._run_single_ant(tau, ant)
      costs[i] = cost
      trails[i] = trail
      routes[i] = tours


    return costs, trails, routes

  def _trail_contribution(self, best_idx: int, trails: np.ndarray, costs: np.ndarray):
    match self.trail_contribution_strategy:
      case TrailContribuionStrategy.BEST_IN_EPOCH:
        return costs.shape[0] * trails[best_idx]
      case TrailContribuionStrategy.SUM:
        return np.sum(trails[best_idx], axis = 0)

    pass

  def _run_epoch(self, tau: np.ndarray, elitist_trail: np.ndarray):
    """
      Esegue una epoca dell'algoritmo
      Args:
        tau (np.ndarray): 
          La matrice dei feromoni.
        elitist_trail (np.ndarray): 
          La matrice dei depositi delle formiche elitarie
      Returns:
        (tau, solution, best_trail) (np.ndarray, Solution, best_trail): 
          - `tau` Matrice dei feromoni aggiornata.
          - `solution` Migliore soluzione di questa epoca.
          - `best_trail` Matrice del deposito di feromoni della migliore soluzione.
    """
    
    # genera le posizioni iniziali delle formiche secondo la strategia scelta
    ants = self._get_ants_initial_position()
    
    # esegue la logica delle singole formiche
    costs, trails, routes = self._run_ants(tau, ants)


    # seleziona la soluzione migliore in questa epoca    
    best_in_epoch = np.argmin(costs)
    best_routes = routes[best_in_epoch]
    best_cost = costs[best_in_epoch] 
    best_trail = trails[best_in_epoch]


    # aggiorna tau ( feromoni )
    epoch_trail_contribution = trails[best_in_epoch]# np.sum(trails, axis = 0)
    elitist_trail_contribution = self.sigma * elitist_trail
    wind_contribution = (
      np.abs(np.random.normal(0, scale = 1.0/(best_cost), size = self.zero.shape))
      if self.wind else self.zero
    )
    evaporation = (1-self.rho) * tau
    tau = evaporation + epoch_trail_contribution + elitist_trail_contribution + wind_contribution
    tau = np.clip(tau, 1e-9, 1)


    return tau, Solution(best_routes, best_cost), best_trail
    

  def run(self, epochs: int):
    """
    Esegue l'algoritmo un numero `epochs` di volte.
    Args:
      epochs (int): Numero di epoche/generazioni per cui eseguire l'algoritmo.
    Returns:
      generator (Generator[Solution]): Un lazy-generator di soluzioni.
    """
    
    # Inizializiamo a None la soluzione migliore ( non settata quindi )
    best_solution = None
    # Inizializiamo a zero il deposito di feromone delle formiche elitarie 
    elitist_trail = self.zero
    # Copiamo tau 
    tau = self.initial_tau.copy()

    # per ogni epoca
    for epoch in range(epochs):
      # eseguiamo la subroutine che esegue l'epoca
      tau, sol, trail = self._run_epoch(tau, elitist_trail)

      # se è la prima soluzione, oppure abbiamo una nuova soluzione migliore, la salviamo
      if best_solution is None or best_solution.value > sol.value:
        sol.set_epoch(epoch)
        best_solution = sol
        elitist_trail = trail
      
      # emette la migliore soluzione fino a questa epoca
      yield best_solution
    
    # restituisce la miglioe soluzione fino a questa epoca 
    return best_solution

  def __run_naive__(self, evaluations):
    """
      Algoritmo iniziale, successivamente ripulito e riorganizzato
    """
    self.best_solution = None
    self.best_solution_value = None
    self.best_solution_trail = self.zero
    dimension = self.dimension
    rho = self.rho
    sigma = self.sigma
    tau = self.initial_tau.copy()
    eta = self.eta
    mu = self.mu
    demands = self.demands
    d = self.distances
    initial_capacity = self.capacity

    alpha, beta, gamma, lambda_ = self.alpha, self.beta, self.gamma, self.lambda_

    for epoch in range(evaluations):
      ants = self._get_ants_initial_position()
      number_of_ants = len(ants)

      costs = np.zeros(number_of_ants)
      trails = np.zeros((number_of_ants,*self.zero.shape))
      tours = []

      for idx, initial_position in enumerate(ants):
        capacity = initial_capacity
        unvisited_nodes = np.ones(dimension, dtype=bool)
        unvisited_nodes[0] = unvisited_nodes[initial_position] = False
        unvisited_count = np.sum(unvisited_nodes)
        trail = self.zero.copy()
        cost = 0
        routes = [[]]
        i = int(initial_position)
        
        if i > 0: 
          routes[-1].append(i)
          cost += d[0,i]
          trail[0,i]+=1

        while unvisited_count > 0:
          kappa = 1 - (capacity - demands) / initial_capacity
          
          #Pij = tau_eta[i] * (kappa ** lambda_) * (mu_ ** sigma) * unvisited_nodes
          #Pij_d = np.sum(Pij)
          #Pij = Pij / Pij_d if Pij_d > 0 else Pij
          epsilon = 1e-9
          # modifiche per stabilità numerica!!!
          tau_log, eta_log, kappa_log, mu_log = (
            np.log(tau[i] + epsilon),
            np.log(eta[i] + epsilon),
            np.log(kappa  + epsilon),
            np.log(mu[i]  + epsilon)
          )

          log_pij = (
            alpha * tau_log +
            beta *  eta_log +
            gamma * kappa_log +
            lambda_ * mu_log
          )

          Pij = np.exp(log_pij) * unvisited_nodes

          Pij = Pij / np.sum(Pij)

          j = np.random.choice(dimension, p=Pij)

          demand_j = demands[j]
          if demand_j > capacity:
            routes.append([])
            j, capacity = 0, initial_capacity
          else:
            routes[-1].append(j)
            capacity-=demand_j
            unvisited_nodes[j] = False
            unvisited_count-=1

          trail[i,j]+=1
          cost += d[i,j]
          i = j
        
        if i > 0:
          cost += d[i,0]

        if self.two_opt:
          for i, route in enumerate(routes):
            route, savings = two_opt(route, d)
            if savings >  0:
              routes[i] = route
              cost -= savings
        
        trail = trail * cost
        trail[trail > 0] = 1.0 / (trail[trail > 0] * cost) 
        

        trails[idx] = trail
        costs[idx] = cost
        tours.append(routes)
      
      best_idx = np.argmin(costs)

      epoch_trail_contribution = np.sum(trails, axis = 0)
      best_solution_contribution = sigma * best_solution_trail
      tau = (1-rho) * tau + epoch_trail_contribution + best_solution_contribution

      tau = np.clip(tau, 1e-6,np.inf)
      
      if best_solution_value is None or costs[best_idx] < best_solution_value:
        best_solution_value = costs[best_idx]
        best_solution_trail = trails[best_idx]
        best_solution = Solution(tours[best_idx], best_solution_value)
      yield best_solution


  def _get_ants_initial_position(self):
    """
      Genera il piazzamento iniziale delle formiche secondo la strategia scelta.
      Returns:
        (np.ndarray): 
          un vettore `|number_of_ants|` dove ogni componente corrisponde alla posizione iniziale della k-esima formica.
    """
    match self.placement_strategy:
      case PlacementStrategy.DEPOT:
        return np.zeros((self.customers), dtype=int)
      case PlacementStrategy.CUSTOMER:
        return np.arange(self.customers, dtype=int) + 1
      case PlacementStrategy.RANDOM:
        return np.random.uniform(0, self.customers, self.customers).astype(int) + 1