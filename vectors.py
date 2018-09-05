from math import *

class Vector2D(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"

    def toTuple(self):
        return (self.x, self.y)
        
    def toIntTuple(self):
        return (int(self.x), int(self.y))
        
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def norm(self):
        m = self.magnitude()
        return Vector2D(self.x/m, self.y/m)

    def __add__(self, rhs):
        return Vector2D(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector2D(self.x - rhs.x, self.y - rhs.y)

    def __neg__(self, rhs):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
            return False

    def copy(self):
        return Vector2D(self.x, self.y)

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def angle(self, other):
        return acos(self.dot(other) / (self.magntitude() * other.magnitude()))

    def angle_xhat(self):
        '''Angle between this and with xhat'''
        return acos(self.x/self.magnitude())

    def angle_yhat(self):
        '''Angle between this and with yhat'''
        return acos(self.y/self.magnitude())

    def unit(self, angle):
        '''Return a unit vector given an angle'''
        return Vector2D(cos(angle), sin(angle))

    def cross(self, other):
        '''The cross product of 2D vectors is a scalar'''
        return self.x*other.y - other.x*self.y

class Vector3D(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "<"+str(self.x)+", "+str(self.y)+", "+str(self.z)+">"

    def toTuple(self):
        return (self.x, self.y, self.z)
        
    def magnitude(self):
        return sqrt(self.magnitudeSquared())

    def magnitudeSquared(self):
        return self.x**2 + self.y**2 + self.z**2

    def __add__(self, rhs):
        return Vector3D(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def __sub__(self, rhs):
        return Vector3D(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __neg__(self, rhs):
        return Vector3D(-self.x, -self.y, -self.z)

    def __mul__(self, scalar):
        return Vector3D(scalar * self.x, scalar * self.y)

    def __div__(self, scalar):
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
            return False

    def copy(self):
        return Vector3D(self.x, self.y, self.z)

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def angle(self, other):
        return acos(self.dot(other) / (self.magntitude() * other.magnitude()))

    def angle_xhat(self):
        '''Angle between this and with xhat'''
        return acos(self.x/self.magnitude())

    def angle_yhat(self):
        '''Angle between this and with yhat'''
        return acos(self.y/self.magnitude())

    def angle_zhat(self):
        '''Angle between this and with zhat'''
        return acos(self.z/self.magnitude())

