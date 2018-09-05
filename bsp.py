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
        self.sliced = []


    def getLineFacingDirection(self, segment):
        '''Given a segment, return the unit vector that describes its facing direction.  This is always a vector that is rotated 90 degrees ccw from this lines direction'''
        d = Vector2D(segment.vec.y, segment.vec.x * -1)
        return d.norm()
        
    def sliceLines(self, segments, index, node=None):
        '''Slice up the line list into smaller segments based on intersections.  This will just make a longer line list called sliced.  Lines can only be sliced within their own groups.  When groups cannot be sliced anymore, then we are done.  Initially, all segments belong in the same group.  When a line gets sliced, then we divide up all the lines into two groups and then call this method on each group.  This method is recursive.'''
        print "index = " + str(index) + " segments = " + str(len(segments))
        frontgroup = []
        backgroup = []
        newlines = []
        line = segments[index]
        #newlines.append(line)
        direction = self.getLineFacingDirection(line)
        for i in range(len(segments)):
            #print line
            #print segments[i]
            t, t2 = line.FindIntersect(segments[i], forward=False)
            if t != None and t2 != 0 and t2 != 1:
                vec = line.p1 + line.vec * t
                line1 = segments[i].p1.toTuple() + vec.toTuple()
                line2 = vec.toTuple() + segments[i].p2.toTuple()
                print t, line1, line2
                newlines.append(Line(*line1, color=segments[i].color))
                newlines.append(Line(*line2, color=segments[i].color))
            else:
                newlines.append(segments[i])
        
        #frontgroup.append(line)
        for i in range(0, len(newlines)):
            v1 = newlines[i].p1 - line.p1
            v2 = newlines[i].p2 - line.p1
            if direction.dot(v1) < 0 or direction.dot(v2) < 0:
                backgroup.append(newlines[i])
            else:
                frontgroup.append(newlines[i])

        print "Dividing line = " + str(line.p1) + " => " + str(line.p2)
        print "Newlines = " + str(len(newlines))
        print "Front = " + str(len(frontgroup))
        print "Behind = " + str(len(backgroup))
        print ""

        if len(backgroup) > 0:
            if node is None:
                self.tree = Node(segment=line)
                node = self.tree
                frontgroup.remove(line)
            else:
                if node.children["Front"] is None:
                    node.children["Front"] = Node(segment=line)
                    node.children["Front"].parent = node
                    node = node.children["Front"]
                    frontgroup.remove(line)
                else:
                    node.children["Back"] = Node(segment=line)
                    node.children["Back"].parent = node
                    node = node.children["Back"]
                    frontgroup.remove(line)


            print "FRONT"
            if len(frontgroup) > 0:
                self.sliceLines(frontgroup, 0, node)
            print "BACK"
            if len(backgroup) > 0:
                self.sliceLines(backgroup, 0, node)
        else:
            if index < len(frontgroup)-1:
                print "Try Next --->"
                self.sliceLines(frontgroup, index+1, node)
            else:
                if node.children["Front"] is None:
                    node.children["Front"] = Node(segment=line)
                    node.children["Front"].parent = node
                    node = node.children["Front"]
                    frontgroup.remove(line)
                    if len(frontgroup) != 0:
                        self.sliceLines(frontgroup, 0, node)
                else:
                    node.children["Back"] = Node(segment=line)
                    node.children["Back"].parent = node
                    node = node.children["Back"]
                    frontgroup.remove(line)
                    if len(frontgroup) != 0:
                        self.sliceLines(frontgroup, 0, node)
                    

    def walk(self, node, level):
        '''Walk through the tree in order to map it out'''
        print ""
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
#bt.sliceLines(walls, 0)
#bt.divideLines(walls)
#print bt.tree
#bt.walk(bt.tree, 0)
#print len(bt.sliced)

#for i in range(len(bt.sliced)):
#    print bt.sliced[i].p1, bt.sliced[i].p2
    
