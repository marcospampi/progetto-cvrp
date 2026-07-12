import sys
import numpy as np

class Instance:
	"""
	Describes an of the CVRP
	"""
	def __init__(self,
		name: str,
		comment: str,
		dimension: int,
		customers: int,
		edge_weight_type: str,
		capacity: int,
		author: str,
		optimal_trucks: int,
		optimal_value: int,
		node_coords: np.ndarray,
		node_demand: np.ndarray,
		distances: np.ndarray
	):
		self.name = name
		self.comment = comment
		self.dimension = dimension
		self.customers = customers
		self.edge_weight_type = edge_weight_type
		self.capacity = capacity
		self.author = author
		self.optimal_trucks = optimal_trucks
		self.optimal_value = optimal_value
		self.node_coords = node_coords
		self.node_demand = node_demand
		self.distances = distances
		

	@staticmethod
	def load_vrp(path: str):
		"""
		Loads a VRP file
		"""
		name = None
		comment = None
		dimension = None
		customers = None
		edge_weight_type = None
		capacity = None
		author = None
		optimal_trucks = None
		optimal_value = None
		node_coords = None
		node_demand = None
		distances = None
		with open(path, 'r', encoding='UTF-8') as file:
			lines = iter(file)
			current_key = None
			
			while current_key != 'EOF':
				next_line = next(lines).split(':')
				current_key = next_line[0].strip()
				value = ':'.join(next_line[1:]).strip() if len(next_line) > 1 else None

				match current_key:
					case 'NAME':
						name = value
					case 'COMMENT':
						comment = value
						try:
							value = value[1:-1] # removes parenthesis
							print(value)
							value = tuple(map(str.strip,value.split(','))) # splits the comment

							author, optimal_trucks, optimal_value = value

							optimal_trucks = int(optimal_trucks.split(':')[1].strip())
							optimal_value = float(optimal_value.split(':')[1].strip())

						except Exception as exc:
							pass
					case 'TYPE':
						if value != 'CVRP':
							raise Exception("Instance type must be CVRP.")
					case 'DIMENSION':
						if not value.isnumeric():
							raise Exception("Dimension is not a number.")
						dimension = int(value)
						customers = dimension - 1
						
						# initializes coords, demand and ndistances
						node_coords = np.zeros((dimension, 2), dtype=float)
						node_demand = np.zeros((dimension), dtype=int)
						distances = np.zeros((dimension,dimension), dtype=float)

					case 'EDGE_WEIGHT_TYPE':
						if value != 'EUC_2D':
							raise Exception("Supported EDGE_WEIGHT_TYPE is EUC_2D, '%s' given" % value)
						edge_weight_type = value
					case 'CAPACITY':
						if not value.isnumeric():
							raise Exception("Capacity is not a number.")
						capacity = int(value)					
					case 'NODE_COORD_SECTION':
						if dimension is None:
							raise Exception("NODE_COORD_SECTION red before DIMENSION")
						for _ in range(dimension):

							index, x, y = next(lines).strip().split(' ')
							index, x, y = int(index) - 1, float(x), float(y)
							node_coords[index] = (x,y)
					case 'DEMAND_SECTION':
						if dimension is None:
							raise Exception("DEMAND_SECTION red before DIMENSION")
						for i in range(dimension):
							index, demand = next(lines).strip().split(' ')
							index, demand = int(index) - 1, int(demand)
							node_demand[index] = demand

					case 'DEPOT_SECTION':
						if dimension is None:
							raise Exception("DEPOT_SECTION red before DIMENSION")						
						pass
					case 'OPTIMAL_VALUE':
						optimal_value = float(value)
					case 'OPTMAL_TRUCKS':
						optimal_trucks = int(value)
					case 'EOF':
						break
		
		for i in range(dimension):
			ix, iy = node_coords[i]
			for j in range(i + 1, dimension):
				jx, jy = node_coords[j]
				distances[i,j] = distances[j,i] = (
					0.0 if i == j else np.hypot((ix-jx), (iy-jy)) # ((ix-jx)**2+(iy-jy)**2)**.5  # 
				)


		return Instance(
			name,
			comment,
			dimension,
			customers,
			edge_weight_type,
			capacity,
			author,
			optimal_trucks,
			optimal_value,
			node_coords,
			node_demand,
			distances
			
		)
