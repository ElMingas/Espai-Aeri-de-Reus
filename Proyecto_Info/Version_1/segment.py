class segment:
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = float((destination.x - origin.x)**2 + (destination.y - origin.y)**2)**0.5
    
       