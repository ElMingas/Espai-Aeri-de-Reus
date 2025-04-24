class node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

    #Salida de info de nodo mas claro
    def __repr__(self):
        return f"node('{self.name}', {self.x}, {self.y})"

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