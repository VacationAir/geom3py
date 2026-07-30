import math
from .point import Point
from .line import Line
from .plane import Plane
from .face import Face

class Cube:

    # ======================================================================
    # Constructors
    # ======================================================================

    def __init__(self, P_min, P_max):
        self.p_min = Point(P_min)
        self.p_max = Point(P_max)
        self.a = (self.p_max - self.p_min).magnitude() / math.sqrt(3)

        x0, y0, z0 = self.p_min.x, self.p_min.y, self.p_min.z
        x1, y1, z1 = self.p_max.x, self.p_max.y, self.p_max.z

        v1 = Point(x0, y0, z0)
        v2 = Point(x1, y0, z0)
        v3 = Point(x1, y1, z0)
        v4 = Point(x0, y1, z0)
        
        v5 = Point(x0, y0, z1)
        v6 = Point(x1, y0, z1)
        v7 = Point(x1, y1, z1)
        v8 = Point(x0, y1, z1)

        self.vertices = (v1, v2, v3, v4, v5, v6, v7, v8)

        self.bottom = Face(v1, v2, v3, v4)
        self.top    = Face(v5, v6, v7, v8)
        self.front  = Face(v1, v2, v6, v5)
        self.back   = Face(v4, v3, v7, v8)
        self.left   = Face(v1, v4, v8, v5)
        self.right  = Face(v2, v3, v7, v6)

        self.faces = [self.bottom, self.top, self.front, self.back, self.left, self.right]

    # ======================================================================
    # Basic Operations
    # ======================================================================

    def surface_area(self):
        A = 0

        for F in self.faces:
            A += F.area()

        return A
    
    def volume(self):
        M = self.front.area()
        h = self.a

        return M * h
    
    def circumsphere_radius(self):
        return self.a / 2
    
    def contains_point(self, Q):
        q = Point(Q)
        return (self.p_min.x <= q.x <= self.p_max.x and 
                self.p_min.y <= q.y <= self.p_max.y and 
                self.p_min.z <= q.z <= self.p_max.z)
    
    def face_contains_point(self, Q):
        for F in self.faces:
            if F.contains_point(Q):
                return True
            
        return False

    def center(self):
        return Point((self.p_max - self.p_min) * 0.5)
    
    def point_on_edge(self, Q):
        for F in self.faces:
            if F.point_on_edge(Q):
                return True
            
        return False

    def point_on_corner(self, Q):
        for F in self.faces:
            if F.point_on_corner(Q):
                return True
            
        return False

    # ======================================================================
    # Positional Relationships
    # ======================================================================    
    
    def position_line(self, G: Line, face: Face = None):
        if face is None:
            result = []
            for F in self.faces:
                result.append(F.position_line(G))

            return result
        else:
            return face.position_line(G)

    def position_plane(self, E: Plane, face: Face = None):
        if face is None:
            result = []
            for F in self.faces:
                result.append(F.position_plane(E))

            return result
        
        else:
            return face.position_plane(E)
        
    def position_face(self, F2: Face, face: Face = None):
        if face is None:
            result = []
            for F in self.faces:
                result.append(F.position_face(F2))

            return result
        
        else:
            return face.position_face(F2)
        
    def position_cube(self, W2: "Cube"):
        """
        on_edge
        on_face
        on_corner
        is_contained
        contains
        outside
        identical
        parallel
        intersecting
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
        result = []
        for F in self.faces:
            S = F.intersection_line(G)
            if S is not None:
                result.append(S)

        return result

    def intersection_plane(self, E: Plane):
        result = []
        for F in self.faces:
            result.append(F.intersection_plane(E))

        return result

    def intersection_face(self, F2: Face):
        result = []
        for F in self.faces:
            result.append(F.intersection_face(F2))

        return result

    # ======================================================================
    # Distance Calculations
    # ======================================================================

    def distance_point(self, Q):
        D = []
        for F in self.faces:
            D.append(F.distance_point(Q))

        return min(D)
    
    def distance_line(self, G: Line):
        D = []
        for F in self.faces:
            D.append(F.distance_line(G))

        return min(D)

    def distance_plane(self, E: Plane):
        D = []
        for F in self.faces:
            D.append(F.distance_plane(E))

        return min(D)
    
    def distance_face(self, F2):
        D = []
        for F in self.faces:
            D.append(F.distance_face(F2))

        return min(D)

    # ======================================================================
    # Transformations
    # ======================================================================

    def scale(self, factor):
        return Cube(self.p_min.scale(factor), self.p_max.scale(factor))

    def rotate(self, angle, axis):
        return Cube(self.p_min.rotate(angle, axis), self.p_max.rotate(angle, axis))

    def translate(self, v):
        return Cube(self.p_min.translate(v), self.p_max.translate(v))

    def reflect_on_point(self, P):
        return Cube(self.p_min.reflect_on_point(P), self.p_max.reflect_on_point(P))

    def reflect_on_line(self, g):
        return Cube(self.p_min.reflect_on_line(g), self.p_max.reflect_on_line(g))

    def reflect_on_plane(self, E):
        return Cube(self.p_min.reflect_on_plane(E), self.p_max.reflect_on_plane(E))
    
    # ======================================================================
    # Visualization
    # ======================================================================

    def draw_on_canvas(self, canvas, camera, **kwargs):
        faces_with_depth = []

        for face in self.faces:
            depth = face.get_depth(camera)
            faces_with_depth.append((depth, face))

        faces_with_depth.sort(key=lambda x: x[0], reverse=True)
        
        for _, face in faces_with_depth:
            face.draw_on_canvas(canvas, camera, **kwargs)
