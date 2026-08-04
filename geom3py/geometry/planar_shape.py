import math
from abc import ABC, abstractmethod
from .point import Point
from .vector import Vector
from .line import Line
from .plane import Plane
from ..utils.linal_utils import close

class PlanarShape(ABC):
    """
    Abstract base class for planar shapes in three-dimensional space
    (Face, Triangle, ...).

    A planar shape is defined by an ordered list of corner points, which
    define the edges of the shape in this order. From the corner points,
    the edges, the center point, the normal vector and the associated
    plane are automatically calculated.

    This class cannot be instantiated directly. Concrete subclasses must
    implement `contains_point`, since the interior test depends on the
    specific shape (triangle, quadrilateral, ...).

    Parameters
    ----------
    points : list of array_like
        The corner points of the shape, in order (at least 3).

    Attributes
    ----------
    points : tuple of Point
        The corner points of the shape.
    n : int
        The number of corner points.
    edges : tuple of Line
        The edges connecting consecutive corner points.
    center : Point
        The center point of the shape (arithmetic mean of the corner points).
    normal_vector : Vector
        The normal vector of the shape's plane.
    plane : Plane
        The plane in which the shape lies.
    """
    # ======================================================================
    # Constructors
    # ======================================================================

    def __init__(self, points):
        """
        Initializes a new planar shape from its corner points.

        Parameters
        ----------
        points : list of array_like
            The corner points of the shape, in order (at least 3).

        Raises
        ------
        ValueError
            If fewer than 3 points are provided.
        """
        if len(points) < 3:
            raise ValueError("A PlanarShape needs at least 3 points.")

        self.points = tuple(
            p if isinstance(p, Point) else Point(p) for p in points
        )
        self.n = len(self.points)

        self.edges = self._compute_edges()
        self.center = self._compute_center()
        self.normal_vector = self._compute_normal()
        self.plane = Plane(self.points[0], self.normal_vector)

    def _compute_edges(self):
        """
        Computes all edges of the shape.

        Returns
        -------
        tuple of Line
            A tuple of Line objects connecting consecutive corner points.
        """
        edges = []
        for i in range(self.n):
            edges.append(Line.from_points(self.points[i], self.points[(i + 1) % self.n]))
        return tuple(edges)

    def _compute_center(self):
        """
        Computes the center (arithmetic mean) of all corner points.

        Returns
        -------
        Point
            The center point.
        """
        x = sum(p.x for p in self.points) / self.n
        y = sum(p.y for p in self.points) / self.n
        z = sum(p.z for p in self.points) / self.n
        return Point(x, y, z)

    def _compute_normal(self):
        """
        Computes the normal vector of the shape's plane.

        Returns
        -------
        Vector
            The normal vector, computed as the cross product of the
            direction vectors of the first two edges.
        """
        return self.edges[0].direction_vector.cross(self.edges[1].direction_vector)

    # ======================================================================
    # Basic Operations
    # ======================================================================

    def area(self):
        """
        Calculates the area of the shape.

        Uses the general 3D polygon area formula: area = 0.5 * |sum(v_i x v_{i+1})|,
        which is valid for any planar shape, triangle, quadrilateral or
        general N-gon.

        Returns
        -------
        float
            The area of the shape.
        """
        area_vector = Vector(0, 0, 0)
        for i in range(self.n):
            v1 = self.points[i]
            v2 = self.points[(i + 1) % self.n]
            area_vector += v1.cross(v2)
        return abs(area_vector.magnitude()) / 2

    def perimeter(self):
        """
        Calculates the perimeter of the shape.

        The perimeter is the sum of the lengths of all edges.

        Returns
        -------
        float
            The perimeter of the shape.
        """
        U = 0.0
        for e in self.edges:
            U += e.direction_vector.magnitude()
        return U

    @abstractmethod
    def contains_point(self, Q):
        """
        Checks if a given point lies within the shape.

        Must be implemented by every concrete subclass, since the
        interior test depends on the specific shape.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies within the shape, otherwise False.
        """
        ...

    def point_on_edge(self, Q):
        """
        Checks if a given point lies on one of the edges of the shape.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies on an edge (or corner) of the shape,
            otherwise False.
        """
        if self.point_on_corner(Q):
            return True

        for K in self.edges:
            r = K._calculate_quotient(Q)
            if r is not None and 0 <= r <= 1:
                return True

        return False

    def point_on_corner(self, Q):
        """
        Checks if a given point matches one of the corners of the shape.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point matches a corner of the shape, otherwise False.
        """
        for K in self.edges:
            if close(K.support_vector, Q):
                return True

        return False

    # ======================================================================
    # Positional Relationships
    # ======================================================================

    def position_line(self, G: Line):
        """
        Determines the positional relationship of this shape to a line.

        The possible relationships are:
        - "parallel": The line is parallel to the shape's plane.
        - "intersecting": The line penetrates the interior of the shape.
        - "outside": The line intersects the shape's plane but outside the shape.
        - "on_edge": The line is identical to an edge of the shape.
        - "touching": The line intersects exactly one edge of the shape.
        - "coplanar_outside": The line lies in the shape's plane but does not intersect any edge.

        If there is more than one edge intersection point, "intersecting" is returned.

        Parameters
        ----------
        G : Line
            The line whose position relative to the shape is to be determined.

        Returns
        -------
        str
            The positional relationship as a string.
        """
        position = self.plane.position_line(G)

        if position == "parallel":
            return "parallel"

        if position == "intersecting":
            S = self.plane.intersection_line(G)
            if self.contains_point(S):
                return "intersecting"
            else:
                return "outside"

        points = []
        for K in self.edges:
            position_K = G.position_line(K)

            if position_K == "identical":
                return "on_edge"

            elif position_K == "intersecting":
                S = G.intersection_line(K)
                r = K._calculate_quotient(S)
                if r is not None and 0 <= r <= 1:
                    if not any(close(S, P) for P in points):
                        points.append(S)

        n = len(points)

        if n == 0:
            return "coplanar_outside"
        elif n == 1:
            return "touching"
        else:
            return "intersecting"

    def position_plane(self, E: Plane):
        """
        Determines the positional relationship of this shape to a plane.

        The possible relationships are:
        - "identical": The shape lies completely in the plane.
        - "parallel": The plane is parallel to the shape's plane but not identical.
        - "touching": The intersection consists only of a corner point of the shape.
        - "intersecting": The intersection runs through the interior of the shape.
        - "on_edge": The intersection runs along an edge of the shape.
        - "outside": The planes intersect but outside the shape.

        Parameters
        ----------
        E : Plane
            The plane whose position relative to the shape is to be determined.

        Returns
        -------
        str
            The positional relationship as a string.
        """
        if self.plane.position_plane(E) == "parallel":
            return "parallel"

        if self.plane.position_plane(E) == "identical":
            return "identical"

        if self.plane.position_plane(E) == "intersecting":
            gS = self.plane.intersection_plane(E)
            result_gS = self.position_line(gS)

            if result_gS == "intersecting":
                return "intersecting"
            elif result_gS == "on_edge":
                return "on_edge"
            elif result_gS == "touching":
                return "touching"
            else:
                return "outside"

    def position_shape(self, other: "PlanarShape"):
        """
        Determines the positional relationship of this shape to another
        planar shape.

        The possible relationships include:
        - "identical": Both shapes have the same corner points.
        - "parallel": The shape planes are parallel but not identical.
        - "intersecting": The planes intersect and the intersection line runs through the interior of both shapes.
        - "on_edge": The shapes lie in the same plane and share a collinear edge segment.
        - "coplanar_intersecting": The shapes lie in the same plane and overlap with more than one edge intersection point or the center of one shape lies in the other.
        - "edge_intersecting": The shapes lie in the same plane and have exactly one true edge intersection point that is not a shared corner.
        - "touching": The shapes touch at exactly one shared corner.
        - "coplanar_outside": The shapes lie in the same plane but do not overlap.
        - "outside": None of the above positional relationships apply.

        Parameters
        ----------
        other : PlanarShape
            The second shape whose position relative to this shape is to be determined.

        Returns
        -------
        str
            The positional relationship as a string.
        """
        position = self.plane.position_plane(other.plane)

        if self.n == other.n and all(close(P1, P2) for P1, P2 in zip(self.points, other.points)):
            return "identical"

        elif position == "parallel":
            return "parallel"

        elif position == "intersecting":
            gS = self.plane.intersection_plane(other.plane)

            position_in_self = self.position_line(gS)
            position_in_other = other.position_line(gS)

            if position_in_self == "intersecting" and position_in_other == "intersecting":
                return "intersecting"
            else:
                return "outside"

        elif position == "identical":
            if self.n == other.n and all(any(close(P1, P2) for P2 in other.points) for P1 in self.points):
                return "identical"

            strict_intersection_points = []
            shared_corners = 0
            collinear_edge_shared = False

            # Evaluate true intersection points
            for K1 in self.edges:
                for K2 in other.edges:
                    lg = K1.position_line(K2)
                    if lg == "intersecting":
                        S = K1.intersection_line(K2)
                        r1 = K1._calculate_quotient(S)
                        r2 = K2._calculate_quotient(S)
                        if r1 is not None and 0 <= r1 <= 1 and r2 is not None and 0 <= r2 <= 1:
                            if not any(close(S, p) for p in strict_intersection_points):
                                strict_intersection_points.append(S)
                    elif lg == "identical":
                        # Check if the edge segments actually share a common area
                        u = K2.support_vector
                        v = K2.support_vector + K2.direction_vector
                        r1 = K1._calculate_quotient(u)
                        r2 = K1._calculate_quotient(v)
                        if r1 is not None and r2 is not None:
                            if max(min(r1, r2), 0) < min(max(r1, r2), 1):
                                collinear_edge_shared = True

            # Count exactly shared corners
            for P1 in self.points:
                if any(close(P1, P2) for P2 in other.points):
                    shared_corners += 1

            num_intersections = len(strict_intersection_points)

            # Analytical classification according to exact test conditions:
            if collinear_edge_shared:
                return "on_edge"

            if num_intersections > 1:
                return "coplanar_intersecting"

            if num_intersections == 1:
                if shared_corners == 1:
                    return "touching"
                return "edge_intersecting"

            if self.contains_point(other.center) or other.contains_point(self.center):
                return "coplanar_intersecting"

            if shared_corners == 1:
                return "touching"

            return "coplanar_outside"

        return "outside"

    # ======================================================================
    # Intersection Calculations
    # ======================================================================

    def intersection_line(self, G: Line):
        """
        Calculates the intersection of this shape with a line.

        Depending on the positional relationship between shape and line (see
        `position_line`), the line itself, the intersection point with the
        shape's plane, an edge of the shape or None is returned.

        Parameters
        ----------
        G : Line
            The line whose intersection with the shape is to be calculated.

        Returns
        -------
        Line or Point or None
            The result of the intersection calculation, depending on the
            positional relationship between shape and line.
        """
        result = self.position_line(G)

        if result == "identical":
            return G

        if result == "intersecting" or result == "touching":
            S = self.plane.intersection_line(G)
            return S

        if result == "on_edge":
            for K in self.edges:
                if G.position_line(K) == "identical":
                    return K

        return None

    def intersection_plane(self, E: Plane):
        """
        Calculates the intersection of this shape with a plane.

        Depending on the positional relationship between shape and plane (see
        `position_plane`), None, the intersection line of the two planes
        or a touching corner point of the shape is returned.

        Parameters
        ----------
        E : Plane
            The plane whose intersection with the shape is to be calculated.

        Returns
        -------
        Line or Point or None
            The result of the intersection calculation, depending on the
            positional relationship between shape and plane.
        """
        result = self.position_plane(E)

        if result in ("parallel", "outside", "identical"):
            return None

        elif result in ("on_edge", "intersecting"):
            return self.plane.intersection_plane(E)

        elif result == "touching":
            for P in self.points:
                if E.contains_point(P):
                    return P

    def _order_coplanar_points(self, points):
        """
        Orders a set of coplanar points counter-clockwise around their
        centroid, so they form a valid, non self-intersecting polygon.

        This is needed because points collected from edge intersections
        and shared corners come in no particular order, and connecting
        them as-is can produce a self-intersecting ("bowtie") shape.

        Parameters
        ----------
        points : list of Point
            The coplanar points to order.

        Returns
        -------
        list of Point
            The same points, sorted counter-clockwise around their centroid.
        """
        cx = sum(p.x for p in points) / len(points)
        cy = sum(p.y for p in points) / len(points)
        cz = sum(p.z for p in points) / len(points)
        centroid = Point(cx, cy, cz)

        normal = self.normal_vector.normalize()
        reference = Vector(1, 0, 0)
        if abs(normal.dot(reference)) > 0.9:
            reference = Vector(0, 1, 0)

        u = normal.cross(reference).normalize()
        v = normal.cross(u).normalize()

        def angle(p):
            d = p - centroid
            return math.atan2(d.dot(v), d.dot(u))

        return sorted(points, key=angle)

    def intersection_shape(self, other: "PlanarShape"):
        """
        Calculates the intersection of this shape with another planar shape.

        Depending on the positional relationship between the two shapes (see
        `position_shape`), None, the second shape, the intersection line
        of the planes, a touching point, an edge intersection point, or a
        new shape formed from the intersection points is returned.

        Parameters
        ----------
        other : PlanarShape
            The second shape whose intersection with this shape is to be calculated.

        Returns
        -------
        PlanarShape or Polygon or Point or Line or None
            The result of the intersection calculation, depending on the
            positional relationship between the two shapes.
        """
        result = self.position_shape(other)

        if result in ("outside", "coplanar_outside", "parallel"):
            return None

        elif result == "identical":
            return other

        elif result == "intersecting":
            return self.plane.intersection_plane(other.plane)

        elif result == "touching":
            for P1 in self.points:
                if other.point_on_edge(P1):
                    return P1

            for P2 in other.points:
                if self.point_on_edge(P2):
                    return P2

        elif result == "edge_intersecting":
            for K1 in self.edges:
                for K2 in other.edges:
                    if K1.position_line(K2) != "intersecting":
                        continue

                    S = K1.intersection_line(K2)
                    r1 = K1._calculate_quotient(S)
                    r2 = K2._calculate_quotient(S)

                    if (
                        r1 is not None and 0 <= r1 <= 1 and
                        r2 is not None and 0 <= r2 <= 1
                    ):
                        return S

        elif result == "coplanar_intersecting":
            P = []

            # 1. Collect points where edges actually intersect
            for K1 in self.edges:
                for K2 in other.edges:
                    if K1.position_line(K2) == "intersecting":
                        pt = K1.intersection_line(K2)
                        r1 = K1._calculate_quotient(pt)
                        r2 = K2._calculate_quotient(pt)
                        if r1 is not None and 0 <= r1 <= 1 and r2 is not None and 0 <= r2 <= 1:
                            if not any(close(pt, e) for e in P):
                                P.append(pt)

            # 2. Add corner points from self that lie within other
            for P1 in self.points:
                if other.contains_point(P1) and not any(close(P1, e) for e in P):
                    P.append(P1)

            # 3. Add corner points from other that lie within self
            for P2 in other.points:
                if self.contains_point(P2) and not any(close(P2, e) for e in P):
                    P.append(P2)

            if len(P) < 3:
                return None

            P = self._order_coplanar_points(P)

            if len(P) == self.n:
                return type(self)(*P)

            from .polygon import Polygon
            return Polygon(P)

    # ======================================================================
    # Distance Calculations
    # ======================================================================

    def distance_point(self, Q):
        """
        Calculates the distance from a point to this shape.

        First, the foot point of the point on the shape's plane is determined.
        If this lies within the shape, the distance corresponds to the
        distance to the plane. Otherwise, the minimum distance from the
        point to the edges of the shape is returned.

        Parameters
        ----------
        Q : array_like
            The point whose distance to the shape is to be calculated.

        Returns
        -------
        float
            The distance from the point to the shape.
        """
        Q = Vector(Q)

        EQ = Line(Q, self.plane.normal_vector)
        L = self.plane.intersection_line(EQ)
        # Check if the orthogonal foot point is a point of the shape

        if L is not None and self.contains_point(L):
            LQ = Q - L
            d = LQ.magnitude()
            return d
        else:
            D = [K.distance_point(Q) for K in self.edges]
            return min(D)

        return None

    def distance_line(self, G: Line):
        """
        Calculates the distance from this shape to a line.

        If the line intersects the shape, the distance is 0. Otherwise,
        depending on the positional relationship between line and shape plane,
        the minimum distance is determined via the edges of the shape or via the plane.

        Parameters
        ----------
        G : Line
            The line whose distance to the shape is to be calculated.

        Returns
        -------
        float
            The distance between the shape and the line.
        """
        if self.intersection_line(G) is not None:
            return 0.0

        elif self.plane.position_line(G) in ("identical", "coplanar_outside"):
            D = []
            for K in self.edges:
                D.append(K.distance_line(G))

            return min(D)

        elif self.plane.position_line(G) == "parallel":
            return self.plane.distance_line(G)

        elif self.position_line(G) == "outside":
            S = self.plane.intersection_line(G)
            D = []
            for K in self.edges:
                D.append(K.distance_point(S))
                D.append(K.distance_line(G))

            return min(D)

    def distance_plane(self, E: Plane):
        """
        Calculates the distance from this shape to a plane.

        In case of intersection, identity, touching or position on an edge,
        the distance is 0. For parallel position, the plane distance is used,
        otherwise the distance is determined via the intersection line of the two planes.

        Parameters
        ----------
        E : Plane
            The plane whose distance to the shape is to be calculated.

        Returns
        -------
        float
            The distance between the shape and the plane.
        """
        result = self.position_plane(E)

        if result in ("intersecting", "identical", "touching", "on_edge"):
            return 0.0

        elif result == "parallel":
            return self.plane.distance_plane(E)

        elif result == "outside":
            gS = self.plane.intersection_plane(E)

            return self.distance_line(gS)

    def distance_shape(self, other: "PlanarShape"):
        """
        Calculates the distance from this shape to another planar shape.

        For intersecting, touching or identical shapes, the distance is 0.
        For parallel position, the plane distance is used.
        Otherwise, the minimum distance between the corner points of one shape
        and the (bounded) edges of the other shape is determined.

        Parameters
        ----------
        other : PlanarShape
            The second shape whose distance to this shape is to be calculated.

        Returns
        -------
        float
            The distance between the two shapes.
        """
        result = self.position_shape(other)

        if result in ("identical", "intersecting", "coplanar_intersecting", "edge_intersecting", "on_edge", "touching"):
            return 0.0

        elif result == "parallel":
            return self.plane.distance_plane(other.plane)

        elif result in ("outside", "coplanar_outside"):
            D = []

            # 1. Distance from each corner point of self to each bounded edge of other
            for P in self.points:
                for K in other.edges:
                    L = K.foot_point(P)
                    r = K._calculate_quotient(L)

                    if r is not None and 0 <= r <= 1:
                        D.append((P - L).magnitude())

            # 2. Distance from each corner point of other to each bounded edge of self
            for P in other.points:
                for K in self.edges:
                    L = K.foot_point(P)
                    r = K._calculate_quotient(L)

                    if r is not None and 0 <= r <= 1:
                        D.append((P - L).magnitude())

            return min(D) if D else 0.0

    # ======================================================================
    # Transformations
    # ======================================================================

    def scale(self, factor):
        """
        Scales the shape by a factor relative to the origin.

        Parameters
        ----------
        factor : float
            The scaling factor

        Returns
        -------
        PlanarShape
            A new scaled shape of the same concrete type
        """
        return type(self)(*[p.scale(factor) for p in self.points])

    def rotate(self, angle, axis):
        """
        Rotates the shape around a specified axis.

        Parameters
        ----------
        angle : float
            The rotation angle in degrees
        axis : str
            The rotation axis ('x', 'y', or 'z')

        Returns
        -------
        PlanarShape
            A new rotated shape of the same concrete type
        """
        return type(self)(*[p.rotate(angle, axis) for p in self.points])

    def translate(self, v):
        """
        Translates the shape by a vector.

        Parameters
        ----------
        v : array_like
            The translation vector

        Returns
        -------
        PlanarShape
            A new translated shape of the same concrete type
        """
        return type(self)(*[p.translate(v) for p in self.points])

    def reflect_on_point(self, P):
        """
        Reflects the shape about a point.

        Parameters
        ----------
        P : array_like
            The point of reflection

        Returns
        -------
        PlanarShape
            A new reflected shape of the same concrete type
        """
        return type(self)(*[p.reflect_on_point(P) for p in self.points])

    def reflect_on_line(self, g):
        """
        Reflects the shape about a line.

        Parameters
        ----------
        g : Line
            The line of reflection

        Returns
        -------
        PlanarShape
            A new reflected shape of the same concrete type
        """
        return type(self)(*[p.reflect_on_line(g) for p in self.points])

    def reflect_on_plane(self, E):
        """
        Reflects the shape about a plane.

        Parameters
        ----------
        E : Plane
            The plane of reflection

        Returns
        -------
        PlanarShape
            A new reflected shape of the same concrete type
        """
        return type(self)(*[p.reflect_on_plane(E) for p in self.points])

    # ======================================================================
    # Visualization
    # ======================================================================

    def draw_on_canvas(self, canvas, camera, **kwargs):
        """
        Draws the shape on a Tkinter canvas.

        Parameters
        ----------
        canvas : tk.Canvas
            The canvas to draw on
        camera : Camera
            The camera for 3D to 2D projection
        **kwargs : dict
            Styling options:
            - fill : str
                Fill color of the shape (default: '#A1FFFF')
            - outline : str
                Outline color of the shape (default: '#52FFFF')
            - width : int
                Width of the outline in pixels (default: 2)

        Returns
        -------
        None

        Notes
        -----
        If any vertex is behind the camera (projection returns None),
        the shape is not drawn.
        """
        points_2d = []
        for p in self.points:
            x, y = camera.project(p)
            if x is None or y is None:
                return
            points_2d.extend([x, y])

        fill_color = kwargs.get("fill", "#A1FFFF")
        outline_color = kwargs.get("outline", "#52FFFF")
        width = kwargs.get("width", 2)

        canvas.create_polygon(
            points_2d,
            fill=fill_color,
            outline=outline_color,
            width=width,
            tags=(type(self).__name__.lower(),)
        )

    def get_depth(self, camera):
        """
        Calculates the depth of the shape with respect to the camera.

        Parameters
        ----------
        camera : Camera
            The camera for depth calculation

        Returns
        -------
        float
            The depth (Z-coordinate) of the shape's center in camera space

        Notes
        -----
        This is used for z-ordering when rendering multiple objects.
        Objects with larger depth values are drawn first (farther away).
        Uses the shape's center point for consistent depth calculation.
        """
        center = self.center
        projected = camera.remapping(center)
        return projected.z

    def __repr__(self):
        """
        Returns a readable string representation of the shape.

        Returns
        -------
        str
            A string representation of the shape.
        """
        return f"{type(self).__name__}(points={self.points}, edges={self.edges}, normal={self.normal_vector})"