from segment import *
from node import *
import matplotlib.pyplot as plt
class Graphs:
    def __init__(self):
        self.nodes = []
        self.segments = []

def AddNode(g, n):
    if n not in g.nodes:
        g.nodes.append[n]
        return True and g
    else:
        return False and g


def AddSegment(g, name, nameOriginNode, nameDestinationNode):
    i = 0
    while i < len(g.nodes):
        no = g.nodes[i]
        if no.name == nameOriginNode:
            break
        else:
            i += 1
    i = 0
    while i < len(g.nodes):
        nd = g.nodes[i]
        if nd.name == nameDestinationNode:
            break
        else:
            i += 1
    s = (name, no, nd)
    found = False
    if s not in g.segments:
        g.segments.append[s]
        return True and g
    else:
        return False and g
    

def GetClosest(g, x, y):
    i = 1
    d = float((x - g.nodes[0].x)**2 + (y - g.nodes[0].y)**2)**0,5
    while i < len(g.nodes):
        n = g.nodes[i]
        nearest = g.nodes[0]
        pd = float((x - n.x)**2 + (y - n.y)**2)**0,5
        if pd > d:
            d = pd
            nearest = g.nodes[i]
        i += 1
    return nearest

def Plot (g):
    i = 0
    while i < len(g.segments):
        s = g.segments[i]
        x_values = [s.origin.x, s.destination.x]
        y_values = [s.origin.y, s.destination.y]
        dx = (s.destination.x - s.origin.x)/2
        dy = (s.destination.y - s.origin.y)/2
        plt.text(dx, dy, s.cost, fontsize = 7, color = 'blue', ha = 'center')
        plt.plot(x_values, y_values)
        i += 1
    i = 0
    while i < len(g.nodes):
        n = g.nodes[i]
        plt.scatter(n.x, n.y, color = 'red')
        i += 1
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    plt.title('Espai aeri de Reus')
    plt.show()



