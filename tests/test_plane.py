import random
from geom3py.geometry.plane import Plane
from geom3py.geometry.line import Line
from geom3py.geometry.point import Point
from geom3py.geometry.vector import Vector
from geom3py.utils.linal_utils import close

class TestPlane:

    def test_creation(self):
        """Tests plane creation"""
        E = Plane([0, 0, 0], [1, 1, 1])
        assert E.point == Vector(0, 0, 0)
        assert E.normal_vector == Vector(1, 1, 1)
        
    def test_from_parametric(self):
        """Tests creation from parametric form"""
        E = Plane.from_parametric([1, 0, 0], [0, 1, 0], [0, 0, 1])
        assert E.normal_vector == Vector(1, 0, 0)
        
    def test_contains_point_true(self):
        """Tests if point lies in plane (true)"""
        E = Plane([0, 0, 0], [1, 0, 0])
        p = Point([0, 1, 2])
        assert E.contains_point(p) is True
        
    def test_contains_point_false(self):
        """Tests if point lies in plane (false)"""
        E = Plane([0, 0, 0], [1, 0, 0])
        p = Point([1, 0, 0])
        assert E.contains_point(p) is False
        
    def test_position_line_intersecting(self):
        """Tests intersecting line-plane"""
        E = Plane([0, 0, 0], [1, 0, 0])
        g = Line([-1, 0, 0], [1, 0, 0])
        assert E.position_line(g) == "intersecting"
        
    def test_position_line_parallel(self):
        """Tests parallel line-plane"""
        E = Plane([0, 0, 0], [1, 0, 0])
        g = Line([1, 0, 0], [0, 1, 0])
        assert E.position_line(g) == "parallel"
        
    def test_position_line_identical(self):
        """Tests line lying in plane"""
        E = Plane([0, 0, 0], [1, 0, 0])
        g = Line([0, 1, 0], [0, 1, 0])
        assert E.position_line(g) == "identical"
        
    def test_intersection_line(self):
        """Tests line-plane intersection point"""
        E = Plane([0, 0, 0], [1, 0, 0])
        g = Line([-1, 1, 1], [1, 0, 0])
        intersection = E.intersection_line(g)
        assert intersection == Vector(0, 1, 1)

    def test_position_plane_identical(self):
        """Tests identical planes"""
        E1 = Plane([0, 0, 0], [1, 0, 0])
        E2 = Plane([0, 0, 0], [2, 0, 0])
        assert E1.position_plane(E2) == "identical"
        
    def test_position_plane_parallel(self):
        """Tests parallel planes"""
        E1 = Plane([0, 0, 0], [1, 0, 0])
        E2 = Plane([2, 0, 0], [1, 0, 0])
        assert E1.position_plane(E2) == "parallel"
        
    def test_position_plane_intersecting(self):
        """Tests intersecting planes"""
        E1 = Plane([0, 0, 0], [1, 0, 0])
        E2 = Plane([0, 0, 0], [0, 1, 0])
        assert E1.position_plane(E2) == "intersecting"
        
    def test_angle_plane(self):
        """Tests angle between planes"""
        E1 = Plane([0, 0, 0], [1, 0, 0])
        E2 = Plane([0, 0, 0], [0, 1, 0])
        assert close(E1.angle_plane(E2, deg=True), 90.0)
        
    def test_distance_point(self):
        """Tests point-plane distance"""
        E = Plane([0, 0, 0], [1, 0, 0])
        p = Point([3, 4, 0])
        assert E.distance_point(p) == 3.0
        
    def test_distance_line_parallel(self):
        """Tests line-plane distance (parallel)"""
        E = Plane([0, 0, 0], [1, 0, 0])
        g = Line([1, 1, 0], [0, 1, 0])
        assert E.distance_line(g) == 1.0
        
    def test_distance_plane_parallel(self):
        """Tests plane-plane distance (parallel)"""
        E1 = Plane([0, 0, 0], [1, 0, 0])
        E2 = Plane([5, 0, 0], [2, 0, 0])
        assert E1.distance_plane(E2) == 5.0
        
    def test_intercept_points(self):
        """Tests intercept points of a plane"""
        E = Plane([0, 0, 0], [1, 1, 1])
        intercept = E.intercept_points()
        for s in intercept:
            if s[0] is not None:
                assert close(s[0], 0)

    def test_huge_numbers(self):
        E = Plane(
            [1e150, 1e150, 1e150],
            [1e150, -1e150, 1e150]
        )

        p = Vector(1e150, 1e150, 1e150)

        assert E.contains_point(p)

    def test_random_intersections(self):
        random.seed(42)

        for _ in range(10000):

            p = Vector(
                random.gauss(0, 1),
                random.gauss(0, 1),
                random.gauss(0, 1)
            )

            n = Vector(
                random.gauss(0, 1),
                random.gauss(0, 1),
                random.gauss(0, 1)
            )

            E = Plane(p, n)

            q = p + Vector(
                random.gauss(0, 1),
                random.gauss(0, 1),
                random.gauss(0, 1)
            )

            q = q - ((q - p).dot(n) / n.dot(n)) * n

            assert E.contains_point(q)

