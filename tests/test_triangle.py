import pytest
import math
from geom3py.geometry.triangle import Triangle
from geom3py.geometry.point import Point
from geom3py.geometry.vector import Vector
from geom3py.geometry.plane import Plane

class TestTriangleContainsPoint:
    """Tests para el método contains_point de Triangle"""
    
    @pytest.fixture
    def triangle_2d_xy(self):
        """Triángulo en el plano XY: (0,0,0), (2,0,0), (0,2,0)"""
        return Triangle(
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(0, 2, 0)
        )
    
    @pytest.fixture
    def triangle_3d(self):
        """Triángulo en 3D: (1,0,0), (0,1,0), (0,0,1)"""
        return Triangle(
            Point(1, 0, 0),
            Point(0, 1, 0),
            Point(0, 0, 1)
        )
    
    @pytest.fixture
    def triangle_large(self):
        """Triángulo grande para tests de escala"""
        return Triangle(
            Point(-5, -5, 0),
            Point(5, -5, 0),
            Point(0, 5, 0)
        )

    # ============================================================
    # Tests para puntos DENTRO del triángulo
    # ============================================================
    
    def test_centroid_is_inside(self, triangle_2d_xy):
        """El centroide siempre debe estar dentro"""
        Q = Point(2/3, 2/3, 0)  # Centroide del triángulo
        assert triangle_2d_xy.contains_point(Q) == True
    
    def test_point_on_vertex_is_inside(self, triangle_2d_xy):
        """Los vértices deben considerarse dentro"""
        assert triangle_2d_xy.contains_point(Point(0, 0, 0)) == True
        assert triangle_2d_xy.contains_point(Point(2, 0, 0)) == True
        assert triangle_2d_xy.contains_point(Point(0, 2, 0)) == True
    
    def test_point_on_edge_is_inside(self, triangle_2d_xy):
        """Los puntos en las aristas deben considerarse dentro"""
        # Punto en el lado AB (entre 0,0 y 2,0)
        assert triangle_2d_xy.contains_point(Point(1, 0, 0)) == True
        # Punto en el lado BC (entre 2,0 y 0,2)
        assert triangle_2d_xy.contains_point(Point(1, 1, 0)) == True
        # Punto en el lado CA (entre 0,2 y 0,0)
        assert triangle_2d_xy.contains_point(Point(0, 1, 0)) == True
    
    def test_point_inside_near_edge(self, triangle_2d_xy):
        """Puntos justo dentro cerca de las aristas"""
        # Cerca del lado AB (y = 0.1)
        assert triangle_2d_xy.contains_point(Point(0.5, 0.1, 0)) == True
        # Cerca del lado BC (x + y ≈ 2)
        assert triangle_2d_xy.contains_point(Point(0.9, 1.1, 0)) == True
        # Cerca del lado CA (x = 0.1)
        assert triangle_2d_xy.contains_point(Point(0.1, 0.5, 0)) == True
    
    def test_random_inside_points(self, triangle_2d_xy):
        """Varios puntos aleatorios dentro del triángulo"""
        inside_points = [
            (0.5, 0.5, 0),    # Centro aproximado
            (1.5, 0.3, 0),    # Cerca de la base
            (0.3, 1.5, 0),    # Cerca del lado izquierdo
            (1.0, 0.8, 0),    # En el interior
            (0.8, 0.6, 0)     # En el interior
        ]
        for x, y, z in inside_points:
            assert triangle_2d_xy.contains_point(Point(x, y, z)) == True
    
    def test_points_inside_3d_triangle(self, triangle_3d):
        """Puntos dentro del triángulo en 3D"""
        inside_points = [
            (1/3, 1/3, 1/3),  # Centroide
            (0.5, 0.25, 0.25),
            (0.25, 0.5, 0.25),
            (0.25, 0.25, 0.5)
        ]
        for x, y, z in inside_points:
            assert triangle_3d.contains_point(Point(x, y, z)) == True

    # ============================================================
    # Tests para puntos FUERA del triángulo
    # ============================================================
    
    def test_points_outside_clearly(self, triangle_2d_xy):
        """Puntos claramente fuera del triángulo"""
        outside_points = [
            (3, 0, 0),    # A la derecha
            (0, 3, 0),    # Arriba
            (-1, 0, 0),   # A la izquierda
            (0, -1, 0),   # Abajo
            (3, 3, 0),    # Diagonal fuera
            (-1, -1, 0)   # Diagonal fuera
        ]
        for x, y, z in outside_points:
            assert triangle_2d_xy.contains_point(Point(x, y, z)) == False
    
    def test_points_outside_by_edge(self, triangle_2d_xy):
        """Puntos justo fuera de cada arista"""
        # Fuera del lado AB (y < 0)
        assert triangle_2d_xy.contains_point(Point(1, -0.1, 0)) == False
        # Fuera del lado BC (x + y > 2)
        assert triangle_2d_xy.contains_point(Point(1.5, 0.6, 0)) == False
        # Fuera del lado CA (x < 0)
        assert triangle_2d_xy.contains_point(Point(-0.1, 0.5, 0)) == False
    
    def test_points_outside_3d_triangle(self, triangle_3d):
        """Puntos fuera del triángulo en 3D"""
        outside_points = [
            (2, 0, 0),    # Extendido en x
            (0, 2, 0),    # Extendido en y
            (0, 0, 2),    # Extendido en z
            (-1, 0, 0),   # Negativo en x
            (0, -1, 0),   # Negativo en y
            (0, 0, -1)    # Negativo en z
        ]
        for x, y, z in outside_points:
            assert triangle_3d.contains_point(Point(x, y, z)) == False
    
    def test_points_outside_but_in_plane(self, triangle_2d_xy):
        """Puntos en el mismo plano pero fuera del triángulo"""
        # Todos en z=0 (el plano del triángulo)
        outside_points = [
            (2.5, 0, 0),
            (0, 2.5, 0),
            (1.5, 1.5, 0),
            (-0.5, 1, 0),
            (1, -0.5, 0),
            (2, 0.5, 0)
        ]
        for x, y, z in outside_points:
            assert triangle_2d_xy.contains_point(Point(x, y, z)) == False
    
    def test_large_triangle(self, triangle_large):
        """Tests con un triángulo más grande"""
        # Dentro
        assert triangle_large.contains_point(Point(0, 0, 0)) == True
        assert triangle_large.contains_point(Point(2, 0, 0)) == True
        assert triangle_large.contains_point(Point(-2, 0, 0)) == True
        
        # En bordes (puntos que SÍ están en la base)
        assert triangle_large.contains_point(Point(-5, -5, 0)) == True  # Vértice
        assert triangle_large.contains_point(Point(5, -5, 0)) == True   # Vértice
        assert triangle_large.contains_point(Point(0, -5, 0)) == True   # Centro de la base
        assert triangle_large.contains_point(Point(0, 5, 0)) == True    # Vértice superior
        
        # Puntos en las aristas laterales
        # Arista izquierda: de (-5,-5) a (0,5) - el punto medio es (-2.5, 0)
        assert triangle_large.contains_point(Point(-2.5, 0, 0)) == True
        # Arista derecha: de (5,-5) a (0,5) - el punto medio es (2.5, 0)
        assert triangle_large.contains_point(Point(2.5, 0, 0)) == True
        
        # Fuera (puntos que NO están en el triángulo)
        assert triangle_large.contains_point(Point(6, 0, 0)) == False    # Fuera a la derecha
        assert triangle_large.contains_point(Point(-6, 0, 0)) == False   # Fuera a la izquierda
        assert triangle_large.contains_point(Point(0, 6, 0)) == False    # Fuera arriba
        assert triangle_large.contains_point(Point(0, -6, 0)) == False   # Fuera abajo
        assert triangle_large.contains_point(Point(5, 0, 0)) == False    # ¡Está fuera!
        assert triangle_large.contains_point(Point(-5, 0, 0)) == False   # ¡Está fuera!
        assert triangle_large.contains_point(Point(4, 4, 0)) == False    # Fuera dentro de la zona

    # ============================================================
    # Tests para casos especiales
    # ============================================================
    
    def test_point_not_in_plane(self, triangle_2d_xy):
        """Puntos que no están en el plano del triángulo deben dar False"""
        # Punto con z diferente (el triángulo está en z=0)
        assert triangle_2d_xy.contains_point(Point(0.5, 0.5, 1)) == False
        assert triangle_2d_xy.contains_point(Point(0.5, 0.5, -1)) == False
    
    def test_point_exactly_on_vertex_with_z(self, triangle_3d):
        """Vértices en 3D deben considerarse dentro"""
        assert triangle_3d.contains_point(Point(1, 0, 0)) == True
        assert triangle_3d.contains_point(Point(0, 1, 0)) == True
        assert triangle_3d.contains_point(Point(0, 0, 1)) == True
    
    def test_point_on_edge_of_3d_triangle(self, triangle_3d):
        """Puntos en las aristas del triángulo 3D"""
        # Arista entre (1,0,0) y (0,1,0): punto medio (0.5, 0.5, 0)
        assert triangle_3d.contains_point(Point(0.5, 0.5, 0)) == True
        # Arista entre (0,1,0) y (0,0,1): punto medio (0, 0.5, 0.5)
        assert triangle_3d.contains_point(Point(0, 0.5, 0.5)) == True
        # Arista entre (0,0,1) y (1,0,0): punto medio (0.5, 0, 0.5)
        assert triangle_3d.contains_point(Point(0.5, 0, 0.5)) == True
    
    def test_symmetry(self, triangle_2d_xy):
        """El método debe ser simétrico (punto dentro del triángulo)"""
        Q = Point(0.5, 0.5, 0)
        assert triangle_2d_xy.contains_point(Q) == True
        # El mismo punto debe dar True siempre
        assert triangle_2d_xy.contains_point(Q) == True
    
    def test_points_very_close_to_edge(self, triangle_2d_xy):
        """Puntos muy cerca de las aristas (prueba de tolerancia numérica)"""
        # Muy cerca del lado AB (y = 1e-9, prácticamente en la arista)
        assert triangle_2d_xy.contains_point(Point(1, 1e-10, 0)) == True
        # Muy cerca del lado BC (x + y ≈ 2)
        assert triangle_2d_xy.contains_point(Point(1.5, 0.5 - 1e-10, 0)) == True
    
    def test_origin_with_offset_triangle(self):
        """Triángulo que no contiene el origen"""
        triangle = Triangle(
            Point(1, 1, 0),
            Point(3, 1, 0),
            Point(2, 3, 0)
        )
        # El origen está fuera
        assert triangle.contains_point(Point(0, 0, 0)) == False
        # Centroide dentro
        assert triangle.contains_point(Point(2, 5/3, 0)) == True

    # ============================================================
    # Tests de regresión y casos límite
    # ============================================================
    
    def test_consecutive_calls(self, triangle_2d_xy):
        """Múltiples llamadas al mismo punto deben dar el mismo resultado"""
        Q = Point(0.5, 0.5, 0)
        result1 = triangle_2d_xy.contains_point(Q)
        result2 = triangle_2d_xy.contains_point(Q)
        result3 = triangle_2d_xy.contains_point(Q)
        assert result1 == result2 == result3
    
    def test_small_but_valid_triangle(self):
        """Triángulo pequeño pero válido (prueba de precisión numérica)"""
        # Usar 1e-3 en lugar de 1e-6 para evitar problemas de precisión
        triangle = Triangle(
            Point(0, 0, 0),
            Point(1e-3, 0, 0),
            Point(0, 1e-3, 0)
        )
        # Centro del triángulo (dentro)
        Q = Point(1e-3/3, 1e-3/3, 0)
        assert triangle.contains_point(Q) == True
        
        # Punto dentro pero cerca de la arista
        Q = Point(1e-4, 1e-4, 0)
        assert triangle.contains_point(Q) == True
        
        # Punto fuera
        Q = Point(2e-3, 2e-3, 0)
        assert triangle.contains_point(Q) == False
    
    def test_numeric_stability(self):
        """Prueba de estabilidad numérica con valores grandes"""
        triangle = Triangle(
            Point(1000, 1000, 0),
            Point(1002, 1000, 0),
            Point(1000, 1002, 0)
        )
        # Punto dentro
        assert triangle.contains_point(Point(1001, 1001, 0)) == True
        # Punto fuera
        assert triangle.contains_point(Point(1003, 1000, 0)) == False
        assert triangle.contains_point(Point(1000, 1003, 0)) == False

    # ============================================================
    # Tests con diferentes orientaciones
    # ============================================================
    
    def test_triangle_in_other_planes(self):
        """Triángulos en diferentes planos"""
        # Plano XZ
        triangle_xz = Triangle(
            Point(0, 0, 0),
            Point(2, 0, 0),
            Point(0, 0, 2)
        )
        assert triangle_xz.contains_point(Point(0.5, 0, 0.5)) == True
        assert triangle_xz.contains_point(Point(0.5, 1, 0.5)) == False  # Fuera del plano
        
        # Plano YZ
        triangle_yz = Triangle(
            Point(0, 0, 0),
            Point(0, 2, 0),
            Point(0, 0, 2)
        )
        assert triangle_yz.contains_point(Point(0, 0.5, 0.5)) == True
        assert triangle_yz.contains_point(Point(1, 0.5, 0.5)) == False  # Fuera del plano
    
    def test_rotated_triangle(self):
        """Triángulo rotado (prueba de orientación)"""
        # Triángulo rotado 45 grados en XY
        import math
        angle = math.radians(45)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        triangle = Triangle(
            Point(0, 0, 0),
            Point(2*cos_a, 2*sin_a, 0),
            Point(-2*sin_a, 2*cos_a, 0)
        )
        # El centroide debe estar dentro
        centroid = Point(
            (0 + 2*cos_a - 2*sin_a)/3,
            (0 + 2*sin_a + 2*cos_a)/3,
            0
        )
        assert triangle.contains_point(centroid) == True

    # ============================================================
    # Tests para triángulos degenerados - AHORA MANEJADOS CORRECTAMENTE
    # ============================================================
    
    def test_degenerate_triangle_raises_error(self):
        """Triángulo degenerado (puntos colineales) debe lanzar ValueError"""
        with pytest.raises(ValueError, match="Normal vector must not be the zero vector"):
            Triangle(
                Point(0, 0, 0),
                Point(1, 0, 0),
                Point(2, 0, 0)
            )

if __name__ == "__main__":
    pytest.main([__file__, "-v"])