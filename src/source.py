# Line
import numpy as np
import math

from src import point

class Source(point.Point):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z
        self.k = 100