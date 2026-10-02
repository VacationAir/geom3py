import math 
from .point import Point
from .box import Box
from .vector import Vector
from ..utils.linal_utils import close
class Sphere:

    def __init__(self, radius, M: Point):
        self.radius = radius
        self.center = M
        self.diameter = radius * 2

        self.volume = self._compute_volume
        self.surface = self._compute_surface    

    # ======================================================================
    # Basic Operations
    # ======================================================================

    def _compute_volume(self):
        return (4/3) * math.pi * (self.radius) ** 3

    def _compute_surface(self):
        return 4 * math.pi * self.radius**2

    def contains_point(self, Q):
        r_vector = Vector(self.radius, self.radius, self.radius)
        p_min = self.center - r_vector
        p_max = self.center + r_vector

        box = Box(p_min, p_max)

        if box.contains_point(Q):
            mq = Q - self.center

            if close(mq.magnitude(), self.radius):
                return True

        return False 
