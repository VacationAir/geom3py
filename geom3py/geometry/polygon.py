from .point import Point
from .vector import Vector
from .line import Line
from .plane import Plane
from ..utils.linal_utils import close
from .triangulation import triangulate


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
    normal_vector : Vector
        Normal vector computed using Newell's method (works for coplanar
        and non-coplanar polygons).
    area : float or None
        Area if coplanar, None otherwise.
    is_convex : bool or None
        Whether the polygon is convex if coplanar, None otherwise.
    is_clockwise : bool or None
        Whether vertices are clockwise if coplanar, None otherwise.
    triangles : list of Triangle or None
        Triangulation of the polygon if coplanar, None otherwise.
    """
    
    def __init__(self, vertices):
        """
        Initializes a new polygon from a list of vertices.

        Parameters
        ----------
        vertices : list of array_like
            List of vertices in order (at least 3).

        Raises
        ------
        ValueError
            If fewer than 3 vertices are provided.
        """
        self.vertices = []
        for vertex in vertices:
            if not isinstance(vertex, Point):
                self.vertices.append(Point(vertex))
            else:
                self.vertices.append(vertex)

        # Basic properties
        self.n = len(self.vertices)
        self.edges = self._compute_edges()
        self.centroid = self._compute_centroid()
        self.perimeter = self._compute_perimeter()
        self.bounding_box = self._compute_bounding_box()
        self.is_coplanar = self._check_coplanarity()
        self.normal_vector = self._compute_newell_normal()

        # Extended properties
        if self.is_coplanar:
            self.area = self._compute_area()
            self.is_convex = self._compute_convexity()
            self.is_clockwise = self._compute_orientation()
        else:
            self.area = None
            self.is_convex = None
            self.is_clockwise = None

        self.triangles = self._compute_triangulation()

    # ======================================================================
    # Private compute methods
    # ======================================================================

    def _compute_edges(self):
        """
        Computes all edges of the polygon.

        Returns
        -------
        tuple of Line
            A tuple of Line objects connecting consecutive vertices.
        """
        edges = []
        for i in range(self.n):
            g = Line.from_points(self.vertices[i], self.vertices[(i + 1) % self.n])
            edges.append(g)
        return tuple(edges)

    def _compute_centroid(self):
        """
        Computes the centroid (average) of all vertices.

        Returns
        -------
        Point
            The centroid point.
        """
        x = sum(v.x for v in self.vertices) / self.n
        y = sum(v.y for v in self.vertices) / self.n
        z = sum(v.z for v in self.vertices) / self.n
        return Point(x, y, z)

    def _compute_perimeter(self):
        """
        Computes the perimeter of the polygon.

        Returns
        -------
        float
            The sum of all edge lengths.
        """
        perimeter = 0.0
        for e in self.edges:
            perimeter += e.direction_vector.magnitude()
        return perimeter

    def _compute_bounding_box(self):
        """
        Computes the axis-aligned bounding box.

        Returns
        -------
        dict
            A dictionary with 'min' and 'max' points.
        """
        vx = [v.x for v in self.vertices]
        vy = [v.y for v in self.vertices]
        vz = [v.z for v in self.vertices]
        return {
            "min": Point(min(vx), min(vy), min(vz)),
            "max": Point(max(vx), max(vy), max(vz))
        }

    def _check_coplanarity(self):
        """
        Checks if all vertices are coplanar.

        Returns
        -------
        bool
            True if all vertices lie in the same plane, False otherwise.
        """
        if self.n < 4:
            return True
        
        v0 = self.vertices[0]
        v1 = self.vertices[1]
        v2 = self.vertices[2]
        
        normal = (v1 - v0).cross(v2 - v0)
        if close(normal.magnitude(), 0):
            return False
        
        E = Plane(v0, normal)
        
        for i in range(3, self.n):
            if not E.contains_point(self.vertices[i]):
                return False
        
        return True

    def _compute_triangulation(self):
        """
        Computes the triangulation of the polygon.

        Returns
        -------
        list of Triangle or None
            List of triangles if coplanar, None otherwise.
        """
        return triangulate(self)

    def _compute_newell_normal(self):
        """
        Computes the normal vector using Newell's method.

        Newell's method works for both coplanar and non-coplanar polygons,
        making it more robust than the cross product method for arbitrary
        polygons.

        Returns
        -------
        Vector
            The normalized normal vector.
        """
        nx = ny = nz = 0.0
        n = len(self.vertices)
        for i in range(n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % n]
            nx += (v1.y - v2.y) * (v1.z + v2.z)
            ny += (v1.z - v2.z) * (v1.x + v2.x)
            nz += (v1.x - v2.x) * (v1.y + v2.y)

        return Vector(nx, ny, nz).normalize()
    
    def _compute_area(self):
        """
        Computes the area of the polygon.

        Returns
        -------
        float
            The area of the polygon.

        Notes
        -----
        Uses the 3D polygon area formula: area = 0.5 * |sum(v_i x v_{i+1})|
        """
        area_vector = Vector(0, 0, 0)
        for i in range(self.n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % self.n]
            area_vector += v1.cross(v2)
        return abs(area_vector.magnitude()) / 2

    def _compute_convexity(self):
        """
        Checks if the polygon is convex.

        Returns
        -------
        bool
            True if the polygon is convex, False otherwise.
        """
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
        """
        Determines if vertices are ordered clockwise or counterclockwise.

        Returns
        -------
        bool
            True if vertices are ordered clockwise, False otherwise.
        """
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
            Styling options:
            - fill : str
                Fill color of the polygon (default: '#96FF9B')
            - outline : str
                Outline color of the polygon (default: 'green')
            - width : int
                Width of the outline in pixels (default: 2)

        Returns
        -------
        None

        Notes
        -----
        If any vertex is behind the camera (projection returns None),
        the polygon is not drawn.
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

        Parameters
        ----------
        camera : Camera
            The camera for depth calculation.

        Returns
        -------
        float
            The depth (Z-coordinate) of the polygon's centroid in camera space.

        Notes
        -----
        This is used for z-ordering when rendering multiple objects.
        Objects with larger depth values are drawn first (farther away).
        """
        projected = camera.remapping(self.centroid)
        return projected.z

    # ======================================================================
    # Representation
    # ======================================================================

    def __repr__(self):
        """
        Returns a readable string representation of the polygon.

        Returns
        -------
        str
            A string representation of the polygon.
        """
        status = "coplanar" if self.is_coplanar else "non-coplanar"
        area_str = f", area={self.area:.2f}" if self.is_coplanar and self.area is not None else ""
        return f"Polygon({self.n} vertices, {status}{area_str})"