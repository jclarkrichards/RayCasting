from line import Line
from vectors import Vector2D
from random import randint
from maps import mapRaw

class Node(object):
    def __init__(self, name="", segment=None, parent=None):
        self.name = name
        self.segments = [] #usually only contains 1, but can contain many
        self.position = segment.p1
        self.direction = None
        self.AddSegment(segment)
        self.parent = parent
        self.children = {"Front":None, "Back":None}
        self.visited = False
        
    def AddSegment(self, segment):
        '''Turn segment into unit vector perpendicular to segment'''
        self.segments.append(segment)
        if self.direction is None:
            d = Vector2D(segment.vec.y, segment.vec.x * -1)
            d = d.norm()
            self.direction = d
        #print self.position, d

        
class BinaryTree(object):
    def __init__(self, linelist):
        self.linelist = linelist
        self.tree = None

    def divideLines(self, lines, side=None, parent=None):
        newlines = []
        frontlines = []
        backlines = []
        #The best line to make root node is a line in the middle
        #For now we can just randomly choose one
        n = randint(0, len(lines)-1) 
        if parent is None:
            node = Node(segment=lines[n])
            self.tree = node
        else:
            node = Node(segment=lines[n])
            parent.children[side] = node
            node.parent = parent

        for i in range(len(lines)):
            if i != n:
                t = lines[n].FindIntersect(lines[i], forward=False)
                if t != None and t != 0 and t != 1:
                    vec = lines[n].p1 + lines[n].vec * t
                    line1 = lines[i].p1.toTuple() + vec.toTuple()
                    line2 = vec.toTuple() + lines[i].p2.toTuple()
                    newlines.append(Line(*line1))
                    newlines.append(Line(*line2))
                else:
                    newlines.append(lines[i])

        for i in range(len(newlines)):
            v1 = newlines[i].p1 - node.position
            v2 = newlines[i].p2 - node.position
            if node.direction.dot(v1) < 0 or node.direction.dot(v2) < 0:
                backlines.append(newlines[i])
            else:
                frontlines.append(newlines[i])


        if len(frontlines) > 1:
            self.divideLines(frontlines, "Front", node)
        elif len(frontlines) == 1:
            node.children["Front"] = Node(segment=frontlines[0])
            node.children["Front"].parent = node

        if len(backlines) > 1:
            self.divideLines(backlines, "Back", node)
        elif len(backlines) == 1:
            node.children["Back"] = Node(segment=backlines[0])
            node.children["Back"].parent = node


    def walk(self, node, level):
        '''Walk through the tree in order to map it out'''
        print node.position, node.direction
        if node.children["Front"] is not None:
            print "FRONT Level "+str(level+1)
            self.walk(node.children["Front"], level+1)
        if node.children["Back"] is not None:
            print "BACK Level "+ str(level+1)
            self.walk(node.children["Back"], level+1)
    
    def manual(self):
        '''Make tree manually for a specific list of lines.'''
        self.tree = Node("root", self.linelist[0])
        nodeB = Node("B", self.linelist[1])
        nodeC = Node("C", self.linelist[2])
        nodeD = Node("D", self.linelist[3])
        nodeE = Node("E", self.linelist[4])
        nodeF1 = Node("F1", self.linelist[5])
        nodeF2 = Node("F2", self.linelist[6])
        nodeG2 = Node("G2", self.linelist[7])
        nodeG1 = Node("G1", self.linelist[8])
        nodeH22 = Node("H22", self.linelist[9])
        nodeH21 = Node("H21", self.linelist[10])
        nodeH1 = Node("H1", self.linelist[11])
        
        #connect the nodes
        self.tree.children["Front"] = nodeE
        self.tree.children["Back"] = nodeB
        nodeB.children["Front"] = nodeF2
        nodeB.children["Back"] = nodeC
        nodeC.children["Front"] = nodeG1
        nodeC.children["Back"] = nodeD
        nodeD.children["Front"] = nodeH21
        nodeE.children["Front"] = nodeF1
        nodeF1.children["Front"] = nodeH1
        nodeF2.children["Front"] = nodeG2
        nodeG1.children["Front"] = nodeH22

        nodeB.parent = self.tree
        nodeE.parent = self.tree
        nodeC.parent = nodeB
        nodeD.parent = nodeC
        nodeH21.parent = nodeD
        nodeG1.parent = nodeC
        nodeH22.parent = nodeG1
        nodeF2.parent = nodeB
        nodeG2.parent = nodeF2
        nodeF1.parent = nodeE
        nodeH1.parent = nodeF1


    
#walls = mapRaw()
#bt = BinaryTree(walls)
#bt.divideLines(walls)
#bt.walk(bt.tree, 0)
    
