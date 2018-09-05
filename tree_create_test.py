from line import Line
from vectors import Vector2D
from mapper import Node
from random import randint


def divideLines(lines, side=None, parent=None):
    newlines = []
    frontlines = []
    backlines = []
    #The best line to make root node is a line in the middle
    #For now we can just randomly choose one
    n = randint(0, len(lines)-1) 
    if parent is None:
        node = Node(segment=lines[n])
        
    else:
        node = Node(segment=lines[n])
        parent.children[side] = node
        node.parent = parent

    for i in range(len(lines)):
        if i != n:
            t = lines[n].FindIntersect(lines[i], forward=False)
            if t != None and t != 0 and t != 1:
                #print t
                vec = lines[n].p1 + lines[n].vec * t
                line1 = lines[i].p1.toTuple() + vec.toTuple()
                line2 = vec.toTuple() + lines[i].p2.toTuple()
                #print line1
                #print line2
                newlines.append(Line(*line1))
                newlines.append(Line(*line2))
            else:
                newlines.append(lines[i])

    #Loop through new line list and split it into frontlines and backlines
    for i in range(len(newlines)):
        v1 = newlines[i].p1 - node.position
        v2 = newlines[i].p2 - node.position
        if node.direction.dot(v1) < 0 or node.direction.dot(v2) < 0:
            backlines.append(newlines[i])
        else:
            frontlines.append(newlines[i])


    if len(frontlines) > 1:
        divideLines(frontlines, "Front", node)
    elif len(frontlines) == 1:
        node.children["Front"] = Node(segment=frontlines[0])

    if len(backlines) > 1:
        divideLines(backlines, "Back", node)
    elif len(backlines) == 1:
        node.children["Back"] = Node(segment=backlines[0])

    return node

"""
#===================================================
lines = [Line(160,120,240,120), Line(240,120,240,200),
         Line(240,200,160,200), Line(160,200,160,120),
         Line(560,40,40,40), Line(560,360,560, 40),
         Line(40,360,560,360), Line(40,40,40,360)]

#fulltree = None
#test = Node()
test = divideLines(lines)
print test.children
#print fulltree.children

print test.position
print "===================="
if test.children["Front"] is not None:
    print test.children["Front"].position

if test.children["Back"] is not None:
    print test.children["Back"].position

"""
