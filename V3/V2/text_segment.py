from segment import *

n1 = Node ('aaa', 0, 0)
n2 = Node ('bbb', 3, 4)
n3 = Node ('ccc', 10, 15)
s1 = Segment('aaaa', n1, n2)
s2 = Segment('bbbb', n2, n3)

print(s1.destination)
print(s2.cost)
print(s1.origin.neighbors)