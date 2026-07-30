from geom3py.geometry import Vector
from geom3py.geometry import Line
from geom3py.geometry import Point
from geom3py.geometry import Plane
from geom3py.geometry import Box
from geom3py.utils.linal_utils import close

class TestCubeTransformations:
    """
    Tests transformations of a cube with corner points
    P_min = (0,0,0) and P_max = (2,2,2).
    """

    def setup_method(self):
        """Creates a cube with edge length 2"""
        self.w = Box(
            [0, 0, 0],
            [2, 2, 2]
        )

    def test_scale(self):
        """Checks if the cube is scaled correctly"""
        scaled = self.w.scale(2)

        assert close(scaled.p_min, [0, 0, 0])
        assert close(scaled.p_max, [4, 4, 4])

    def test_rotate_around_z_axis(self):
        """Checks a rotation of 90 degrees around the z-axis"""
        rotated = self.w.rotate(90, "z")

        assert close(rotated.p_min, [0, 0, 0])
        assert close(rotated.p_max, [-2, 2, 2])

    def test_translate(self):
        """Checks a translation of the cube"""
        v = Vector(1, 2, 3)

        translated = self.w.translate(v)

        assert close(translated.p_min, [1, 2, 3])
        assert close(translated.p_max, [3, 4, 5])

    def test_reflect_on_point(self):
        """Checks point reflection at the origin"""
        P = Point([0, 0, 0])

        reflected = self.w.reflect_on_point(P)

        assert close(reflected.p_min, [0, 0, 0])
        assert close(reflected.p_max, [-2, -2, -2])

    def test_reflect_on_line(self):
        """Checks reflection about the x-axis"""
        g = Line(
            Point([0, 0, 0]),
            Vector(1, 0, 0)
        )

        reflected = self.w.reflect_on_line(g)

        assert close(reflected.p_min, [0, 0, 0])
        assert close(reflected.p_max, [2, -2, -2])

    def test_reflect_on_plane(self):
        """Checks reflection about the xy-plane"""
        E = Plane.from_parametric(
            Point([0, 0, 0]),
            Vector(1, 0, 0),
            Vector(0, 1, 0)
        )

        reflected = self.w.reflect_on_plane(E)

        assert close(reflected.p_min, [0, 0, 0])
        assert close(reflected.p_max, [2, 2, -2])