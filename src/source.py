# Line
import numpy as np
import math

from src import point

class Source(point.Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.k = 100