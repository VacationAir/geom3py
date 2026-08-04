"""
Tests para la clase Polygon y su triangulación.
"""
import pytest
import math
from geom3py.geometry.point import Point
from geom3py.geometry.vector import Vector
from geom3py.geometry.line import Line
from geom3py.geometry.polygon import Polygon
from geom3py.geometry.triangle import Triangle
from geom3py.geometry.triangulation import triangulate

class TestPolygonBasic:
    """Tests básicos para la creación y propiedades de Polygon."""
    
    def test_create_triangle(self):
        """Crear un polígono de 3 vértices (triángulo)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(1, 0, 0),
            Point(0, 1, 0)
        ])
        
        assert poly.n == 3
        assert poly.is_coplanar == True
        assert poly.area == 0.5
        assert poly.perimeter == 2 + math.sqrt(2)  # 1 + 1 + sqrt(2)
        assert poly.is_convex == True
        assert poly.triangles is not None
        assert len(poly.triangles) == 1
    
    def test_create_quadrilateral(self):
        """Crear un polígono de 4 vértices (cuadrilátero)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(2, 2, 0),
            Point(0, 2, 0)
        ])
        
        assert poly.n == 4
        assert poly.is_coplanar == True
        assert poly.area == 4.0
        assert poly.perimeter == 8.0
        assert poly.is_convex == True
        assert len(poly.triangles) == 2  # Triangulación: 2 triángulos
    
    def test_create_pentagon(self):
        """Crear un polígono de 5 vértices (pentágono)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(3, 1, 0),
            Point(2, 2, 0),
            Point(0, 2, 0)
        ])
        
        assert poly.n == 5
        assert poly.is_coplanar == True
        assert poly.is_convex == True
        assert len(poly.triangles) == 3  # Pentágono → 3 triángulos
    
    def test_create_non_coplanar_polygon(self):
        """Crear un polígono no coplanar."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(1, 0, 0),
            Point(1, 1, 0),
            Point(0, 0, 1)  # Este punto rompe la coplanaridad
        ])
        
        assert poly.n == 4
        assert poly.is_coplanar == False
        assert poly.area is None
        assert poly.is_convex is None
        assert poly.is_clockwise is None
        assert poly.normal_vector is not None
    
    def test_create_polygon_with_lists(self):
        """Crear polígono usando listas en lugar de Points."""
        poly = Polygon([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0]
        ])
        
        assert poly.n == 3
        assert isinstance(poly.vertices[0], Point)
        assert poly.vertices[0].x == 0
        assert poly.vertices[0].y == 0
        assert poly.vertices[0].z == 0
    
    def test_create_polygon_with_mixed_types(self):
        """Crear polígono con tipos mixtos (Points y listas)."""
        poly = Polygon([
            Point(0, 0, 0),
            [1, 0, 0],
            Point(0, 1, 0)
        ])
        
        assert poly.n == 3
        assert all(isinstance(v, Point) for v in poly.vertices)


class TestPolygonProperties:
    """Tests para las propiedades calculadas de Polygon."""
    
    def test_centroid(self):
        """Calcular el centroide de un polígono."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(2, 2, 0),
            Point(0, 2, 0)
        ])
        
        centroid = poly.centroid
        assert centroid.x == 1.0
        assert centroid.y == 1.0
        assert centroid.z == 0.0
    
    def test_bounding_box(self):
        """Calcular la bounding box de un polígono."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(3, -1, 0),
            Point(2, 4, 0),
            Point(-1, 2, 0)
        ])
        
        bbox = poly.bounding_box
        assert bbox["min"].x == -1.0
        assert bbox["min"].y == -1.0
        assert bbox["min"].z == 0.0
        assert bbox["max"].x == 3.0
        assert bbox["max"].y == 4.0
        assert bbox["max"].z == 0.0
    
    def test_normal_vector_coplanar(self):
        """Calcular el vector normal de un polígono coplanar."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(0, 2, 0)
        ])
        
        normal = poly.normal_vector
        assert normal.z > 0  # Debe apuntar hacia arriba
        assert abs(normal.magnitude() - 1.0) < 1e-10  # Normalizado
    
    def test_newell_normal_non_coplanar(self):
        """Calcular la normal de Newell para polígono no coplanar."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(1, 0, 0),
            Point(1, 1, 0),
            Point(0, 0, 1)
        ])
        
        normal = poly.normal_vector
        assert normal is not None
        assert abs(normal.magnitude() - 1.0) < 1e-10  # Normalizado


