# Line
import numpy as np
import math

from src import point


class Line(object):
    def __init__(self, point1: point.Point, point2: point.Point=None, slope=None):
        # super().__init__(point1, point2, slope)
        if slope is None:
            assert point2 is not None
            self.slope = (point2.y - point1.y)/(point2.x - point1.x)
            self.intercept = (point2.x * point1.y - point2.y * point1.x)/(point2.x - point1.x)

        else:
            assert slope is not None
            self.slope = slope
            self.intercept = point1.y  - self.slope * point1.x
        
    def  GetPerpendicularFromPoint(self, point1: point.Point):
        m = -1/self.slope 
        return Line(point1=point1, slope=m)

    @staticmethod
    def IntersectLine(line1, line2):
        y = (line1.slope * line2.intercept - line1.intercept * line2.slope)/(line1.slope - line2.slope)
        x = (line2.intercept - line1.intercept) / (line1.slope - line2.slope)

        return point.Point(x=x, y=y)
    
    def PointonLine(self, point1: point.Point):
        return point1.y - self.slope * point1.x  == 0

    @staticmethod
    def Intensity(source: point.Point, point1: point.Point):
        sx = souce.x
        sy = souce.y

        intensity = source.k/ ((sx - point1.x) **2 + (sy - point1.y)**2 + 1)
        return intensity


