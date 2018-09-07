import pygame
from pygame.locals import *
from vectors import Vector2D
from math import pi, sin, cos, tan
from line import Line

class RayCaster(object):
    def __init__(self, screenW, screenH):
        self.screenW = screenW
        self.screenH = screenH
        self.color = (255,0,0)
        self.numRays = 600
        self.position = Vector2D(300, 300)
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
        self.radiusSquared = self.radius * self.radius
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
        #self.color = (255,0,0)
        startAngle = self.pointAngle - self.viewAngle
        for i, segment in enumerate(segments):
            #self.CheckCollision(segment)
            for num in range(self.numRays):
                if self.rays[num] is None:
                    angle = startAngle + self.da*num
                    s = self.position + self.GetDirection(angle)
                    ray = Line(self.position.x, self.position.y, 
                               s.x, s.y, segment.color)
                    t, t2 = ray.FindIntersect(segment)
                    
                    if t != None:
                        newray = ray.p1 + (ray.p2-ray.p1)*t
                        self.rays[num] = Line(self.position.x, 
                                              self.position.y,
                                              newray.x, newray.y,
                                              color=ray.color)

    def CheckCollision(self, segments, screen):
        self.color = (255,0,0)
        #print ""
        segment = segments[8]
        for segment in segments:
        #if True:
            #print "P1, P2"
            #print segment.p1, segment.p2
            #print "vec"
            #print segment.vec
            c = self.position - segment.p1
            #print "Position, C"
            #print self.position, c
            proj = segment.vec * (c.dot(segment.vec) / segment.vec.magnitudeSquared())
            #print "Projection onto vec"
            #print proj
            #pygame.draw.line(screen, (200,200,0), segment.p1.toTuple(), proj.toTuple(), 2)
            #print "D vec"
            d = c - proj
            #print d
            collision = False
            #print d.magnitudeSquared(), self.radiusSquared
            if d.magnitudeSquared() <= self.radiusSquared:
                #print "Collision Step 1"
                #print proj.dot(segment.vec)
                if proj.dot(segment.vec) < 0:
                    #print "By P1"
                    #print c.magnitudeSquared(), self.radiusSquared
                    if c.magnitudeSquared() < self.radiusSquared:
                        #print "colliding out of bounds near P1"
                        collision = True
                elif proj.dot(segment.vec) > 0:
                    #print "By P2 or inbounds"
                    #print "vec distance VS proj distance"
                    #print segment.vec.magnitudeSquared(), proj.magnitudeSquared()
                    if segment.vec.magnitudeSquared() < proj.magnitudeSquared():
                        #print "Out of bounds by P2"
                        c2 = self.position - segment.p2
                        #print c2.magnitudeSquared, self.radiusSquared
                        if c2.magnitudeSquared() < self.radiusSquared:
                            #print "colliding out of bounds near P2"
                            collision = True
                    else:
                        print "inbounds"
                        dnew = d.norm() * self.radius
                        test = segment.p1+proj+dnew
                        #print self.position, test
                        self.position = test
                        collision = True
                else:
                    print "I guess the dot product is 0 here"

            if collision:
                self.color = (200,200,0)



    def Render(self, screen):
        pos = Vector2D(int(self.position.x), int(self.position.y))
        pygame.draw.circle(screen, self.color, pos.toTuple(), self.radius)

    def RenderPointDirection(self, screen):
        p2 = self.lookDirection*200 +self.position
        pygame.draw.line(screen, (0,255,255), self.position.toTuple(),
                         p2.toTuple(), 1)

    def RenderRays(self, screen):
        for i in range(len(self.rays)):
            if self.rays[i] is not None:
                self.rays[i].render(screen)

        
