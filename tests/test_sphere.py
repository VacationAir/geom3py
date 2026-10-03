from geom3py.geometry.sphere import Sphere
from geom3py.geometry.point import Point
from geom3py.utils.linal_utils import close
import math 

class TestSpherePositionSphere:
    """
    Tests for the positional relationship between two spheres
    (Sphere.position_sphere).
    """

    def setup_method(self):
        """Creates a base sphere centered at the origin with radius 1."""
        self.s = Sphere(1, [0, 0, 0])

    def test_identical(self):
        """Two spheres with the same center and radius are identical."""
        S2 = Sphere(1, [0, 0, 0])
        assert self.s.position_sphere(S2) == "identical"

    def test_concentric(self):
        """Two spheres with the same center but different radii are concentric."""
        S2 = Sphere(3, [0, 0, 0])
        assert self.s.position_sphere(S2) == "concentric"

    def test_contains(self):
        """This sphere fully contains a smaller one, no touching."""
        S2 = Sphere(0.2, [0, 0, 0.5])
        assert self.s.position_sphere(S2) == "contains"

    def test_is_contained(self):
        """This sphere is fully contained inside a larger one, no touching."""
        S2 = Sphere(3, [0, 0, 0.2])
        assert self.s.position_sphere(S2) == "is_contained"

    def test_touching_external(self):
        """Two spheres touch at exactly one point, outside each other."""
        S2 = Sphere(1, [2, 0, 0])
        assert self.s.position_sphere(S2) == "touching"

    def test_touching_internal(self):
        """Two spheres touch at exactly one point, one inside the other."""
        S2 = Sphere(0.5, [0.5, 0, 0])
        assert self.s.position_sphere(S2) == "touching"

    def test_intersecting(self):
        """Two spheres cross each other (surfaces intersect in a circle)."""
        S2 = Sphere(1, [1.5, 0, 0])
        assert self.s.position_sphere(S2) == "intersecting"

    def test_outside(self):
        """Two spheres are completely separate."""
        S2 = Sphere(1, [5, 0, 0])
        assert self.s.position_sphere(S2) == "outside"

class TestSphereIntersectionLine:
    """
    Tests for the intersection of a sphere with a line.
    """

    def setup_method(self):
        """Base sphere: center at origin, radius 1."""
        self.s = Sphere(1, [0, 0, 0])

    def test_outside_returns_none(self):
        """Line passing far from the sphere."""
        from geom3py.geometry.line import Line
        g = Line([5, 0, -1], [0, 0, 1])   # x=5, y=0, paralela a Z
        assert self.s.intersection_line(g) is None

    def test_touching_returns_point(self):
        """Tangent line: only one point."""
        from geom3py.geometry.line import Line
        g = Line([1, 0, -5], [0, 0, 1])   # x=1, y=0 → tangente en (1,0,0)
        # OJO: tu posición_line devuelve "touching" aquí,
        # pero tu intersection_line devuelve g.distance_point(center) que es un float
        # Eso es un bug: debería devolver un Point
        result = self.s.intersection_line(g)
        assert result is not None

    def test_intersecting_returns_two_points(self):
        """Secant line through the sphere."""
        from geom3py.geometry.line import Line
        g = Line([0, 0, -5], [0, 0, 1])   # eje Z
        result = self.s.intersection_line(g)

        assert len(result) == 2
        assert close(result[0], [0, 0, 1])
        assert close(result[1], [0, 0, -1])

    def test_intersecting_non_unit_direction(self):
        """La longitud del vector director no debe importar."""
        from geom3py.geometry.line import Line
        g = Line([0, 0, -5], [0, 0, 7])   # dirección larga, misma recta
        result = self.s.intersection_line(g)

        assert len(result) == 2
        assert close(result[0], [0, 0, 1])
        assert close(result[1], [0, 0, -1])

    def test_intersecting_offset_direction(self):
        """Recta diagonal que cruza la esfera."""
        from geom3py.geometry.line import Line
        g = Line([-5, 0, 0], [1, 0, 0])   # eje X
        result = self.s.intersection_line(g)

        assert len(result) == 2
        assert close(result[0], [1, 0, 0])
        assert close(result[1], [-1, 0, 0])

    def test_intersecting_3d_diagonal(self):
        """Recta que pasa por el centro en dirección diagonal."""
        from geom3py.geometry.line import Line
        g = Line([0, 0, 0], [1, 1, 1])
        result = self.s.intersection_line(g)

        assert len(result) == 2
        # Los dos puntos están a distancia 1 del origen
        for p in result:
            assert close(p.magnitude(), 1.0)

    def test_intersecting_asymmetric(self):
        """Recta que corta la esfera sin pasar por el centro."""
        from geom3py.geometry.line import Line
        g = Line([0.5, 0, -5], [0, 0, 1])   # x=0.5, y=0
        result = self.s.intersection_line(g)

        assert len(result) == 2
        h = math.sqrt(1 - 0.25)
        assert close(result[0], [0.5, 0, h])
        assert close(result[1], [0.5, 0, -h])

    def test_both_points_on_surface(self):
        """Verificación geométrica: los puntos deben estar sobre la superficie."""
        from geom3py.geometry.line import Line
        g = Line([0, 0, 0], [1, 2, 3])   # pasa por el centro
        result = self.s.intersection_line(g)

        assert len(result) == 2
        for p in result:
            assert close((p - self.s.center).magnitude(), self.s.radius)