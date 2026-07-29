import math
from .point import Point
from .line import Line
from .vector import Vector
from ..utils.linal_utils import linsys_solve, close

class Plane:
    """
    Represents a plane in three-dimensional space.

    A plane is defined by a point and a normal vector.
    The normal equation is: (x - point) · normal_vector = 0.

    Parameters
    ----------
    point : array_like
        A point on the plane (support vector).
    normal_vector : array_like
        The normal vector of the plane (must not be the zero vector).

    Attributes
    ----------
    point : Vector
        A point on the plane.
    normal_vector : Vector
        The normal vector of the plane.
    """
    # ======================================================================
    # Constructors
    # ======================================================================

    def __init__(self, point, normal_vector):
        """
        Initializes a new plane with point and normal vector.

        Parameters
        ----------
        point : array_like
            A point on the plane.
        normal_vector : array_like
            The normal vector of the plane (must not be the zero vector).

        Raises
        ------
        ValueError
            If the vectors do not have dimension 3 or the
            normal vector is the zero vector.
        """
        self.point = Vector(point)
        self.normal_vector = Vector(normal_vector)
        if len(self.point) != 3 or len(self.normal_vector) != 3:
            raise ValueError("Vectors must have dimension 3")

        if close(self.normal_vector.magnitude(), 0):
            raise ValueError("Normal vector must not be the zero vector")
    
    @classmethod
    def from_parametric(cls, point, v1, v2):
        """
        Creates a plane from parametric form.

        The plane is defined by a point and two direction vectors.
        The normal vector is given by the cross product v1 × v2.

        Parameters
        ----------
        point : array_like
            A point on the plane.
        v1 : array_like
            First direction vector of the plane.
        v2 : array_like
            Second direction vector of the plane.

        Returns
        -------
        Plane
            The plane defined by point and direction vectors.

        Raises
        ------
        ValueError
            If the vectors do not have dimension 3 or the
            direction vectors are linearly dependent.
        """
        v1 = Vector(v1)
        v2 = Vector(v2)

        normal_vector = v1.cross(v2)
        if close(normal_vector.magnitude(), 0):
            raise ValueError("Direction vectors are linearly dependent")
        
        return cls(point, normal_vector)
    
    # ======================================================================
    # Basic Operations
    # ======================================================================

    def contains_vector(self, x_vector):
        """
        Checks if a given vector satisfies the plane equation.

        A vector x lies in the plane if (x - point) · normal_vector = 0.

        Parameters
        ----------
        x_vector : array_like
            The vector (point) to check.

        Returns
        -------
        bool
            True if the vector lies in the plane, otherwise False.
        """
        return close(x_vector.dot(self.normal_vector), 
                         self.point.dot(self.normal_vector))
    
    def contains_point(self, p1):
        """
        Checks if a given point lies in the plane.

        Parameters
        ----------
        p1 : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies in the plane, otherwise False.
        """
        if close(p1.dot(self.normal_vector), 
                     self.point.dot(self.normal_vector)):
            return True
        else:
            return False
        
    # ======================================================================
    # Positional Relationships
    # ======================================================================

    def position_line(self, line):
        """
        Determines the positional relationship of a line to this plane.

        The possible relationships are:
        - "identical": The line lies completely in the plane.
        - "parallel": The line is parallel to the plane but not in it.
        - "intersecting": The line intersects the plane at a point.

        Parameters
        ----------
        line : Line
            The line to check.

        Returns
        -------
        str
            The positional relationship as a string: "identical", "parallel" or "intersecting".
        """
        if close(line.direction_vector.dot(self.normal_vector), 0):
            if self.contains_point(line.point_at(0)):
                return "identical"
            else:
                return "parallel"
        else:
            return "intersecting"
 
    def position_plane(self, E2):
        """
        Determines the positional relationship of another plane to this plane.

        The possible relationships are:
        - "identical": The planes are identical.
        - "parallel": The planes are parallel but not identical.
        - "intersecting": The planes intersect in a line.

        Parameters
        ----------
        E2 : Plane
            The second plane.

        Returns
        -------
        str
            The positional relationship as a string: "identical", "parallel" or "intersecting".
        """
        if close(self.normal_vector.cross(E2.normal_vector).magnitude(), 0):
            if self.contains_point(E2.point):
                return "identical"
            else:
                return "parallel"
        else:
            return "intersecting"
        
    def intercept_points(self):
        """
        Calculates the intercept points of the plane.

        Intercept points are the intersections of the plane with the coordinate axes:
        - S1: Intersection with the x-axis (y = 0, z = 0)
        - S2: Intersection with the y-axis (x = 0, z = 0)
        - S3: Intersection with the z-axis (x = 0, y = 0)

        If the plane is parallel to an axis, None is returned at that position.

        Returns
        -------
        list
            A list with three entries [S1, S2, S3], where each entry
            is a point (list) or None.
        """
        S = []
        for i in range(3):
            d = self.point.dot(self.normal_vector)
            x = [0] * 3
            if not close(self.normal_vector[i], 0):
                x[i] = d / self.normal_vector[i]
            else:
                x[i] = None

            S.append(x)
        return S
    
    # ======================================================================
    # Intersection Calculations
    # ======================================================================

    def intersection_line(self, g: Line):
        """
        Calculates the intersection point of a line with this plane.

        The intersection point is only calculated for intersecting lines.

        Parameters
        ----------
        g : Line
            The line whose intersection with the plane is to be calculated.

        Returns
        -------
        Vector or None
            The intersection point if the line intersects the plane,
            otherwise None.
        """
        if self.position_line(g) == "intersecting":
            numerator = self.normal_vector.dot(self.point - g.support_vector)
            denominator = self.normal_vector.dot(g.direction_vector)
            r = numerator / denominator
            return g.point_at(r)
        else:
            return None
    
    def intersection_plane(self, E2):
        """
        Calculates the intersection line of this plane with another plane.

        The intersection line is only calculated for intersecting planes.

        Parameters
        ----------
        E2 : Plane
            The second plane.

        Returns
        -------
        Line or None
            The intersection line if the planes intersect,
            otherwise None.
        """
        if self.position_plane(E2) == "intersecting":
            d1 = self.normal_vector.dot(self.point)
            d2 = E2.normal_vector.dot(E2.point)
            d = [d1, d2]

            A = [
                list(self.normal_vector),
                list(E2.normal_vector)
            ]

            solution = linsys_solve(A, d)

            if solution is None:
                return None

            support_vector = Vector(*solution)
            direction_vector = self.normal_vector.cross(E2.normal_vector)

            return Line(support_vector, direction_vector)
        
        else:
            return None

    def foot_point(self, P):
        numerator = (P - self.point).dot(self.normal_vector)
        denominator = self.normal_vector.dot(self.normal_vector)
        r = numerator / denominator

        L = P - r * self.normal_vector

        return L
    
    # ======================================================================
    # Distance Calculations
    # ======================================================================

    def distance_point(self, point: Point):
        """
        Calculates the distance from a point to this plane.

        Parameters
        ----------
        point : Point
            The point whose distance to the plane is to be calculated.

        Returns
        -------
        float
            The distance from the point to the plane. If the point lies
            in the plane, 0 is returned.
        """
        if not self.contains_point(point):
            p_array = point
            numerator = abs((p_array - self.point).dot(self.normal_vector))
            denominator = self.normal_vector.magnitude()
            d = numerator / denominator
        
            return d
        else:
            return 0    
    
    def distance_line(self, g: Line):
        """
        Calculates the distance from a line to this plane.

        The distance is only calculated for lines parallel to the plane.

        Parameters
        ----------
        g : Line
            The line whose distance to the plane is to be calculated.

        Returns
        -------
        float or None
            The distance from the line to the plane if it is parallel,
            otherwise None.
        """
        if self.position_line(g) == "parallel":
            q = g.support_vector
            return self.distance_point(q)
        else:
            return None

    def distance_plane(self, E2):
        """
        Calculates the distance from this plane to another plane.

        The distance is only calculated for parallel planes.

        Parameters
        ----------
        E2 : Plane
            The second plane.

        Returns
        -------
        float or None
            The distance between the planes if they are parallel,
            otherwise None.
        """
        if self.position_plane(E2) == "parallel":
            return self.distance_point(E2.point)
        else:
            return None
  
    # ======================================================================
    # Angle Calculations
    # ======================================================================

    def angle_line(self, g: Line, deg=None):
        """
        Calculates the angle between a line and this plane.

        The angle is calculated from the sine of the angle between the
        normal vector of the plane and the direction vector of the line.

        Parameters
        ----------
        g : Line
            The line.
        deg : bool, optional
            If True, the angle is returned in degrees.
            If False or None, the angle is returned in radians.
            Default is None (radians).

        Returns
        -------
        float
            The angle in radians or degrees.
        """
        numerator = abs(self.normal_vector.dot(g.direction_vector))
        denominator = self.normal_vector.magnitude() * g.direction_vector.magnitude()
        result_rad = math.asin(numerator / denominator)

        return math.degrees(result_rad) if deg else result_rad
    
    def angle_plane(self, E2, deg=None):
        """
        Calculates the angle between this plane and another plane.

        The angle is calculated from the dot product of the normal vectors.

        Parameters
        ----------
        E2 : Plane
            The second plane.
        deg : bool, optional
            If True, the angle is returned in degrees.
            If False or None, the angle is returned in radians.
            Default is None (radians).

        Returns
        -------
        float
            The angle in radians or degrees.
        """
        numerator = abs(self.normal_vector.dot(E2.normal_vector))
        denominator = self.normal_vector.magnitude() * E2.normal_vector.magnitude()
        result_rad = math.acos(numerator / denominator)

        return math.degrees(result_rad) if deg else result_rad
    
    # ======================================================================
    # Transformations
    # ======================================================================

    def scale(self, factor):
        return Plane(self.point.scale(factor), self.normal_vector.scale(factor))

    def rotate(self, angle, axis):
        return Plane(self.point.rotate(angle, axis), self.normal_vector.rotate(angle, axis))

    def translate(self, v):
        return Plane(self.point.translate(v), self.normal_vector)

    def reflect_on_point(self, P):
        return Plane(self.point.reflect_on_point(P), self.normal_vector.reflect_on_point(P))

    def reflect_on_line(self, g):
        return Plane(self.point.reflect_on_line(g), self.normal_vector.reflect_on_line(g))

    def reflect_on_plane(self, E):
        return Plane(self.point.reflect_on_plane(E), self.normal_vector.reflect_on_plane(E))

    def __repr__(self):
        """
        Returns a readable string representation of the plane.

        Returns
        -------
        str
            A string representation of the plane.
        """
        return f"Plane(point={self.point}, normal={self.normal_vector})"