class TestTransformPlane:

    def test_scale(self):
        """Tests scaling of a plane"""
        E = Plane(
            Vector([1, 2, 3]),
            Vector([0, 0, 1])
        )

        E2 = E.scale(2)

        assert close(E2.point, Vector([2, 4, 6]))
        assert close(E2.normal_vector, Vector([0, 0, 2]))

    def test_translate(self):
        """Tests translation of a plane"""
        E = Plane(
            Vector([1, 2, 3]),
            Vector([0, 0, 1])
        )

        E2 = E.translate(Vector([1, 1, 1]))

        assert close(E2.point, Vector([2, 3, 4]))
        assert close(E2.normal_vector, Vector([0, 0, 1]))

    def test_rotate_x(self):
        """Tests rotation of a plane around the x-axis"""
        E = Plane(
            Vector([0, 1, 0]),
            Vector([0, 1, 0])
        )

        E2 = E.rotate(90, "x")

        assert close(E2.point, Vector([0, 0, 1]))
        assert close(E2.normal_vector, Vector([0, 0, 1]))

    def test_rotate_y(self):
        """Tests rotation of a plane around the y-axis"""
        E = Plane(
            Vector([0, 0, 1]),
            Vector([0, 0, 1])
        )

        E2 = E.rotate(90, "y")

        assert close(E2.point, Vector([1, 0, 0]))
        assert close(E2.normal_vector, Vector([1, 0, 0]))

    def test_rotate_z(self):
        """Tests rotation of a plane around the z-axis"""
        E = Plane(
            Vector([1, 0, 0]),
            Vector([1, 0, 0])
        )

        E2 = E.rotate(90, "z")

        assert close(E2.point, Vector([0, 1, 0]))
        assert close(E2.normal_vector, Vector([0, 1, 0]))

    def test_reflect_on_point(self):
        """Tests reflection of a plane about a point"""
        E = Plane(
            Vector([1, 2, 3]),
            Vector([0, 0, 1])
        )

        E2 = E.reflect_on_point(Vector([0, 0, 0]))

        assert close(E2.point, Vector([-1, -2, -3]))
        assert close(E2.normal_vector, Vector([0, 0, -1]))

    def test_reflect_on_line(self):
        """Tests reflection of a plane about a line"""
        g = Line(
            Vector([0, 0, 0]),
            Vector([1, 0, 0])
        )

        E = Plane(
            Vector([0, 1, 0]),
            Vector([0, 1, 0])
        )

        E2 = E.reflect_on_line(g)

        assert close(E2.point, Vector([0, -1, 0]))
        assert close(E2.normal_vector, Vector([0, -1, 0]))

    def test_reflect_on_plane(self):
        """Tests reflection of a plane about a plane"""
        mirror = Plane(
            Vector([0, 0, 0]),
            Vector([0, 0, 1])
        )

        E = Plane(
            Vector([1, 2, 3]),
            Vector([0, 1, 1])
        )

        E2 = E.reflect_on_plane(mirror)

        assert close(E2.point, Vector([1, 2, -3]))
        assert close(E2.normal_vector, Vector([0, 1, -1]))