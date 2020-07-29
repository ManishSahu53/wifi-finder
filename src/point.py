# Points
import numpy as np
import math

# from src import vector
# from src import line


class Point:
    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z
        self.path = []
        self._intensity = None

    @staticmethod
    def Distance(point1, point2):
        x = point1.x - point2.x
        y = point1.y - point2.y
        z = point1.z - point2.z

        dist = (x ** 2 + y ** 2 + z ** 2)**0.5
        return dist

    def Intensity(self, source):
        sx = source.x
        sy = source.y
        sz = source.z

        intensity = source.k / ((sx - self.x) ** 2 +
                                (sy - self.y)**2 + (sz - self.z)**2 + 1)
        self._intensity = intensity
        print('Intensity at x: {}, y: {}, z: {}, is I: {}'.format(
            self.x, self.y, self.z, self._intensity))
        return self._intensity

    def Move(self, delta_x, delta_y, delta_z):
        self.path = [self.x, self.y, self.z]

        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

        print('Moved to x: {}, y: {}, z: {}'.format(self.x, self.y, self.z))

    def Goto(self, x, y, z):
        self.path = [self.x, self.y, self.z]

        self.x = x
        self.y = y
        self.z = z
        print('Moved to x: {}, y: {}, z: {}'.format(self.x, self.y, self.z))

    def GetVector(self, x, y, z):
        vx = x - self.x
        vy = y - self.y
        vz = z - self.z
        return vx, vy, vz

    def MoveAlongLine_xy(self, line1, distance):
        x = self.x + distance * (1/(1 + line1.slope_xy ** 2)) ** 0.5
        y = self.y + distance * \
            (line1.slope_xy / (1 + line1.slope_xy ** 2) ** 0.5)
        z = self.z
        self.Goto(x, y, z)

    def MoveAlongLine_yz(self, line1, distance):
        x = self.x
        y = self.y + distance * (1/(1 + line1.slope_yz ** 2)) ** 0.5
        z = self.z + distance * \
            (line1.slope_yz / (1 + line1.slope_yz ** 2) ** 0.5)

        self.Goto(x, y, z)
    
    # def GetMaximumIntensityPoint(self, line1):
