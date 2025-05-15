class NavAirport:
    def __init__(self, name, SID, STAR):
        self.name = name
        self.sid = SID
        self.star = STAR

Airport_list = []

def AddNavAirport(file):
    if file == 'Europe':
        file = 'Eur_aer.txt'
    elif file == 'Spain':
        file = 'Spain_aer.txt'
    else:
        file = 'Cat_aer.txt'
    
    with open(file, 'r') as f:
        sid = []
        star = []
        name = None
        for line in f:
            line = line.strip('\n')
            i = line.split('.')
            if name == None and len(i) == 1:
                name = i[0]
            elif name != None and len(i) == 1:
                Airport_list.append(NavAirport(name, sid, star))
                name = i[0]
                sid = []
                star = []
            elif i[1] == 'D':
                sid.append(line)
            else:
                star.append(line)

'''AddNavAirport('Catalonia')
print(Airport_list[3].star)
print(Airport_list[3].sid)'''


