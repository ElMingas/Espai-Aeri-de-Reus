from node import *
from segment import *
n1 = node ('aaa', 0, 0)
n2 = node ('bbb', 3, 4)
n3 = node ('ccc', 10, 15)
s1 = segment('aaaa', n1, n2)
s2 = segment('bbbb', n2, n3)

print(s1.destination)
print(s2.cost)
print(s1.origin.neighbors)