import sys


class Instance:
	"""
	Describes an of the CVRP
	"""
	def __init__(self,
		name: str,
		comment: str,
		dimension: int,
		edge_weight_type: str,
		capacity: int,
		author: str,
		optimal_trucks: int,
		optimal_value: int,
		node_coords: dict[int, tuple[int, int]],
		node_demand: dict[int, int],
		depot_node: int,
	):
		self.name = name
		self.comment = comment
		self.dimension = dimension
		self.edge_weight_type = edge_weight_type
		self.capacity = capacity
		self.author = author
		self.optimal_trucks = optimal_trucks
		self.optimal_value = optimal_value
		self.node_coords = node_coords
		self.node_demand = node_demand
		self.depot_node = depot_node

	@staticmethod
	def load_vrp(path: str):
		"""
		Loads a VRP file
		"""
		name = None
		comment = None
		dimension = None
		edge_weight_type = None
		capacity = None
		author = None
		optimal_trucks = None
		optimal_value = None
		node_coords = {}
		node_demand = {}
		depot_node = None
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
							optimal_value = int(optimal_value.split(':')[1].strip())

						except Exception as exc:
							print(exc, file= sys.stderr)
					case 'TYPE':
						if value != 'CVRP':
							raise Exception("Instance type must be CVRP.")
					case 'DIMENSION':
						if not value.isnumeric():
							raise Exception("Dimension is not a number.")
						dimension = int(value)
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
						for i in range(dimension):

							index, x, y = tuple( map(float,next(lines).strip().split(' ')))
							node_coords[index] = (x,y)
					case 'DEMAND_SECTION':
						if dimension is None:
							raise Exception("DEMAND_SECTION red before DIMENSION")
						for i in range(dimension):
							index, demand = tuple(map(int,next(lines).strip().split(' ')))
							node_demand[index] = demand

					case 'DEPOT_SECTION':
						if dimension is None:
							raise Exception("DEPOT_SECTION red before DIMENSION")
						depot_node = int(next(lines).strip())
						_ = int(next(lines).strip())

			return Instance(
				name,
				comment,
				dimension,
				edge_weight_type,
				capacity,
				author,
				optimal_trucks,
				optimal_value,
				node_coords,
				node_demand,
				depot_node
			)
