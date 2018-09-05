import pygame
from vectors import Vector2D
from math import cos
from line import Line

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
        print self.position, d
        

class Map(object):
    def __init__(self, tree=None):
        self.tree = tree
        self.color = (255,255,255)
        self.color1 = (200,0,0)
        self.color2 = (100,20,150)
        if self.tree is None:
            self.walls = [Line(160,120,240,120, color=self.color1),
                          Line(240,120,240,200, color=self.color2),
                          Line(240,200,160,200, color=self.color1),
                          Line(160,200,160,120, color=self.color2),
                          Line(560,40,40,40, color=self.color1),
                          Line(560,120,560, 40, color=self.color2),
                          Line(560,360,560,120, color=self.color2),
                          Line(240,360,560,360, color=self.color1),
                          Line(40,360,240,360, color=self.color1),
                          Line(40,200,40,360, color=self.color2),
                          Line(40,120,40,200, color=self.color2),
                          Line(40,40,40,120, color=self.color2)]

            self.makeTreeManual()
        self.startNode = None

    def ClearTree(self, node):
        node.visited = False
        if node.children["Front"]:
            self.ClearTree(node.children["Front"])
        if node.children["Back"]:
            self.ClearTree(node.children["Back"])
        
    def TraverseTree(self, player, node):
        '''Walk back through the tree'''
        node.visited = True
        pos = player.position - node.position
        pvalue = pos.dot(node.direction)
        if None in player.rays:
            if pvalue >= 0:
                self.HasChildren(player, node, "Front", "Back")
            else:
                self.HasChildren(player, node, "Back", "Front")
        else:
            self.ClearTree(self.tree)

    def CheckChildren(self, player, node, child1, child2):
        if not node.children[child1].visited:
            self.TraverseTree(player, node.children[child1])
        else:
            player.CastRays(node.segments)
            if node.children[child2] is not None:
                if not node.children[child2].visited:
                    self.TraverseTree(player, node.children[child2])
                else: #already visited back node
                    self.TraverseTree(player, node.parent)
            else: #No back nodes
                self.TraverseTree(player, node.parent)

    def HasChildren(self, player, node, child1, child2):
        if node.children[child1] is not None:
            self.CheckChildren(player, node, child1, child2)
        elif node.children[child2] is not None:
            self.CheckChildren(player, node, child2, child1)
        else:
            player.CastRays(node.segments)
            self.TraverseTree(player, node.parent)
        

    def makeTreeManual(self):
        self.tree = Node("root", self.walls[0])
        nodeB = Node("B", self.walls[1])
        nodeC = Node("C", self.walls[2])
        nodeD = Node("D", self.walls[3])
        nodeE = Node("E", self.walls[4])
        nodeF1 = Node("F1", self.walls[5])
        nodeF2 = Node("F2", self.walls[6])
        nodeG2 = Node("G2", self.walls[7])
        nodeG1 = Node("G1", self.walls[8])
        nodeH22 = Node("H22", self.walls[9])
        nodeH21 = Node("H21", self.walls[10])
        nodeH1 = Node("H1", self.walls[11])
        
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
        
    def Render3D(self, screen, player):
        for i in range(len(player.rays)):
            if player.rays[i] is not None:
                v = player.rays[i].vec
                w = player.lookDirection
                r = w * (v.dot(w) / w.magnitudeSquared())
                distanceAdjust = r.magnitude()
                #distanceAdjust = v.magnitude()
                columnH = player.hRatio / distanceAdjust
                columnPos = Vector2D(i*player.columnWidth, (player.screenH - columnH)/2)
                pygame.draw.rect(screen, player.rays[i].color, columnPos.toTuple()+(player.columnWidth, columnH))

    def renderWalls(self,screen):
        for wall in self.walls:
            wall.render(screen)

