from .point import Point
from .vector import Vector
from .line import Line
from .plane import Plane

class Polygon:
    """
    Represents a polygon in 3D space.
    
    Can be coplanar (all vertices in the same plane) or non-coplanar.
    If coplanar, all geometric properties (area, normal, etc.) are available.
    If non-coplanar, it behaves as a 3D polyline/loop with basic operations.

    Parameters
    ----------
    vertices : list of array_like
        List of vertices in order (at least 3).

    Attributes
    ----------
    vertices : tuple of Point
        The vertices of the polygon.
    edges : tuple of Line
        The edges connecting consecutive vertices.
    centroid : Point
        Geometric center (average of vertices).
    perimeter : float
        Perimeter of the polygon.
    bounding_box : dict
        Axis-aligned bounding box with 'min' and 'max' points.
    is_coplanar : bool
        Whether all vertices lie in the same plane.
    normal_vector : Vector or None
        Normal vector if coplanar, None otherwise.
    area : float or None
        Area if coplanar, None otherwise.
    is_convex : bool or None
        Whether the polygon is convex if coplanar, None otherwise.
    is_clockwise : bool or None
        Whether vertices are clockwise if coplanar, None otherwise.
    """
    
    def __init__(self, n_vertex):
                
        self.vertices = []
        for vertex in n_vertex:
            if not isinstance(vertex, Point):
                self.vertices.append(Point(vertex))

            else:
                self.vertices.append(vertex)

        if len(self.vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")

        # Basic properties
        self.n = len(self.vertices)
        self.edges = self._compute_edges()
        self.centroid = self._compute_centroid()
        self.perimeter = self._compute_perimeter()
        self.bounding_box = self._compute_bounding_box()
        self.is_coplanar = self._check_coplanarity()

        # Extended properties
        if self.is_coplanar:
            self.normal_vector = self._compute_normal()
            self.area = self._compute_area()
            self.is_convex = self._compute_convexity()
            self.is_clockwise = self._compute_orientation()
        else:
            self.normal = None
            self.area = None
            self.is_convex = None
            self.is_clockwise = None

    # ======================================================================
    # Private compute methods
    # ======================================================================

    def _compute_edges(self):
        edges = []

        for i in range(self.n):
            g = Line.from_points(self.vertices[i], self.vertices[(i+1) % self.n])
            edges.append(g)

        return tuple(edges)

    def _compute_centroid(self):
        x = sum(v.x for v in self.vertices) / self.n
        y = sum(v.y for v in self.vertices) / self.n
        z = sum(v.z for v in self.vertices) / self.n

        return Point(x, y, z)

    def _compute_perimeter(self):
        perimeter = 0
        for e in self.edges:
            perimeter += e.direction_vector.magnitude()

        return perimeter

    def _compute_bounding_box(self):
        vx = [v.x for v in self.vertices]
        vy = [v.y for v in self.vertices]
        vz = [v.z for v in self.vertices]

        return{
            "min": Point(min(vx), min(vy), min(vz)),
            "max": Point(max(vx), max(vy), max(vz))
        }

    def _check_coplanarity(self):
        E = Plane.from_parametric((self.edges[0]).support_vector, (self.edges[0]).direction_vector, (self.edges[1]).direction_vector)

        for e in self.edges:
            if E.position_line(e) != "identical":
                return False

        return True

    def _compute_normal(self):
        norm_vector = (self.edges[0]).direction_vector.cross((self.edges[1]).direction_vector)

        return norm_vector
    
    def _compute_area(self):
        area_vector = Vector(0, 0, 0)
        
        for i in range(self.n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % self.n]
            area_vector += v1.cross(v2)
        
        return abs(area_vector.magnitude()) / 2

    def _compute_convexity(self):
        if self.n < 4:
            return True
        
        signs = []
        for i in range(self.n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % self.n]
            v3 = self.vertices[(i + 2) % self.n]
            
            cross = (v2 - v1).cross(v3 - v2)
            dot = cross.dot(self.normal_vector)
            signs.append(1 if dot > 0 else -1 if dot < 0 else 0)
        
        has_positive = any(s > 0 for s in signs)
        has_negative = any(s < 0 for s in signs)
        return not (has_positive and has_negative)

    def _compute_orientation(self):
        signed_area = 0.0
        for i in range(self.n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % self.n]
            signed_area += v1.x * v2.y - v2.x * v1.y
        
        return signed_area < 0

    # ======================================================================
    # Visualization
    # ======================================================================

    def draw_on_canvas(self, canvas, camera, **kwargs):
        """
        Draws the polygon on a Tkinter canvas.

        Parameters
        ----------
        canvas : tk.Canvas
            The canvas to draw on.
        camera : Camera
            The camera for 3D to 2D projection.
        **kwargs : dict
            Styling options: fill, outline, width.
        """
        points_2d = []
        for p in self.vertices:
            x, y = camera.project(p)
            if x is None or y is None:
                return
            
            points_2d.extend([x, y])
        
        fill_color = kwargs.get('fill', '#96FF9B')
        outline_color = kwargs.get('outline', 'green')
        width = kwargs.get('width', 2)
        
        canvas.create_polygon(
            points_2d,
            fill=fill_color,
            outline=outline_color,
            width=width,
            tags=('polygon',)
        )

    def get_depth(self, camera):
        """
        Calculates the depth of the polygon with respect to the camera.
        Uses the average depth of all edges for better accuracy.
        """
        projected = camera.remapping(self.centroid)
        return projected.z
