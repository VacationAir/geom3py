import math
from .point import Point
from .line import Line
from .plane import Plane
from .face import Face
from .vector import Vector
from ..utils.linal_utils import close

class Box:
    """
    Represents a rectangular box (parallelepiped) in 3D space.
    
    A box is defined by two opposite corner points P_min and P_max.
    Unlike a cube, the dimensions can be different in X, Y, and Z.
    
    This can represent:
    - A perfect cube (all dimensions equal)
    - A rectangular prism (different dimensions)
    - A building footprint extruded to a given height
    
    Parameters
    ----------
    P_min : array_like
        The minimum corner point (x0, y0, z0).
    P_max : array_like
        The maximum corner point (x1, y1, z1).
    
    Attributes
    ----------
    p_min : Point
        The minimum corner point.
    p_max : Point
        The maximum corner point.
    width : float
        The width (X dimension).
    depth : float
        The depth (Y dimension).
    height : float
        The height (Z dimension).
    vertices : tuple of Point
        The 8 vertices of the box.
    faces : list of Face
        The 6 faces of the box.
    bottom, top, front, back, left, right : Face
        Individual faces for easy access.
    """
    
    # ======================================================================
    # Constructors
    # ======================================================================

    def __init__(self, P_min, P_max):
        """
        Initializes a new box from two opposite corner points.

        Parameters
        ----------
        P_min : array_like
            The minimum corner point (x0, y0, z0).
        P_max : array_like
            The maximum corner point (x1, y1, z1).
        """
        self.p_min = Point(P_min)
        self.p_max = Point(P_max)
        
        self.width = self.p_max.x - self.p_min.x
        self.depth = self.p_max.y - self.p_min.y
        self.height = self.p_max.z - self.p_min.z

        x0, y0, z0 = self.p_min.x, self.p_min.y, self.p_min.z
        x1, y1, z1 = self.p_max.x, self.p_max.y, self.p_max.z

        # Los 8 vértices
        v1 = Point(x0, y0, z0)  # 0: min, min, min
        v2 = Point(x1, y0, z0)  # 1: max, min, min
        v3 = Point(x1, y1, z0)  # 2: max, max, min
        v4 = Point(x0, y1, z0)  # 3: min, max, min
        
        v5 = Point(x0, y0, z1)  # 4: min, min, max
        v6 = Point(x1, y0, z1)  # 5: max, min, max
        v7 = Point(x1, y1, z1)  # 6: max, max, max
        v8 = Point(x0, y1, z1)  # 7: min, max, max

        self.vertices = (v1, v2, v3, v4, v5, v6, v7, v8)

        self.bottom = Face(v1, v2, v3, v4)
        
        self.top = Face(v5, v6, v7, v8)
        
        self.front = Face(v1, v2, v6, v5)
        
        self.back = Face(v4, v3, v7, v8)
        
        self.left = Face(v1, v4, v8, v5)
        
        self.right = Face(v2, v3, v7, v6)

        self.faces = [self.bottom, self.top, self.front, self.back, self.left, self.right]
    
    @classmethod
    def from_footprint(cls, footprint, height):
        """
        Creates a box by extruding a 2D footprint to a given height.
        
        Parameters
        ----------
        footprint : Face
            A 2D Face representing the footprint (must be coplanar in XY plane).
        height : float
            The height to extrude in Z direction.
            
        Returns
        -------
        Box
            A box representing the extruded footprint.
        """
        xs = [v.x for v in footprint.edges]
        ys = [v.y for v in footprint.edges]
        
        return cls(
            Point(min(xs), min(ys), 0),
            Point(max(xs), max(ys), height)
        )
    
    # ======================================================================
    # Basic Operations
    # ======================================================================

    def surface_area(self):
        """
        Calculates the total surface area of the box.

        Returns
        -------
        float
            The total surface area.
        """
        return 2 * (self.width * self.depth + self.width * self.height + self.depth * self.height)
    
    def volume(self):
        """
        Calculates the volume of the box.

        Returns
        -------
        float
            The volume of the box.
        """
        return self.width * self.depth * self.height
    
    def diagonal(self):
        """
        Calculates the space diagonal of the box.

        Returns
        -------
        float
            The length of the space diagonal.
        """
        return math.sqrt(self.width**2 + self.depth**2 + self.height**2)
    
    def circumsphere_radius(self):
        """
        Calculates the radius of the circumsphere (sphere that contains the box).

        Returns
        -------
        float
            The circumsphere radius.
        """
        return self.diagonal() / 2
    
    def contains_point(self, Q):
        """
        Checks if a given point is inside the box.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point is inside the box, otherwise False.
        """
        q = Point(Q)
        return (self.p_min.x <= q.x <= self.p_max.x and 
                self.p_min.y <= q.y <= self.p_max.y and 
                self.p_min.z <= q.z <= self.p_max.z)
    
    def face_contains_point(self, Q):
        """
        Checks if a given point lies on any face of the box.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies on any face, otherwise False.
        """
        for F in self.faces:
            if F.contains_point(Q):
                return True
        return False

    def center(self):
        """
        Calculates the center point of the box.

        Returns
        -------
        Point
            The center point.
        """
        return Point((self.p_max - self.p_min) * 0.5)
    
    def point_on_edge(self, Q):
        """
        Checks if a given point lies on any edge of the box.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point lies on any edge, otherwise False.
        """
        for F in self.faces:
            if F.point_on_edge(Q):
                return True
        return False

    def point_on_corner(self, Q):
        """
        Checks if a given point matches any corner of the box.

        Parameters
        ----------
        Q : array_like
            The point to check.

        Returns
        -------
        bool
            True if the point matches a corner, otherwise False.
        """
        for F in self.faces:
            if F.point_on_corner(Q):
                return True
        return False

    # ======================================================================
    # Positional Relationships
    # ======================================================================    
    
    def position_line(self, G: Line, face: Face = None):
        """
        Determines the positional relationship of a line to the box.

        Parameters
        ----------
        G : Line
            The line to check.
        face : Face, optional
            Specific face to check against. If None, checks all faces.

        Returns
        -------
        list or str
            If face is None, returns a list of results for each face.
            If face is specified, returns a single result string.
        """
        if face is None:
            result = []
            for F in self.faces:
                result.append(F.position_line(G))
            return result
        else:
            return face.position_line(G)

    def position_plane(self, E: Plane, face: Face = None):
        """
        Determines the positional relationship of a plane to the box.

        Parameters
        ----------
        E : Plane
            The plane to check.
        face : Face, optional
            Specific face to check against. If None, checks all faces.

        Returns
        -------
        list or str
            If face is None, returns a list of results for each face.
            If face is specified, returns a single result string.
        """
        if face is None:
            result = []
            for F in self.faces:
                result.append(F.position_plane(E))
            return result
        else:
            return face.position_plane(E)
        
    def position_face(self, F2: Face, face: Face = None):
        """
        Determines the positional relationship of a face to the box.

        Parameters
        ----------
        F2 : Face
            The face to check.
        face : Face, optional
            Specific face to check against. If None, checks all faces.

        Returns
        -------
        list or str
            If face is None, returns a list of results for each face.
            If face is specified, returns a single result string.
        """
        if face is None:
            result = []
            for F in self.faces:
                result.append(F.position_face(F2))
            return result
        else:
            return face.position_face(F2)
        
    def position_box(self, W2: "Box"):
        """
        Determines the positional relationship between two boxes.

        Returns
        -------
        str
            One of: "identical", "contains", "is_contained", "intersecting",
            "on_face", "on_edge", "on_corner", "parallel", or "outside"
        """
        if self.p_min == W2.p_min and self.p_max == W2.p_max:
            return "identical"
        
        elif self.contains_point(W2.p_min) and self.contains_point(W2.p_max):
            return "contains"
        
        elif W2.contains_point(self.p_min) and W2.contains_point(self.p_max):
            return "is_contained"
        
        num_intersections = 0
        num_faces = 0
        num_corners = 0
        num_edges = 0
        num_parallel = 0

        for F1 in self.faces:
            for F2 in W2.faces:
                position = F1.position_face(F2)
                if position == "identical":
                    num_faces += 1
                
                elif position == "touching":
                    num_corners += 1
                
                elif position == "intersecting":
                    num_intersections += 1

                elif position == "parallel":
                    num_parallel += 1

                for K1 in F1.edges:
                    for K2 in F2.edges:
                        if K1.position_line(K2) == "identical":
                            num_edges += 1
                        
        if num_intersections > 0:
            return "intersecting"
        
        if num_faces > 0:
            return "on_face"
        
        if num_edges > 0:
            return "on_edge"
        
        if num_corners > 0:
            return "on_corner"
        
        if num_parallel > 0:
            return "parallel"
        
        return "outside"
    
    # ======================================================================
    # Intersection Calculations
    # ======================================================================   
    
    def intersection_line(self, G: Line):
        """
        Calculates intersections of a line with the box.

        Parameters
        ----------
        G : Line
            The line to intersect with the box.

        Returns
        -------
        list
            A list of intersection points or lines with each face.
        """
        result = []
        for F in self.faces:
            S = F.intersection_line(G)
            if S is not None:
                result.append(S)
        return result

    def intersection_plane(self, E: Plane):
        """
        Calculates intersections of a plane with the box.

        Parameters
        ----------
        E : Plane
            The plane to intersect with the box.

        Returns
        -------
        list
            A list of intersection results with each face.
        """
        result = []
        for F in self.faces:
            result.append(F.intersection_plane(E))
        return result

    def intersection_face(self, F2: Face):
        """
        Calculates intersections of a face with the box.

        Parameters
        ----------
        F2 : Face
            The face to intersect with the box.

        Returns
        -------
        list
            A list of intersection results with each face.
        """
        result = []
        for F in self.faces:
            result.append(F.intersection_face(F2))
        return result

    # ======================================================================
    # Distance Calculations
    # ======================================================================

    def distance_point(self, Q):
        """
        Calculates the minimum distance from a point to the box.

        Parameters
        ----------
        Q : array_like
            The point to measure distance from.

        Returns
        -------
        float
            The minimum distance to the box.
        """
        D = []
        for F in self.faces:
            D.append(F.distance_point(Q))
        return min(D)
    
    def distance_line(self, G: Line):
        """
        Calculates the minimum distance from a line to the box.

        Parameters
        ----------
        G : Line
            The line to measure distance from.

        Returns
        -------
        float
            The minimum distance to the box.
        """
        D = []
        for F in self.faces:
            D.append(F.distance_line(G))
        return min(D)

    def distance_plane(self, E: Plane):
        """
        Calculates the minimum distance from a plane to the box.

        Parameters
        ----------
        E : Plane
            The plane to measure distance from.

        Returns
        -------
        float
            The minimum distance to the box.
        """
        D = []
        for F in self.faces:
            D.append(F.distance_plane(E))
        return min(D)
    
    def distance_face(self, F2):
        """
        Calculates the minimum distance from a face to the box.

        Parameters
        ----------
        F2 : Face
            The face to measure distance from.

        Returns
        -------
        float
            The minimum distance to the box.
        """
        D = []
        for F in self.faces:
            D.append(F.distance_face(F2))
        return min(D)

    # ======================================================================
    # Transformations
    # ======================================================================

    def scale(self, factor):
        """
        Scales the box by a factor relative to the origin.

        Parameters
        ----------
        factor : float
            The scaling factor.

        Returns
        -------
        Box
            A new scaled box.
        """
        return Box(self.p_min.scale(factor), self.p_max.scale(factor))

    def rotate(self, angle, axis):
        """
        Rotates the box around a specified axis.

        Parameters
        ----------
        angle : float
            The rotation angle in degrees.
        axis : str
            The rotation axis ('x', 'y', or 'z').

        Returns
        -------
        Box
            A new rotated box.
        """
        return Box(self.p_min.rotate(angle, axis), self.p_max.rotate(angle, axis))

    def translate(self, v):
        """
        Translates the box by a vector.

        Parameters
        ----------
        v : array_like
            The translation vector.

        Returns
        -------
        Box
            A new translated box.
        """
        return Box(self.p_min.translate(v), self.p_max.translate(v))

    def reflect_on_point(self, P):
        """
        Reflects the box about a point.

        Parameters
        ----------
        P : array_like
            The point of reflection.

        Returns
        -------
        Box
            A new reflected box.
        """
        return Box(self.p_min.reflect_on_point(P), self.p_max.reflect_on_point(P))

    def reflect_on_line(self, g):
        """
        Reflects the box about a line.

        Parameters
        ----------
        g : Line
            The line of reflection.

        Returns
        -------
        Box
            A new reflected box.
        """
        return Box(self.p_min.reflect_on_line(g), self.p_max.reflect_on_line(g))

    def reflect_on_plane(self, E):
        """
        Reflects the box about a plane.

        Parameters
        ----------
        E : Plane
            The plane of reflection.

        Returns
        -------
        Box
            A new reflected box.
        """
        return Box(self.p_min.reflect_on_plane(E), self.p_max.reflect_on_plane(E))
    
    # ======================================================================
    # Visualization
    # ======================================================================

    def draw_on_canvas(self, canvas, camera, **kwargs):
        """
        Draws the box on a Tkinter canvas.

        Parameters
        ----------
        canvas : tk.Canvas
            The canvas to draw on.
        camera : Camera
            The camera for 3D to 2D projection.
        **kwargs : dict
            Styling options passed to each face.
        """
        faces_with_depth = []

        for face in self.faces:
            depth = face.get_depth(camera)
            faces_with_depth.append((depth, face))

        faces_with_depth.sort(key=lambda x: x[0], reverse=True)
        
        for _, face in faces_with_depth:
            face.draw_on_canvas(canvas, camera, **kwargs)

    def get_depth(self, camera):
        """
        Calculates the depth of the box with respect to the camera.

        Parameters
        ----------
        camera : Camera
            The camera for depth calculation.

        Returns
        -------
        float
            The average depth of all faces.
        """
        total = sum(face.get_depth(camera) for face in self.faces)
        return total / len(self.faces)