import math 
from .point import Point
from .box import Box
from .line import Line
from .plane import Plane
from .vector import Vector
from ..utils.linal_utils import close

class Sphere:

    def __init__(self, radius, M):
        self.radius = radius
        self.center = Point(M)
        self.diameter = radius * 2
        self.circumference = 2 * math.pi * radius

        self.containing_cube = self._compute_containing_cube
        self.volume = self._compute_volume
        self.surface = self._compute_surface    

    # ======================================================================
    # Private compute methods
    # ======================================================================

    def _compute_volume(self):
        return (4/3) * math.pi * (self.radius) ** 3

    def _compute_surface(self):
        return 4 * math.pi * self.radius**2

    def _compute_containing_cube(self):
        r_vector = Vector(self.radius, self.radius, self.radius)
        p_min = self.center - r_vector
        p_max = self.center + r_vector

        box = Box(p_min, p_max)
    # ======================================================================
    # Basic Operations
    # ======================================================================

    def contains_point(self, Q):
        if self.conatining_cube.contains_point(Q):
            mq = Q - self.center

            if close(mq.magnitude(), self.radius):
                return True

        return False 

    def point_on_surface(self, Q):
        if close(Q - self.center, 0):
            return True

        return False

    # ======================================================================
    # Positional Relationships
    # ======================================================================

    def position_point(self, Q):
        if self.contains_point(Q) and not self.point_on_surface(Q):
            return "inside"

        elif self.point_on_surface(Q):
            return "on_surface"

        return "outside"

    def position_line(self, g: Line):
        d = g.distance_point(self.center)

        if d < self.radius:
            return "intersecting"

        elif close(d, self.radius):
            return "touching"

        return "outside"

    def position_plane(self, E: Plane):
        d = E.distance_point(self.center)

        if d < self.radius:
            return "intersecting"

        elif close(d, self.radius):
            return "touching"

        return "outside"

    def position_sphere(self, S2):
        if self.center == S2.center and self.radius == S2.radius:
            return "identical"

        d = (S2.center - self.center).magnitude()
        if self.center == S2.center:
            return "concentric"
        
        if d + S2.radius < self.radius:
            return "contains"
        
        elif d + self.radius < S2.radius:
            return "is_contained"

        elif close(self.radius + S2.radius, d) or close(abs(self.radius - S2.radius), d):
            return "touching"

        elif self.radius + S2.radius > d:
            return "intersecting"

        elif self.radius + S2.radius < d:
            return "outside"

    # ======================================================================
    # Intersection Calculations
    # ======================================================================

    def intersection_line(self, g: Line):
        position = self.position_line(g)

        if position == "outside":
            return None

        elif position == "touching":
            return g.distance_point(self.center)

        elif position == "intersecting":
            L = g.foot_point(self.center)
            d = L - self.center
            h = math.sqrt(self.radius**2 - d.magnitude()**2)
            P1 = L + g.direction_vector.normalize() * h
            P2 = L -g.direction_vector.normalize() * h

            return [P1, P2]
        