class TestPolygonConvexity:
    """Tests para la convexidad de polígonos."""
    
    def test_convex_triangle(self):
        """Un triángulo siempre es convexo."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(0, 2, 0)
        ])
        assert poly.is_convex == True
    
    def test_convex_quadrilateral(self):
        """Un cuadrado es convexo."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(2, 2, 0),
            Point(0, 2, 0)
        ])
        assert poly.is_convex == True
    
    def test_concave_polygon(self):
        """Un polígono cóncavo (forma de L)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(3, 0, 0),
            Point(3, 1, 0),
            Point(1, 1, 0),
            Point(1, 3, 0),
            Point(0, 3, 0)
        ])
        assert poly.is_convex == False
    
    def test_clockwise_orientation(self):
        """Polígono orientado en sentido horario."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(0, 2, 0),   # Orden horario
            Point(2, 2, 0),
            Point(2, 0, 0)
        ])
        assert poly.is_clockwise == True
    
    def test_counterclockwise_orientation(self):
        """Polígono orientado en sentido antihorario."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),   # Orden antihorario
            Point(2, 2, 0),
            Point(0, 2, 0)
        ])
        assert poly.is_clockwise == False


class TestPolygonTriangulation:
    """Tests específicos para la triangulación de polígonos."""
    
    def test_triangulate_triangle(self):
        """Triangulación de un triángulo (caso base)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(0, 2, 0)
        ])
        
        triangles = poly.triangles
        assert len(triangles) == 1
        assert isinstance(triangles[0], Triangle)
        assert triangles[0].area() == 2.0  # 0.5 * 2 * 2 = 2
    
    def test_triangulate_square(self):
        """Triangulación de un cuadrado (2 triángulos)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(2, 2, 0),
            Point(0, 2, 0)
        ])
        
        triangles = poly.triangles
        assert len(triangles) == 2
        assert all(isinstance(t, Triangle) for t in triangles)
        
        # Suma de áreas debe ser igual al área del cuadrado
        total_area = sum(t.area() for t in triangles)
        assert abs(total_area - poly.area) < 1e-10
    
    def test_triangulate_pentagon(self):
        """Triangulación de un pentágono (3 triángulos)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(3, 1, 0),
            Point(2, 2, 0),
            Point(0, 2, 0)
        ])
        
        triangles = poly.triangles
        assert len(triangles) == 3
        assert all(isinstance(t, Triangle) for t in triangles)
        
        # Suma de áreas debe ser igual al área del pentágono
        total_area = sum(t.area() for t in triangles)
        assert abs(total_area - poly.area) < 1e-10
    
    def test_triangulate_hexagon(self):
        """Triangulación de un hexágono (4 triángulos)."""
        hexagon_vertices = []
        for i in range(6):
            angle = 2 * math.pi * i / 6
            x = math.cos(angle)
            y = math.sin(angle)
            hexagon_vertices.append(Point(x, y, 0))
        
        poly = Polygon(hexagon_vertices)
        triangles = poly.triangles
        
        assert len(triangles) == 4  # Hexágono → 4 triángulos
        assert all(isinstance(t, Triangle) for t in triangles)
        
        # Suma de áreas debe ser igual al área del hexágono
        total_area = sum(t.area() for t in triangles)
        assert abs(total_area - poly.area) < 1e-10
    
    def test_triangulate_concave_polygon(self):
        """Triangulación de un polígono cóncavo."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(3, 0, 0),
            Point(3, 1, 0),
            Point(1, 1, 0),
            Point(1, 3, 0),
            Point(0, 3, 0)
        ])
        
        triangles = poly.triangles
        # Para un polígono de 6 vértices → 4 triángulos
        assert len(triangles) == 4
        assert all(isinstance(t, Triangle) for t in triangles)
        
        # Suma de áreas debe ser igual al área del polígono
        total_area = sum(t.area() for t in triangles)
        assert abs(total_area - poly.area) < 1e-10
    
    def test_triangulate_star_shape(self):
        """Triangulación de una estrella (polígono cóncavo complejo)."""
        # Estrella de 5 puntas
        star_points = []
        for i in range(10):
            angle = 2 * math.pi * i / 10
            radius = 2.0 if i % 2 == 0 else 0.8
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            star_points.append(Point(x, y, 0))
        
        poly = Polygon(star_points)
        triangles = poly.triangles
        
        # Para 10 vértices → 8 triángulos
        assert len(triangles) == 8
        assert all(isinstance(t, Triangle) for t in triangles)
        
        # Verificar que la suma de áreas es correcta
        total_area = sum(t.area() for t in triangles)
        assert abs(total_area - poly.area) < 1e-9
    
    def test_triangulation_preserves_area(self):
        """La triangulación debe preservar el área total."""
        # Probar con varios polígonos aleatorios
        import random
        random.seed(42)
        
        for _ in range(5):
            # Generar polígono aleatorio en el plano XY
            n = random.randint(4, 10)
            vertices = []
            for i in range(n):
                angle = 2 * math.pi * i / n + random.uniform(-0.1, 0.1)
                radius = random.uniform(1, 3)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                vertices.append(Point(x, y, 0))
            
            poly = Polygon(vertices)
            triangles = poly.triangles
            
            total_area = sum(t.area() for t in triangles)
            assert abs(total_area - poly.area) < 1e-9
    
    def test_triangulate_3d_coplanar_polygon(self):
        """Triangulación de un polígono coplanar en 3D."""
        # Triángulo en el plano XZ
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(0, 0, 2)
        ])
        
        triangles = poly.triangles
        assert len(triangles) == 1
        assert triangles[0].area() == 2.0
    
    def test_triangulate_3d_rotated_polygon(self):
        """Triangulación de un polígono rotado en 3D."""
        # Cuadrado en un plano inclinado
        import math
        angle = math.radians(45)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        poly = Polygon([
            Point(0, 0, 0),
            Point(2*cos_a, 2*sin_a, 0),
            Point(2*cos_a - 2*sin_a, 2*sin_a + 2*cos_a, 0),
            Point(-2*sin_a, 2*cos_a, 0)
        ])
        
        triangles = poly.triangles
        assert len(triangles) == 2
        
        total_area = sum(t.area() for t in triangles)
        assert abs(total_area - poly.area) < 1e-10

class TestPolygonIntegration:
    """Tests de integración con otras clases."""
    
    def test_polygon_to_triangles(self):
        """Convertir polígono a triángulos y usar métodos de Triangle."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(0, 2, 0)
        ])
        
        triangles = poly.triangles
        tri = triangles[0]
        
        # Usar métodos de Triangle
        assert tri.area() == 2.0
        assert tri.perimeter() == 2 + math.sqrt(8) + 2 # 2 + 2*sqrt(2)
        assert tri.contains_point(Point(0.5, 0.5, 0)) == True
        assert tri.contains_point(Point(1.5, 1.5, 0)) == False
    
    def test_polygon_area_from_triangles(self):
        """Calcular área del polígono a partir de sus triángulos."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(3, 0, 0),
            Point(3, 2, 0),
            Point(1, 2, 0),
            Point(1, 1, 0),
            Point(0, 1, 0)
        ])
        
        triangles = poly.triangles
        area_from_triangles = sum(t.area() for t in triangles)
        
        assert abs(area_from_triangles - poly.area) < 1e-10
    
    def test_draw_polygon(self):
        """Verificar que draw_on_canvas existe (sin ejecutar realmente)."""
        poly = Polygon([
            Point(0, 0, 0),
            Point(1, 0, 0),
            Point(0, 1, 0)
        ])
        
        # Verificar que el método existe
        assert hasattr(poly, 'draw_on_canvas')
        assert callable(poly.draw_on_canvas)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])