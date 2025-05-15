from navpoint import *

class NavSegment:
    def __init__(self, OriginNumber, DestinationNumber, Distance):
        # Asegurar que origin y dest sean nodos
        '''if not isinstance(OriginNumber, NavPoint) or not isinstance(DestinationNumber, NavPoint):
            raise TypeError("origin and destination must be node objects")'''

        self.origin = OriginNumber
        self.destination = DestinationNumber
        self.cost = Distance

        addneighbor(OriginNumber, DestinationNumber)

NavSegment_list = []
def AddNavSegment(file):
    if file == 'Europe':
        file = 'Eur_seg.txt'
    elif file == 'Spain':
        file = 'Spain_seg.txt'
    else:
        file = 'Cat_seg.txt'
    
    with open(file, 'r') as f:
        for line in f:
            seg_info = line.split(' ')
            if len(seg_info) != 3:
                continue

            origin_number = int(seg_info[0])
            dest_number = int(seg_info[1])
            distance = float(seg_info[2])

            '''if origin_number in NavPoint_index and dest_number in NavPoint_index:
                origin = NavPoint_index[origin_number]
                dest = NavPoint_index[dest_number]
                segment = NavSegment(origin, dest, distance)
                NavSegment_list.append(segment)'''

            origin = NavPoint_index[origin_number]
            dest = NavPoint_index[dest_number]
            segment = NavSegment(origin, dest, distance)
            NavSegment_list.append(segment)
