import pygame
from vectors import Vector2D

class Line(object):
    '''Define a line by giving it 4 x and y points.  
    The color of the line will define the color of the wall drawn in 3D'''
    def __init__(self, x1, y1, x2, y2, color=(255,255,255)):
        self.p1 = Vector2D(x1, y1)
        self.p2 = Vector2D(x2, y2)
        self.vec = self.p2 - self.p1
        #print self.vec
        self.color = color
        self.thickness = 1

    def FindIntersect(self, other, forward=True):
        '''Given another line, find the point of intersection
        If no intersection, then return None (lines are parallel)
        forward only looks in one direction, setting to false would 
        check in both directions of line direction'''
        m1 = self.p1.cross(self.p2)
        m2 = self.p2.cross(other.p1)
        m3 = other.p1.cross(self.p1)
        m4 = other.p2.cross(self.p2)
        m5 = self.p1.cross(other.p2)
        m6 = other.p1.cross(other.p2)
        m = m2+m3+m4+m5
        if m != 0:
            tw = (m1+m2+m3) / m
            tr = (m6-m5-m3) / -m
            if forward:
                if tr >= 0 and 0 <= tw <= 1:
                    return tr
            else:
                if 0 <= tw <=1:
                    return tr
        return None
    
    def render(self, screen):
        pygame.draw.line(screen, self.color, self.p1.toTuple(),
                         self.p2.toTuple(), self.thickness)
