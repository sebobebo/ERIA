# -*- coding: utf-8 -*-


import re
import math

file = open("grid.txt","r")
raw = file.readlines()
file.close()

grid = []
for line in reversed(raw):
    cleaned = re.sub("\s", "", line)
    grid.append(cleaned)

NX = len(grid[0]) - 1
NY = len(grid) - 1

class Node:

    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  if parent == None else parent.g + 1
        self.f = self.g + self.h()

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return str([self.x, self.y, self.f, self.g])
    def __repr__(self):
        return str([self.x, self.y, self.f, self.g])

    def neighbours(self):
        nbs = []
        x = self.x
        y = self.y
        nbspos = [[x, y+1],[x, y-1],[x-1,y],[x+1,y]]
        for npos in nbspos:
            if npos[0] < 0 or npos[0] > NX or npos[1] < 0 or npos[1] > NY:
                continue
            if grid[npos[1]][npos[0]] == '5':
                continue
            nbs.append(Node(npos[0], npos[1], self))
        return nbs

    def h(self):
        return math.sqrt((self.x - NX)**2 + (self.y - NY)**2)

def onlist(elem, _list):
    for i in range(len(_list)):
        if _list[i] == elem:
            return i
    return -1

def add2list(elem, _list):
    i = 0
    for i in range(len(_list)):
        if _list[i].f < elem.f:
            continue
        break
    _list.insert(i, elem)

# implementacja algorytmu A*
start = Node(0, 0, None)
stop = Node(NX, NY, None)

opened = [start]
closed = []

while(opened):
    node = opened[0]
    del(opened[0])
    closed.append(node)
    if node == stop:
        break
    
    for candidate in node.neighbours():
        iop = onlist(candidate, opened)
        icl = onlist(candidate, closed)

        if iop + icl == -2:
            add2list(candidate, opened)
        else:
            if iop == -1:
                if candidate.f < closed[icl].f:
                    del(closed[icl])
                    add2list(candidate, opened)
            else:
                if candidate.f < opened[iop].f:
                    del(opened[iop])
                    add2list(candidate, opened)

else: 
    print("Nie ma rozwiazania")
    file = open("./result.txt","w")
    file.writeline("Nie ma rozwiazania")
    file.close()
    exit(-1)


while (node):
#    print(node)
    x = node.x
    y = node.y
    line = list(raw[NY - y])
    line[2*x] = '3'
    raw[NY - y] = ''.join(line)
    node = node.parent

file = open("./result.txt","w")
file.writelines(raw)
file.close()
