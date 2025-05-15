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
        return f"NavPoint({self.number}, {self.name})"

def addneighbor(n1, n2):
    #Añadir n2 en los vecinos de n1 si todavia no lo es
    if n2 not in n1.neighbors:
        n1.neighbors.append(n2)
        return True
    return False

#Distancia euclidea
def distance(n1, n2):
    d = float(((n2.x - n1.x)**2 + (n2.y - n1.y)**2)**0.5)
    return d

NavPoint_lict = []
NavPoint_index = {}

def AddNavPoint(file):
    if file == 'Europe':
        file = 'Eur_nav.txt'
    elif file == 'Spain':
        file = 'Spain.nav.txt'
    else:
        file = 'Cat_nav.txt'
    
    with open(file, 'r') as f:
        for line in f:
            point_info = line.split(' ')

            number = int(point_info[0])
            name = point_info[1]
            lat = float(point_info[2])
            lon = float(point_info[3])

            point = NavPoint(number, name, lat, lon)

            NavPoint_lict.append(point)
            NavPoint_index[number] = point

'''def get_navpoint(number):
    for point in NavPoint_list:
        if int(point.number) == int(number):
            return point
    return None'''

'''AddNavPoint('Catalonia')
print(NavPoint_list[0].longitude)
print(NavPoint_list[1].longitude)
print(NavPoint_list[2].name)
print(NavPoint_list[3].name)
print(NavPoint_list[4].name)
print(NavPoint_list[5].name)'''