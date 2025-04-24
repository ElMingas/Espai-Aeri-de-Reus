from node import *
n1 = node ('aaa', 0, 0)
n2 = node ('bbb', 3, 4)
print (distance(n1,n2))
print (addneighbor(n1, n2))
print (addneighbor(n1, n2))
print (n1.__dict__)
for n in n1.neighbors:
    print ( n.__dict__)