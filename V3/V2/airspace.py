from navpoint import *
from navsegment import *
from navairport import *

class Airspace:
    def __init__(self, NavPoints, NavSegments, NavAirports):
        '''self.points = NavPoints
        self.segments = NavSegments
        self.airports = NavAirports'''

        self.nodes = NavPoints
        self.segments = NavSegments
        self.airports = NavAirports
    
def Create_Airspace():
    espai_aeri = Airspace(NavPoint_lict, NavSegment_list, Airport_list)