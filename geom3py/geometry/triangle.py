from .planar_shape import PlanarShape
from .point import Point


class Triangle(PlanarShape):
    """
    Represents a triangle in three-dimensional space.

    A triangle is defined by three corner points A, B, C. From these
    points, the edges, center point, normal vector and associated plane
    are automatically calculated via the parent PlanarShape class.

    Parameters
    ----------
    A : array_like
        First corner point of the triangle.
    B : array_like
        Second corner point of the triangle.
    C : array_like
        Third corner point of the triangle.

    Attributes
    ----------
    A, B, C : Point
        The three corner points of the triangle.
    points : tuple of Point
        The three corner points as a tuple (A, B, C).
    edges : tuple of Line
        The three edges of the triangle.
    center : Point
        The center point of the triangle (arithmetic mean of the corners).
    normal_vector : Vector
        The normal vector of the triangle's plane.
    plane : Plane
        The plane in which the triangle lies.
    """

    def __init__(self, A, B, C):
        """
        Initializes a new triangle from three corner points.

        Parameters
        ----------
        A : array_like
            First corner point of the triangle.
        B : array_like
            Second corner point of the triangle.
        C : array_like
            Third corner point of the triangle.
        """
        PlanarShape.__init__(self, [A, B, C])
        self.A, self.B, self.C = self.points

    def contains_point(self, Q):
        """
        Checks if a given point lies within the triangle.

        Uses the orientation method: a point Q is inside the triangle ABC
        if the signed distances (d1, d2, d3) computed from the cross
        products of each edge with the vector from the corresponding
        vertex to Q all have the same sign (all positive or all negative).

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies within the triangle, otherwise False.

        Notes
        -----
        The method first checks if Q lies in the triangle's plane.
        Points on the edges or corners are considered inside.
        """
        Q = Point(Q)
        if not self.plane.contains_point(Q):
            return False

        else:
            d1 = (self.edges[0].direction_vector.cross(Q - self.A)).dot(self.normal_vector)
            d2 = (self.edges[1].direction_vector.cross(Q - self.B)).dot(self.normal_vector)
            d3 = (self.edges[2].direction_vector.cross(Q - self.C)).dot(self.normal_vector)

            if max([d1, d2, d3]) <= 0 or min([d1, d2, d3]) >= 0:
                return True

            else:
                return False

    # ======================================================================
    # Backward-compatible aliases
    # ======================================================================
    #
    # These methods existed on Triangle before the shared logic was moved to
    # PlanarShape (where they were renamed to the shape-agnostic
    # position_shape / intersection_shape / distance_shape). They are kept
    # here so existing code that calls the old Triangle-specific names keeps
    # working unchanged.

    def position_triangle(self, T2: "Triangle"):
        """
        Alias for `position_shape`, kept for backward compatibility.

        Determines the positional relationship of this triangle to another
        triangle. This is a convenience wrapper that calls the generic
        `position_shape` method from PlanarShape.

        Parameters
        ----------
        T2 : Triangle
            The second triangle whose position relative to this triangle
            is to be determined.

        Returns
        -------
        str
            The positional relationship as a string.
            Possible values: "identical", "parallel", "intersecting",
            "on_edge", "coplanar_intersecting", "edge_intersecting",
            "touching", "coplanar_outside", "outside".

        See Also
        --------
        PlanarShape.position_shape : The generic method this aliases.
        """
        return self.position_shape(T2)

    def intersection_triangle(self, T2: "Triangle"):
        """
        Alias for `intersection_shape`, kept for backward compatibility.

        Calculates the intersection of this triangle with another triangle.
        This is a convenience wrapper that calls the generic
        `intersection_shape` method from PlanarShape.

        Parameters
        ----------
        T2 : Triangle
            The second triangle whose intersection with this triangle
            is to be calculated.

        Returns
        -------
        Triangle or Point or Line or None
            The result of the intersection calculation:
            - Triangle: if the triangles overlap in a coplanar region
            - Point: if they touch at a single point
            - Line: if they intersect along a line
            - None: if there is no intersection

        See Also
        --------
        PlanarShape.intersection_shape : The generic method this aliases.
        """
        return self.intersection_shape(T2)

    def distance_triangle(self, T2: "Triangle"):
        """
        Alias for `distance_shape`, kept for backward compatibility.

        Calculates the distance from this triangle to another triangle.
        This is a convenience wrapper that calls the generic
        `distance_shape` method from PlanarShape.

        Parameters
        ----------
        T2 : Triangle
            The second triangle whose distance to this triangle is to be
            calculated.

        Returns
        -------
        float
            The distance between the two triangles. Returns 0.0 if the
            triangles intersect, touch, or are identical.

        See Also
        --------
        PlanarShape.distance_shape : The generic method this aliases.
        """
        return self.distance_shape(T2)