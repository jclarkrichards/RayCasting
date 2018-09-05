import pygame
from vectors import Vector2D
from math import cos
from line import Line
from maps import mapPrecooked, mapRaw
from bsp import BinaryTree


class Map(object):
    def __init__(self):
        #self.walls = mapPrecooked()
        self.walls = mapRaw()
        bsp = BinaryTree(self.walls)
        #bsp.manual()
        bsp.divideLines(self.walls)
        bsp.walk(bsp.tree, 0)
        self.tree = bsp.tree
        self.startNode = None

    def ClearTree(self, node):
        '''Turn all of trees nodes to unvisited'''
        node.visited = False
        if node.children["Front"]:
            self.ClearTree(node.children["Front"])
        if node.children["Back"]:
            self.ClearTree(node.children["Back"])
        
    def TraverseTree(self, player, node):
        '''Walk back through the tree recursively'''
        #print node
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
        ''''''
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
        '''If the node has a Front or Back child or is a Leaf Node'''
        if node.children[child1] is not None:
            self.CheckChildren(player, node, child1, child2)
        elif node.children[child2] is not None:
            self.CheckChildren(player, node, child2, child1)
        else:
            player.CastRays(node.segments)
            self.TraverseTree(player, node.parent)
        

        
    def Render3D(self, screen, player):
        '''Draw the walls as columns'''
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

    def Render2D(self,screen):
        '''Draw the walls as lines'''
        for wall in self.walls:
            wall.render(screen)

