from node import *

class segment:
    def __init__(self, name, origin, destination):
        #Asegurar que origin y dest sean nodos
        if not isinstance(origin, node) or not isinstance(destination, node):
            raise TypeError("origin and destination must be node objects")

        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = distance(origin, destination)

        #Añadir vecinos automaticamente al crear un segmento
        addneighbor(origin, destination)