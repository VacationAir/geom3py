import math 
from .vector import Vector
from ..utils.linal_utils import linsys_solve, close

class Line:
    """
    Represents a line in three-dimensional space.

    A line is defined by a support vector and a direction vector.
    The parametric equation is: g: x = support + r * direction.

    Parameters
    ----------
    support_vector : array_like
        The support vector (position vector of a point on the line).
    direction_vector : array_like
        The direction vector of the line (must not be the zero vector).

    Attributes
    ----------
    support_vector : Vector
        The support vector of the line.
    direction_vector : Vector
        The direction vector of the line.
    """
    # ======================================================================
    # Constructor
    # ======================================================================

    def __init__(self, support_vector, direction_vector):
        """
        Initializes a new line with support and direction vectors.

        Parameters
        ----------
        support_vector : array_like
            The support vector (position vector of a point on the line).
        direction_vector : array_like
            The direction vector of the line (must not be the zero vector).

        Raises
        ------
        ValueError
            If the vectors do not have dimension 3 or the
            direction vector is the zero vector.
        """
        self.support_vector = Vector(support_vector)
        self.direction_vector = Vector(direction_vector)

    @classmethod
    def from_points(cls, p1, p2):
        """
        Creates a line from two given points.

        The line passes through both points. The direction vector
        is given by the difference p2 - p1.

        Parameters
        ----------
        p1 : array_like
            Coordinates of the first point.
        p2 : array_like
            Coordinates of the second point.

        Returns
        -------
        Line
            The line passing through both points.

        Raises
        ------
        ValueError
            If the points do not have dimension 3 or are identical.
        """
        p1 = Vector(p1)
        p2 = Vector(p2)
        return cls(p1, p2 - p1)
    
    # ======================================================================
    # Basic Operations
    # ======================================================================

    def point_at(self, r):
        """
        Calculates the point on the line for a given parameter r.

        The parametric equation is: x(r) = support + r * direction.

        Parameters
        ----------
        r : float
            The parameter value.

        Returns
        -------
        Vector
            The point on the line.
        """
        return self.support_vector + r * self.direction_vector

    def _calculate_quotient(self, point):
        """
        Calculates the parameter r for a given point.

        This method is used internally to check if a point
        lies on the line.

        Parameters
        ----------
        point : array_like
            The point to check.

        Returns
        -------
        float or None
            The parameter r if the point lies on the line,
            otherwise None.
        """
        point = Vector(point)
        solutions_r = []

        for i in range(3):
            if close(self.direction_vector[i], 0):
                if not close(point[i], self.support_vector[i]):
                    return None
            else:
                r = (point[i] - self.support_vector[i]) / self.direction_vector[i]
                solutions_r.append(r)

        if len(solutions_r) == 0:
            return 0.0

        if close(solutions_r, solutions_r[0]):
            return solutions_r[0]

        return None

    def contains_point(self, point):
        """
        Checks if a given point lies on the line.

        Parameters
        ----------
        point : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies on the line, otherwise False.
        """
        if self._calculate_quotient(point) != None:
            return True
        else:
            return False
        
    def foot_point(self, q):
        """
        Calculates the foot point of a point on the line.
        """
        aq = q - self.support_vector
        r = aq.dot(self.direction_vector) / self.direction_vector.dot(self.direction_vector)
        
        return self.point_at(r)
    
    # ======================================================================
    # Positional Relationships
    # ======================================================================
    
    def position_line(self, g2):
        """
        Determines the positional relationship of this line to another line.

        The possible relationships are:
        - "identical": The lines are identical.
        - "parallel": The lines are parallel but not identical.
        - "intersecting": The lines intersect at a point.
        - "skew": The lines are skew (not parallel, not intersecting).

        Parameters
        ----------
        g2 : Line
            The second line.

        Returns
        -------
        str
            The positional relationship as a string: "identical", "parallel",
            "intersecting" or "skew".
        """
        # First check collinear or not
        collinear = close(self.direction_vector.cross(g2.direction_vector), 0)
        if collinear:
            if self.contains_point(g2.support_vector):
                return "identical"
            else:
                return "parallel"
        else:
            pq = g2.support_vector - self.support_vector
            n = self.direction_vector.cross(g2.direction_vector)
            distance = abs(pq.dot(n) / n.magnitude())
            if close(distance, 0):
                return "intersecting"
            else:
                return "skew"
            
    # ======================================================================
    # Intersection Calculations
    # ======================================================================

    def intersection_line(self, g2: "Line"):
        """
        Calculates the intersection point of this line with another line.

        The intersection point is only calculated for intersecting lines.

        Parameters
        ----------
        g2 : Line
            The second line.

        Returns
        -------
        Vector or None
            The intersection point if the lines intersect,
            otherwise None.
        """
        if self.position_line(g2) == "intersecting":
            A = [
                [self.direction_vector[0], -g2.direction_vector[0]],
                [self.direction_vector[1], -g2.direction_vector[1]],
                [self.direction_vector[2], -g2.direction_vector[2]]
            ]

            b = g2.support_vector - self.support_vector

            solution = linsys_solve(A, b)

            if solution is None:
                return None
            
            return self.point_at(solution[0])
        
        else:
            return None
        
    def intercept_points(self):
        """
        Calculates the intercept points of the line.

        Intercept points are the intersections of the line with the coordinate planes:
        - S1: Intersection with the x-axis (y = 0, z = 0)
        - S2: Intersection with the y-axis (x = 0, z = 0)
        - S3: Intersection with the z-axis (x = 0, y = 0)

        If the line is parallel to an axis, None is returned at that position.

        Returns
        -------
        list
            A list with three entries [S1, S2, S3], where each entry
            is a point (Vector) or None.
        """
        S = []
        for i in range(3):
            if self.direction_vector[i] != 0:
                r = -self.support_vector[i] / self.direction_vector[i]
                S.append(self.point_at(r))
            else:
                S.append(None)
        return S

    # ======================================================================
    # Distance Calculations
    # ======================================================================

    def distance_point(self, q):
        """
        Calculates the distance from a point to this line.

        The distance is calculated using the formula d = |(q - support) x direction| / |direction|.

        Parameters
        ----------
        q : array_like
            The point whose distance to the line is to be calculated.

        Returns
        -------
        float
            The distance from the point to the line.
        """
        vector_pq = q - self.support_vector
        cross_product = vector_pq.cross(self.direction_vector)
        numerator = cross_product.magnitude()
        denominator = self.direction_vector.magnitude()
        return numerator / denominator

    def distance_line(self, g2):
        """
        Calculates the distance between this line and another line.

        The distance is only calculated for skew lines.
        For intersecting, parallel or identical lines, None is returned.

        Parameters
        ----------
        g2 : Line
            The second line.

        Returns
        -------
        float or None
            The distance between the lines if they are skew,
            otherwise None.
        """
        if self.position_line(g2) == "skew":
            vector_pq = g2.support_vector - self.support_vector

            normal_vector = self.direction_vector.cross(g2.direction_vector)
            dot_product = vector_pq.dot(normal_vector)

            numerator = abs(dot_product)
            denominator = normal_vector.magnitude()
            distance = numerator / denominator

            return distance
        else:
            return None

    # ======================================================================
    # Angle Calculations
    # ======================================================================
    
    def angle_lines(self, g2, deg=None):
        """
        Calculates the angle between this line and another line.

        The angle is calculated from the dot product of the direction vectors.

        Parameters
        ----------
        g2 : Line
            The second line.
        deg : bool, optional
            If True, the angle is returned in degrees.
            If False or None, the angle is returned in radians.
            Default is None (radians).

        Returns
        -------
        float
            The angle between the lines in radians or degrees.
        """
        numerator = abs(self.direction_vector.dot(g2.direction_vector))
        denominator = self.direction_vector.magnitude() * g2.direction_vector.magnitude()
        result_in_radians = math.acos(numerator / denominator)
        if deg:
            return math.degrees(result_in_radians)
        return result_in_radians

    # ======================================================================
    # Transformations
    # ======================================================================

    def scale(self, factor):
        return Line(self.support_vector.scale(factor), self.direction_vector.scale(factor))

    def rotate(self, angle, axis):
        return Line(self.support_vector.rotate(angle, axis), self.direction_vector.rotate(angle, axis))

    def translate(self, v):
        return Line(self.support_vector.translate(v), self.direction_vector)

    def reflect_on_point(self, P):
        return Line(self.support_vector.reflect_on_point(P), self.direction_vector.reflect_on_point(P))

    def reflect_on_line(self, g):
        return Line(self.support_vector.reflect_on_line(g), self.direction_vector.reflect_on_line(g))

    def reflect_on_plane(self, E):
        return Line(self.support_vector.reflect_on_plane(E), self.direction_vector.reflect_on_plane(E))
    
    def __repr__(self):
        """
        Returns a readable string representation of the line.

        Returns
        -------
        str
            A string representation of the line.
        """
        return f"Line(support={self.support_vector}, direction={self.direction_vector})"