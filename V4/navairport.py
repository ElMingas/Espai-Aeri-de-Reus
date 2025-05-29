class NavAirport:
    def __init__(self, name, sid, star):
        self.name = name
        self.sid = sid
        self.star = star

Airport_list = []

def AddNavAirport(file):
    if file == 'Europe':
        file = 'Eur_aer.txt'
    elif file == 'Spain':
        file = 'Spain_aer.txt'
    elif file == 'Catalonia':
        file = 'Cat_aer.txt'

    with open(file, 'r') as f:
        sid = []
        star = []
        name = None

        for line in f:
            line = line.strip('\n')
            i = line.split('.')
            if not name and len(i) == 1:
                name = i[0]
            elif name and len(i) == 1:
                Airport_list.append(NavAirport(name, sid, star))
                name = i[0]
                sid = []
                star = []
            elif i[1] == 'D':
                sid.append(line)
            else:
                star.append(line)

'''def add_nav_airport(file):
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
            if not name and len(i) == 1:
                name = i[0]
            elif name and len(i) == 1:
                Airport_list.append(NavAirport(name, sid, star))
                name = i[0]
                sid = []
                star = []
            elif i[1] == 'D':
                sid.append(line)
            else:
                star.append(line)'''