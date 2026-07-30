from .point import Point
from .line import Line
from .plane import Plane
from .vector import Vector
from ..utils.linal_utils import close

class Face:
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
    edge_X1_X2 : Line
        The edge between X1 and X2.
    edge_X2_X3 : Line
        The edge between X2 and X3.
    edge_X3_X4 : Line
        The edge between X3 and X4.
    edge_X4_X1 : Line
        The edge between X4 and X1.
    edges : tuple of Line
        All four edges of the face in order
        (edge_X1_X2, edge_X2_X3, edge_X3_X4, edge_X4_X1).
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
        self.X1 = Point(X1)
        self.X2 = Point(X2)
        self.X3 = Point(X3)
        self.X4 = Point(X4)
        self.points = (
            self.X1,
            self.X2,
            self.X3,
            self.X4
        )

        self.edge_X1_X2 = Line.from_points(X1, X2)
        self.edge_X2_X3 = Line.from_points(X2, X3)
        self.edge_X3_X4 = Line.from_points(X3, X4)
        self.edge_X4_X1 = Line.from_points(X4, X1)
        self.edges = (
            self.edge_X1_X2,
            self.edge_X2_X3,
            self.edge_X3_X4,
            self.edge_X4_X1,
        )

        self.d1 = Line.from_points(self.X4, self.X2)
        self.d2 = Line.from_points(self.X1, self.X3)

        self.center = Point((self.X1 + self.X2 + self.X3 + self.X4) / 4)
        self.normal_vector = self.edge_X1_X2.direction_vector.cross(self.edge_X2_X3.direction_vector)
        self.plane = Plane(self.X1, self.normal_vector)

    # ======================================================================
    # Basic Operations
    # ======================================================================

    def area(self):
        """
        Calculates the area of the face.

        The face is divided along diagonal d1 into two triangles,
        whose areas are calculated via the cross product and then added.

        Returns
        -------
        float
            The area of the face.
        """
        A1 = 0.5 * (self.edge_X4_X1.direction_vector.cross(self.d1.direction_vector)).magnitude()
        A2 = 0.5 * (self.edge_X2_X3.direction_vector.cross(self.d1.direction_vector)).magnitude()
        
        return A1 + A2
    
    def perimeter(self):
        """
        Calculates the perimeter of the face.

        The perimeter is the sum of the lengths of all four edges.

        Returns
        -------
        float
            The perimeter of the face.
        """
        U = (self.edge_X1_X2.direction_vector.magnitude() + 
             self.edge_X2_X3.direction_vector.magnitude() + 
             self.edge_X3_X4.direction_vector.magnitude() + 
             self.edge_X4_X1.direction_vector.magnitude())
        
        return U

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

        L = self.edge_X1_X2.foot_point(Q)
        LX2_X3 = self.edge_X2_X3.foot_point(Q)    
        LX3_X4 = self.edge_X3_X4.foot_point(Q)    
        LX4_X1 = self.edge_X4_X1.foot_point(Q)    

        v1 = Q - L
        v2 = LX2_X3 - Q
        v3 = LX3_X4 - Q
        v4 = LX4_X1 - Q

        L_list = [L, LX2_X3, LX3_X4, LX4_X1]
        G_list = [self.edge_X1_X2, self.edge_X2_X3, self.edge_X3_X4, self.edge_X4_X1]

        if v1.dot(v2) >= 0 or v1.dot(v3) >= 0 or v1.dot(v4) >= 0:
            for i in range(len(L_list)):
                r = G_list[i]._calculate_quotient(L_list[i])
                if r is None or not (0 <= r <= 1):
                    return False
            
            return True
        
        else:
            return False

    def point_on_edge(self, Q):
        """
        Checks if a given point lies on one of the edges of the face.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies on an edge (or corner) of the face,
            otherwise False.
        """
        for K in self.edges:
            if self.point_on_corner(Q):
                return True
            
            r = K._calculate_quotient(Q)
            if r is not None and 0 <= r <= 1:
                return True

        return False

    def point_on_corner(self, Q):
        """
        Checks if a given point matches one of the corners of the face.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point matches a corner of the face, otherwise False.
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
        Determines the positional relationship of this face to a line.

        The possible relationships are:
        - "parallel": The line is parallel to the face plane.
        - "intersecting": The line penetrates the interior of the face.
        - "outside": The line intersects the face plane but outside the face.
        - "on_edge": The line is identical to an edge of the face.
        - "touching": The line intersects exactly one edge of the face.
        - "coplanar_outside": The line lies in the face plane but does not intersect any edge.

        If there is more than one edge intersection point, "intersecting" is returned.

        Parameters
        ----------
        G : Line
            The line whose position relative to the face is to be determined.

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
        Determines the positional relationship of this face to a plane.

        The possible relationships are:
        - "identical": The face lies completely in the plane.
        - "parallel": The plane is parallel to the face plane but not identical.
        - "touching": The intersection consists only of a corner point of the face.
        - "intersecting": The intersection runs through the interior of the face.
        - "on_edge": The intersection runs along an edge of the face.
        - "outside": The planes intersect but outside the face.

        Parameters
        ----------
        E : Plane
            The plane whose position relative to the face is to be determined.

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

    def position_face(self, F2: "Face"):
        """
        Determines the positional relationship of this face to another face.

        The possible relationships include:
        - "identical": Both faces have the same corner points.
        - "parallel": The face planes are parallel but not identical.
        - "intersecting": The planes intersect and the intersection line runs through the interior of both faces.
        - "on_edge": The faces lie in the same plane and share a collinear edge segment.
        - "coplanar_intersecting": The faces lie in the same plane and overlap with more than one edge intersection point or the center of one face lies in the other.
        - "edge_intersecting": The faces lie in the same plane and have exactly one true edge intersection point that is not a shared corner.
        - "touching": The faces touch at exactly one shared corner.
        - "coplanar_outside": The faces lie in the same plane but do not overlap.
        - "outside": None of the above positional relationships apply.

        Parameters
        ----------
        F2 : Face
            The second face whose position relative to this face is to be determined.

        Returns
        -------
        str
            The positional relationship as a string.
        """
        position = self.plane.position_plane(F2.plane)
 
        if all(close(P1, P2) for P1, P2 in zip(self.points, F2.points)):
            return "identical"
        
        elif position == "parallel":
            return "parallel"
        
        elif position == "intersecting":
            gS = self.plane.intersection_plane(F2.plane)
 
            position_in_F1 = self.position_line(gS)
            position_in_F2 = F2.position_line(gS)

            if position_in_F1 == "intersecting" and position_in_F2 == "intersecting":
                return "intersecting"
            else:
                return "outside"
        
        elif position == "identical":
            if all(any(close(P1, P2) for P2 in F2.points) for P1 in self.points):
                return "identical"
 
            strict_intersection_points = []
            shared_corners = 0
            collinear_edge_shared = False
 
            # Evaluate true intersection points
            for K1 in self.edges:
                for K2 in F2.edges:
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
                if any(close(P1, P2) for P2 in F2.points):
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
                
            if self.contains_point(F2.center) or F2.contains_point(self.center):
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
        Calculates the intersection of this face with a line.

        Depending on the positional relationship between face and line (see
        `position_line`), the line itself, the intersection point with the
        face plane, an edge of the face or None is returned.

        Parameters
        ----------
        G : Line
            The line whose intersection with the face is to be calculated.

        Returns
        -------
        Line or Point or None
            The result of the intersection calculation, depending on the
            positional relationship between face and line.
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
        Calculates the intersection of this face with a plane.

        Depending on the positional relationship between face and plane (see
        `position_plane`), None, the intersection line of the two planes
        or a touching corner point of the face is returned.

        Parameters
        ----------
        E : Plane
            The plane whose intersection with the face is to be calculated.

        Returns
        -------
        Line or Point or None
            The result of the intersection calculation, depending on the
            positional relationship between face and plane.
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

    def intersection_face(self, F2: "Face"):
        """
        Calculates the intersection of this face with another face.

        Depending on the positional relationship between the two faces (see
        `position_face`), None, the second face, the intersection line
        of the planes, a touching point, an edge intersection point, or a
        new face formed from the intersection points is returned.

        Parameters
        ----------
        F2 : Face
            The second face whose intersection with this face is to be calculated.

        Returns
        -------
        Face or Point or Line or None
            The result of the intersection calculation, depending on the
            positional relationship between the two facess.
        """
        result = self.position_face(F2)

        if result in ("outside", "coplanar_outside", "parallel"):
            return None
        
        elif result == "identical":
            return F2

        elif result == "intersecting":
            return self.plane.intersection_plane(F2.plane)
        
        elif result == "touching":
            P = []

            for P1 in self.points:
                if F2.point_on_edge(P1):
                    return P1
                
            for P2 in F2.points:
                if self.point_on_edge(P2):
                    return P2
        
        elif result == "edge_intersecting":
            for K1 in self.edges:
                for K2 in F2.edges:
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
                for K2 in F2.edges:
                    if K1.position_line(K2) == "intersecting":
                        pt = K1.intersection_line(K2)
                        r1 = K1._calculate_quotient(pt)
                        r2 = K2._calculate_quotient(pt)
                        if r1 is not None and 0 <= r1 <= 1 and r2 is not None and 0 <= r2 <= 1:
                            if not any(close(pt, e) for e in P):
                                P.append(pt)

            # 2. Add corner points from F1 that lie within F2
            for P1 in self.points:
                if F2.contains_point(P1) and not any(close(P1, e) for e in P):
                    P.append(P1)

            # 3. Add corner points from F2 that lie within F1
            for P2 in F2.points:
                if self.contains_point(P2) and not any(close(P2, e) for e in P):
                    P.append(P2)

            if len(P) >= 4:
                # Sort points minimally to form a valid face if needed
                return Face(P[0], P[1], P[2], P[3])
            
            return None
            
    # ======================================================================
    # Distance Calculations
    # ======================================================================

    def distance_point(self, Q):
        """
        Calculates the distance from a point to this face.

        First, the foot point of the point on the face plane is determined.
        If this lies within the face, the distance corresponds to the
        distance to the plane. Otherwise, the minimum distance from the
        point to the four edges of the face is returned.

        Parameters
        ----------
        Q : array_like
            The point whose distance to the face is to be calculated.

        Returns
        -------
        float
            The distance from the point to the face.
        """
        Q = Vector(Q)
        
        EQ = Line(Q, self.plane.normal_vector)
        L = self.plane.intersection_line(EQ)
        # Check if the orthogonal foot point is a point of the face

        if L is not None and self.contains_point(L):
            LQ = Q - L
            d = LQ.magnitude()
            return d
        else:
            D = [
                self.edge_X1_X2.distance_point(Q),
                self.edge_X2_X3.distance_point(Q),
                self.edge_X3_X4.distance_point(Q),
                self.edge_X4_X1.distance_point(Q)
            ]

            return min(D)
        
        return None

    def distance_line(self, G: Line):
        """
        Calculates the distance from this face to a line.

        If the line intersects the face, the distance is 0. Otherwise,
        depending on the positional relationship between line and face plane,
        the minimum distance is determined via the edges of the face or via the plane.

        Parameters
        ----------
        G : Line
            The line whose distance to the face is to be calculated.

        Returns
        -------
        float
            The distance between the face and the line.
        """
        if self.intersection_line(G) is not None:
            return 0.0
        
        elif self.plane.position_line(G) in ("identical", "coplanar_outside"):
            D = []
            for K in [self.edge_X1_X2, self.edge_X2_X3, self.edge_X3_X4, self.edge_X4_X1]:
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
        Calculates the distance from this face to a plane.

        In case of intersection, identity, touching or position on an edge,
        the distance is 0. For parallel position, the plane distance is used,
        otherwise the distance is determined via the intersection line of the two planes.

        Parameters
        ----------
        E : Plane
            The plane whose distance to the face is to be calculated.

        Returns
        -------
        float
            The distance between the face and the plane.
        """
        result = self.position_plane(E)

        if result in ("intersecting", "identical", "touching", "on_edge"):
            return 0.0
        
        elif result == "parallel":
            return self.plane.distance_plane(E)
        
        elif result == "outside":
            gS = self.plane.intersection_plane(E)
            
            return self.distance_line(gS)

    def distance_face(self, F2):
        """
        Calculates the distance from this face to another face.

        For intersecting, touching or identical faces, the distance is 0.
        For parallel position, the plane distance is used.
        Otherwise, the minimum distance between the corner points of one face
        and the (bounded) edges of the other face is determined.

        Parameters
        ----------
        F2 : face
            The second face whose distance to this face is to be calculated.

        Returns
        -------
        float
            The distance between the two faces.
        """
        result = self.position_face(F2)

        if result in ("identical", "intersecting", "coplanar_intersecting", "edge_intersecting", "on_edge", "touching"):
            return 0.0

        elif result == "parallel":
            return self.plane.distance_plane(F2.plane)
        
        elif result in ("outside", "coplanar_outside"):
            D = []

            # 1. Distance from each corner point of F1 to each bounded edge of F2
            for P in self.points:
                for K in F2.edges:
                    L = K.foot_point(P)
                    r = K._calculate_quotient(L)

                    if r is not None and 0 <= r <= 1:
                        D.append((P - L).magnitude())

            # 2. Distance from each corner point of F2 to each bounded edge of F1
            for P in F2.points:
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
        return Face(
            self.X1.scale(factor),
            self.X2.scale(factor),
            self.X3.scale(factor),
            self.X4.scale(factor)
        )

    def rotate(self, angle, axis):
        return Face(
            self.X1.rotate(angle, axis),
            self.X2.rotate(angle, axis),
            self.X3.rotate(angle, axis),
            self.X4.rotate(angle, axis)
        )

    def translate(self, v):
        return Face(
            self.X1.translate(v),
            self.X2.translate(v),
            self.X3.translate(v),
            self.X4.translate(v)        
        )

    def reflect_on_point(self, P):
        return Face(
            self.X1.reflect_on_point(P),
            self.X2.reflect_on_point(P),
            self.X3.reflect_on_point(P),
            self.X4.reflect_on_point(P)            
        )

    def reflect_on_line(self, g):
        return Face(
            self.X1.reflect_on_line(g),
            self.X2.reflect_on_line(g),
            self.X3.reflect_on_line(g),
            self.X4.reflect_on_line(g)            
        )

    def reflect_on_plane(self, E):
        return Face(
            self.X1.reflect_on_plane(E),
            self.X2.reflect_on_plane(E),
            self.X3.reflect_on_plane(E),
            self.X4.reflect_on_plane(E)            
        )

    # ======================================================================
    # Visualization
    # ======================================================================

    def draw_on_canvas(self, canvas, camera, **kwargs):
            points_2d = []
            for p in self.points:
                points_2d.extend(camera.project(p))

            fill_color = kwargs.get("fill", "lightgreen")
            outline_color = kwargs.get("outline", "green")
            width = kwargs.get("width", 2)

            canvas.create_polygon(
                points_2d,
                fill=fill_color,
                outline = outline_color,
                width=width,
                tags = ("face", )
            )

    def get_depth(self, camera):
        """
        Calculates the depth of the face with respect tot he camera.
        """
        center = self.center 
        projected = camera.remapping(center)
        return projected.z
    
    def __repr__(self):
        """
        Returns a readable string representation of the face.

        Returns
        -------
        str
            A string representation of the face.
        """
        return f"Face(points={self.points}, edges={self.edges}, normal={self.normal_vector})"