# Line
import numpy as np
import math

from src import point


class Line(object):
    def __init__(self, point1: point.Point, point2: point.Point=None, slope_xy=None, slope_yz=None, axis=2):
        # super().__init__(point1, point2, slope_xy)
        if slope_xy is None and axis ==2:
            assert point2 is not None
            self.slope_yz = 0
            self.intercept_yz = 0
            self.slope_xy = (point2.y - point1.y)/(point2.x - point1.x)
            self.intercept_xy = (point2.x * point1.y - point2.y * point1.x)/(point2.x - point1.x)

        elif slope_xy is not None and axis == 2:
            assert slope_xy is not None
            self.slope_xy = slope_xy
            self.slope_yz = 0
            self.intercept_yz = 0

            self.intercept_xy = point1.y  - self.slope_xy * point1.x

        if slope_yz is None and axis ==3:
            assert point2 is not None
            self.slope_xy = 0
            self.intercept_xy = 0
            self.slope_yz = (point2.z - point1.z)/(point2.y - point1.y)
            self.intercept_yz = (point2.y * point1.z - point2.z * point1.y)/(point2.y - point1.y)

        elif slope_yz is not None and axis == 3:
            assert slope_yz is not None
            self.slope_xy = 0
            self.intercept_xy = 0
            self.slope_yz = slope_yz
            self.intercept_yz = point1.z  - self.slope_yz * point1.y
        
    def  GetPerpendicularFromPoint(self, point1: point.Point, axis=2):
        
        assert axis == 2 or axis ==3, "only 2D and 3D allowed, so 2 and 3"
        # If 3D
        if axis == 3:
            m_yz = -1/self.slope_yz 
            m_xy = self.slope_xy
        
        # If 2D
        if axis == 2:
            m_xy = -1/self.slope_xy 
            m_yz = self.slope_yz



        return Line(point1=point1, slope_xy=m_xy, slope_yz=m_yz, axis=axis)

    @staticmethod
    def IntersectLine(line1, line2, axis):
        assert axis == 2 or axis ==3, "only 2D and 3D allowed, so 2 and 3"

        if axis == 2:
            y = (line1.slope_xy * line2.intercept_xy - line1.intercept_xy * line2.slope_xy)/(line1.slope_xy - line2.slope_xy)
            x = (line2.intercept_xy - line1.intercept_xy) / (line1.slope_xy - line2.slope_xy)
            z = 0
        if axis == 3:
            z = (line1.slope_yz * line2.intercept_yz - line1.intercept_yz * line2.slope_yz)/(line1.slope_yz - line2.slope_yz)
            y = (line2.intercept_yz - line1.intercept_yz) / (line1.slope_yz - line2.slope_yz)
            x = 0

        return point.Point(x=x, y=y, z=z)
    
    def PointonLine(self, point1: point.Point):
        return point1.y - self.slope_xy * point1.x  == 0

    @staticmethod
    def Intensity(source: point.Point, point1: point.Point):
        sx = source.x
        sy = source.y
        sz = source.z
        intensity = source.k/ ((sx - point1.x) **2 + (sy - point1.y)**2 + (sz - point1.z)**2 + 1)
        return intensity


