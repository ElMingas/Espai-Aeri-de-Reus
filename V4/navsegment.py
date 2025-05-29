from navpoint import *


class NavSegment:
    def __init__(self, origin, destination, dist):
        # Asegurar que origin y dest sean nodos
        '''if not isinstance(OriginNumber, NavPoint) or not isinstance(DestinationNumber, NavPoint):
            raise TypeError("origin and destination must be node objects")'''

        self.origin = origin
        self.destination = destination
        self.cost = dist

        addneighbor(origin, destination)

    def __repr__(self):
        return f"NavSegment({self.origin}, {self.destination}, {self.cost})"

NavSegment_list = []
def AddNavSegment(file):
    NavSegment_list.clear()

    if file == 'ECAC':
        file = 'ECAC/ECAC_seg.txt'
    elif file == 'Spain':
        file = 'Spain/Spain_seg.txt'
    elif file == 'Catalonia':
        file = 'catalonia/catalonia_seg.txt'

    with open(file, 'r') as f:
        for line in f:
            seg_info = line.split(' ')
            if len(seg_info) != 3:
                continue

            origin_number = int(seg_info[0])
            dest_number = int(seg_info[1])
            dist = float(seg_info[2])

            '''if origin_number in NavPoint_index and dest_number in NavPoint_index:
                origin = NavPoint_index[origin_number]
                dest = NavPoint_index[dest_number]
                segment = NavSegment(origin, dest, distance)
                NavSegment_list.append(segment)'''

            origin = NavPoint_index[origin_number]
            dest = NavPoint_index[dest_number]
            segment = NavSegment(origin, dest, dist)
            NavSegment_list.append(segment)
