class node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

def AddNeighbor(n1, n2):
    if n2 not in n1.neighbors:
        n1.neighbors.append(n2)
        return True
    else:
        return False

def Distance(n1, n2):
    d = ((n2.x - n1.x)**2 + (n2.y - n1.y)**2)**0.5
    return d