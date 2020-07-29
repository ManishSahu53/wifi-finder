# Points
import numpy as np
import math

# from src import vector
# from src import line


class Point:
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.path = []
        self._intensity = None

    @staticmethod
    def Distance(point1, point2):
        x = point1.x - point2.x
        y = point1.y - point2.y
        dist = (x **2 + y **2)**0.5
        return dist


    def Intensity(self, source):
        sx = source.x
        sy = source.y

        intensity = source.k/ ((sx - self.x) **2 + (sy - self.y)**2 + 1)
        self._intensity = intensity
        print('Intensity at x: {}, y: {} is I: {}'.format(self.x, self.y, self._intensity))
        return self._intensity

    def Move(self, delta_x, delta_y):
        self.path = [self.x, self.y]

        self.x += delta_x
        self.y += delta_y
        print('Moved to x: {}, y: {}'.format(self.x, self.y))

    
    def Goto(self, x, y):
        self.path = [self.x, self.y]

        self.x = x
        self.y = y
        print('Moved to x: {}, y: {}'.format(self.x, self.y))
    

    def GetVector(self, x, y):
        vx = x - self.x
        vy = y - self.y
        return vx, vy

    def MoveAlongLine(self, line1, distance):
        x = self.x + distance * (1/(1 + line1.slope **2 )) ** 0.5
        y = self.y + distance * (line1.slope /(1 + line1.slope ** 2) **0.5)
        
        self.Goto(x, y)
        

    # def GetMaximumIntensityPoint(self, line1):
