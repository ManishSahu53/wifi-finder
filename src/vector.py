# Vector
import numpy as np
import math

from src import point

class Vector(object):
    def __init__(self, point1: point.Point, point2: point.Point, slope=None):
        super().__init__()

        if slope is not None:
            self.vx = point2.x - point1.x
            self.vy = point2.y - point1.y
            self.slope = vy/vx
        else:
            self.slope = m
            self.vx = m*1/(2)**0.5
            self.vy = 1/(2)**0.5
        
        self.magnitude = (self.vx**2 + self.vy **2) ** 0.5

    def GetPerpendicular(self):
        m = -1/self.slope
        return m
