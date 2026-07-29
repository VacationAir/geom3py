from geom3py.geometry.vector import Vector
from geom3py.geometry.line import Line
from geom3py.geometry.plane import Plane
from geom3py.utils.linal_utils import close


class TestVector:

    def test_scale(self):
        """Tests vector scaling"""
        v = Vector([1, 2, 3])

        assert close(v.scale(2), [2, 4, 6])
        assert close(v.scale(-1), [-1, -2, -3])
        assert close(v.scale(0), [0, 0, 0])

    def test_translate(self):
        """Tests vector translation"""
        v = Vector([1, 2, 3])

        assert close(v.translate(Vector([4, 5, 6])), Vector([5, 7, 9]))
        assert close(v.translate(Vector([-1, -2, -3])), Vector([0, 0, 0]))

    def test_rotate_x(self):
        """Tests rotation around the x-axis"""
        v = Vector([0, 1, 0])

        assert close(v.rotate(90, "x"), [0, 0, 1])

    def test_rotate_y(self):
        """Tests rotation around the y-axis"""
        v = Vector([0, 0, 1])

        assert close(v.rotate(90, "y"), [1, 0, 0])

    def test_rotate_z(self):
        """Tests rotation around the z-axis"""
        v = Vector([1, 0, 0])

        assert close(v.rotate(90, "z"), [0, 1, 0])

    def test_reflect_on_point(self):
        """Tests reflection of a vector about a point"""
        v = Vector([1, 2, 3])

        assert close(
            v.reflect_on_point(Vector([0, 0, 0])),
            [-1, -2, -3]
        )

        assert close(
            v.reflect_on_point(Vector([1, 1, 1])),
            [1, 0, -1]
        )

    def test_reflect_on_line(self):
        """Tests reflection of a vector about a line"""
        g = Line([0, 0, 0], [1, 0, 0])

        assert close(
            Vector([1, 2, 0]).reflect_on_line(g),
            [1, -2, 0]
        )

        assert close(
            Vector([3, 0, 0]).reflect_on_line(g),
            [3, 0, 0]
        )

    def test_reflect_on_plane(self):
        """Tests reflection of a vector about a plane"""
        E = Plane([0, 0, 0], [0, 0, 1])

        assert close(
            Vector([1, 2, 3]).reflect_on_plane(E),
            [1, 2, -3]
        )

        assert close(
            Vector([4, 5, 0]).reflect_on_plane(E),
            [4, 5, 0]
        )

    def test_rotation_preserves_length(self):
        """A rotation preserves the magnitude of a vector"""
        v = Vector([1, 2, 3])

        assert close(
            v.magnitude(),
            v.rotate(123, "x").magnitude()
        )

    def test_double_reflection_point(self):
        """Double point reflection yields the original vector"""
        v = Vector([1, 2, 3])
        P = Vector([5, 1, -2])

        assert close(
            v,
            v.reflect_on_point(P).reflect_on_point(P)
        )