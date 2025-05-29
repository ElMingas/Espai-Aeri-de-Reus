class NavPoint:
    def __init__(self, number, name, latitude, longitude):
        '''self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors = []'''

        self.number = number
        self.name = name
        self.y = latitude
        self.x = longitude
        self.neighbors = []

    def __repr__(self):
        return f"NavPoint({self.number}, {self.name}, {self.x}, {self.y})"

    def __lt__(self, other):
        # Compare nodes based on their names for consistent ordering
        return self.name < other.name

def addneighbor(n1, n2):
    # Añadir n2 en los vecinos de n1 si todavia no lo es
    if n2 not in n1.neighbors:
        n1.neighbors.append(n2)
        return True
    return False


# Distancia euclidea
def distance(n1, n2):
    d = float(((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2) ** 0.5)
    return d


NavPoint_lict = []
NavPoint_index = {} # Por ID
#NavPoint_name_index = {} # Por name
def AddNavPoint(file):
    # Limpiar files existentes
    NavPoint_lict.clear()
    NavPoint_index.clear()

    if file == 'ECAC':
        file = 'ECAC/ECAC_nav.txt'
    elif file == 'Spain':
        file = 'Spain/Spain_nav.txt'
    elif file == 'Catalonia':
        file = 'catalonia/catalonia_nav.txt'

    with open(file, 'r') as f:
        for line in f:
            point_info = line.split(' ')
            if len(point_info) < 4:
                continue

            number = int(point_info[0])
            name = point_info[1]
            lat = float(point_info[2])
            lon = float(point_info[3])

            point = NavPoint(number, name, lat, lon)

            NavPoint_lict.append(point)
            NavPoint_index[number] = point
            #NavPoint_name_index[name] = point

'''def get_navpoint(number):
    for point in NavPoint_list:
        if int(point.number) == int(number):
            return point
    return None'''