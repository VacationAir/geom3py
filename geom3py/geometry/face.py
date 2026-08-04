from .point import Point
from .line import Line
from .planar_shape import PlanarShape

class Face(PlanarShape):
    """
    Represents a planar face (quadrilateral) in three-dimensional space.

    A face is defined by four corner points X1, X2, X3, X4, which
    define the edges of the face in this order. From the
    corner points, the four edges, the two diagonals, the center point,
    the normal vector and the associated plane are automatically calculated.

    Parameters
    ----------
    X1 : array_like
        First corner point of the face.
    X2 : array_like
        Second corner point of the face.
    X3 : array_like
        Third corner point of the face.
    X4 : array_like
        Fourth corner point of the face.

    Attributes
    ----------
    X1, X2, X3, X4 : Point
        The four corner points of the face.
    points : tuple of Point
        The four corner points as a tuple (X1, X2, X3, X4).
    edges : tuple of Line
        All four edges of the face in order.
    d1 : Line
        The diagonal from X4 to X2.
    d2 : Line
        The diagonal from X1 to X3.
    center : Point
        The center point of the face (arithmetic mean of the four corner points).
    normal_vector : Vector
        The normal vector of the face plane.
    plane : Plane
        The plane in which the face lies.
    """
    # ======================================================================
    # Constructors
    # ======================================================================

    def __init__(self, X1, X2, X3, X4):
        """
        Initializes a new face from four corner points.

        Parameters
        ----------
        X1 : array_like
            First corner point of the face.
        X2 : array_like
            Second corner point of the face.
        X3 : array_like
            Third corner point of the face.
        X4 : array_like
            Fourth corner point of the face.
        """
        super().__init__([X1, X2, X3, X4])

        self.X1, self.X2, self.X3, self.X4 = self.points

        self.d1 = Line.from_points(self.X4, self.X2)
        self.d2 = Line.from_points(self.X1, self.X3)

    # ======================================================================
    # Basic Operations
    # ======================================================================

    def contains_point(self, Q):
        """
        Checks if a given point lies within the face.

        First, it is checked whether the point lies in the plane of the
        face and whether it lies on an edge or corner.
        Otherwise, the foot points on the four edges are used to determine
        whether the point lies within the area bounded by the edges.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies within the face, otherwise False.
        """
        Q = Point(Q)

        if not self.plane.contains_point(Q):
            return False

        if self.point_on_edge(Q):
            return True

        edge_X1_X2, edge_X2_X3, edge_X3_X4, edge_X4_X1 = self.edges

        L = edge_X1_X2.foot_point(Q)
        LX2_X3 = edge_X2_X3.foot_point(Q)
        LX3_X4 = edge_X3_X4.foot_point(Q)
        LX4_X1 = edge_X4_X1.foot_point(Q)

        v1 = Q - L
        v2 = LX2_X3 - Q
        v3 = LX3_X4 - Q
        v4 = LX4_X1 - Q

        L_list = [L, LX2_X3, LX3_X4, LX4_X1]
        G_list = [edge_X1_X2, edge_X2_X3, edge_X3_X4, edge_X4_X1]

        if v1.dot(v2) >= 0 or v1.dot(v3) >= 0 or v1.dot(v4) >= 0:
            for i in range(len(L_list)):
                r = G_list[i]._calculate_quotient(L_list[i])
                if r is None or not (0 <= r <= 1):
                    return False

            return True

        else:
            return False

    # ======================================================================
    # Backward-compatible aliases
    # ======================================================================
    #
    # These methods existed on Face before the shared logic was moved to
    # PlanarShape (where they were renamed to the shape-agnostic
    # position_shape / intersection_shape / distance_shape). They are kept
    # here so existing code that calls the old Face-specific names keeps
    # working unchanged.

    def position_face(self, F2: "Face"):
        """
        Alias for `position_shape`, kept for backward compatibility.

        Parameters
        ----------
        F2 : Face
            The second face whose position relative to this face is to be determined.

        Returns
        -------
        str
            The positional relationship as a string. See `position_shape`.
        """
        return self.position_shape(F2)

    def intersection_face(self, F2: "Face"):
        """
        Alias for `intersection_shape`, kept for backward compatibility.

        Parameters
        ----------
        F2 : Face
            The second face whose intersection with this face is to be calculated.

        Returns
        -------
        Face or Point or Line or None
            The result of the intersection calculation. See `intersection_shape`.
        """
        return self.intersection_shape(F2)

    def distance_face(self, F2: "Face"):
        """
        Alias for `distance_shape`, kept for backward compatibility.

        Parameters
        ----------
        F2 : Face
            The second face whose distance to this face is to be calculated.

        Returns
        -------
        float
            The distance between the two faces. See `distance_shape`.
        """
        return self.distance_shape(F2)