import pygame
from pygame.locals import *
from vectors import Vector2D
from math import pi, sin, cos, tan
from line import Line

class RayCaster(object):
    def __init__(self, screenW, screenH):
        self.screenW = screenW
        self.screenH = screenH
        self.numRays = 600
        self.position = Vector2D(440, 200)
        self.pointAngle = pi/2
        self.viewAngle= pi/6.0
        self.da = 2*self.viewAngle / self.numRays
        self.lookDirection = self.GetDirection(self.pointAngle)
        self.moveDirection = Vector2D()
        self.speed = 200
        self.rotate_speed = 2
        self.columnHeight = 100.0
        self.columnWidth = screenW / self.numRays
        self.hRatio = self.columnHeight*screenW*tan(self.viewAngle)
        self.radius = 15
        self.rays = [None]*self.numRays
        self.wallType = [] #horizontal 'h' or vertical 'v'
        self.numRaysCast = 0

    def GetDirection(self, angle):
        '''Get Unit Vector pointing in direction defined by angle'''
        return Vector2D(cos(angle), sin(angle))

    def Move(self, dt):
        key_pressed = pygame.key.get_pressed()
        self.moveDirection = Vector2D()
        if key_pressed[K_LEFT]:
            self.pointAngle -= self.rotate_speed*dt
            self.pointAngle %= 2*pi
            if self.pointAngle == 0.0: self.pointAngle = 2*pi
        elif key_pressed[K_RIGHT]:
            self.pointAngle += self.rotate_speed*dt
            self.pointAngle %= 2*pi
            if self.pointAngle == 0.0: self.pointAngle = 2*pi
        if (key_pressed[K_w] or key_pressed[K_UP]):
            self.moveDirection = self.GetDirection(self.pointAngle)
        elif (key_pressed[K_s] or key_pressed[K_DOWN]):
            self.moveDirection = self.GetDirection(self.pointAngle)*-1
        if key_pressed[K_a]:
            self.moveDirection = self.GetDirection(self.pointAngle-pi/2)
        elif key_pressed[K_d]:
            self.moveDirection = self.GetDirection(self.pointAngle+pi/2)
        self.lookDirection = self.GetDirection(self.pointAngle)
        self.position += self.moveDirection*self.speed*dt

    def ResetRays(self):
        self.rays = [None]*self.numRays

    def CastRays(self, segments):
        '''Apply line intersection algorithm here'''
        startAngle = self.pointAngle - self.viewAngle
        for i, segment in enumerate(segments):
            for num in range(self.numRays):
                if self.rays[num] is None:
                    angle = startAngle + self.da*num
                    s = self.position + self.GetDirection(angle)
                    ray = Line(self.position.x, self.position.y, 
                               s.x, s.y, segment.color)
                    t = ray.FindIntersect(segment)
                    
                    if t != None:
                        newray = ray.p1 + (ray.p2-ray.p1)*t
                        self.rays[num] = Line(self.position.x, 
                                              self.position.y,
                                              newray.x, newray.y,
                                              color=ray.color)

    def Render(self, screen):
        pos = Vector2D(int(self.position.x), int(self.position.y))
        pygame.draw.circle(screen, (255,0,0), pos.toTuple(), self.radius)

    def RenderPointDirection(self, screen):
        p2 = self.lookDirection*200 +self.position
        pygame.draw.line(screen, (0,255,255), self.position.toTuple(),
                         p2.toTuple(), 1)

    def RenderRays(self, screen):
        for i in range(len(self.rays)):
            if self.rays[i] is not None:
                self.rays[i].render(screen)

        
