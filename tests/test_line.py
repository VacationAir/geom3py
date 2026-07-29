from geom3py.geometry.line import Line
from geom3py.geometry.point import Point
from geom3py.geometry.vector import Vector
from geom3py.geometry.plane import Plane
from geom3py.utils.linal_utils import close

class TestLine:

    def test_creation_from_points(self):
        """Tests line creation from two points"""
        g = Line.from_points([0, 0, 0], [1, 1, 1])
        assert close(g.support_vector, [0, 0, 0])
        assert close(g.direction_vector, [1, 1, 1])
        
    def test_point_at(self):
        """Tests point calculation on the line"""
        g = Line([0, 0, 0], [1, 1, 1])
        assert close(g.point_at(2), [2, 2, 2])
        
    def test_contains_point_true(self):
        """Tests if a point lies on the line (true)"""
        g = Line.from_points([0, 0, 0], [2, 2, 2])
        p = Point([1, 1, 1])
        assert g.contains_point(p) is True
        
    def test_contains_point_false(self):
        """Tests if a point lies on the line (false)"""
        g = Line.from_points([0, 0, 0], [2, 2, 2])
        p = Point([1, 2, 3])
        assert g.contains_point(p) is False
        
    def test_distance_point(self):
        """Tests distance between point and line"""
        g = Line([0, 0, 0], [1, 0, 0])
        p = Point([1, 1, 0])
        assert g.distance_point(p) == 1.0
        
    def test_angle_lines(self):
        """Tests angle between two lines"""
        g1 = Line([0, 0, 0], [1, 0, 0])
        g2 = Line([0, 0, 0], [0, 1, 0])
        assert close(g1.angle_lines(g2, deg=True), 90.0)
        
    def test_position_line_identical(self):
        """Tests identical lines"""
        g1 = Line([0, 0, 0], [1, 1, 1])
        g2 = Line([1, 1, 1], [2, 2, 2])
        assert g1.position_line(g2) == "identical"
        
    def test_position_line_parallel(self):
        """Tests parallel lines"""
        g1 = Line([0, 0, 0], [1, 1, 1])
        g2 = Line([1, 0, 0], [2, 2, 2])
        assert g1.position_line(g2) == "parallel"
        
    def test_position_line_intersecting(self):
        """Tests intersecting lines"""
        g1 = Line([0, 0, 0], [1, 0, 0])
        g2 = Line([0, 0, 0], [0, 1, 0])
        assert g1.position_line(g2) == "intersecting"
        
    def test_position_line_skew(self):
        """Tests skew lines"""
        g1 = Line([0, 0, 0], [1, 0, 0])
        g2 = Line([0, 1, 0], [0, 1, 1])
        assert g1.position_line(g2) == "skew"
        
    def test_intersection_with_line(self):
        """Tests intersection point of two lines"""
        g1 = Line([0, 0, 0], [1, 0, 0])
        g2 = Line([0, 0, 0], [0, 1, 0])
        intersection = g1.intersection_line(g2)
        assert close(intersection, [0, 0, 0])
        
    def test_intercept_points(self):
        """Tests intercept points of a line"""
        g = Line.from_points([1, 2, 3], [2, 3, 4])
        intercept = g.intercept_points()
        assert len(intercept) == 3


class TestTransformLine:

    def test_scale(self):
        """Tests scaling of a line"""
        g = Line(
            Vector([1, 2, 3]),
            Vector([4, 5, 6])
        )

        g2 = g.scale(2)

        assert close(g2.support_vector, Vector([2, 4, 6]))
        assert close(g2.direction_vector, Vector([8, 10, 12]))

    def test_translate(self):
        """Tests translation of a line"""
        g = Line(
            Vector([1, 2, 3]),
            Vector([4, 5, 6])
        )

        g2 = g.translate(Vector([1, 1, 1]))

        assert close(g2.support_vector, Vector([2, 3, 4]))
        assert close(g2.direction_vector, Vector([4, 5, 6]))

    def test_rotate_x(self):
        """Tests rotation of a line around the x-axis"""
        g = Line(
            Vector([0, 1, 0]),
            Vector([0, 1, 0])
        )

        g2 = g.rotate(90, "x")

        assert close(g2.support_vector, Vector([0, 0, 1]))
        assert close(g2.direction_vector, Vector([0, 0, 1]))

    def test_rotate_y(self):
        """Tests rotation of a line around the y-axis"""
        g = Line(
            Vector([0, 0, 1]),
            Vector([0, 0, 1])
        )

        g2 = g.rotate(90, "y")

        assert close(g2.support_vector, Vector([1, 0, 0]))
        assert close(g2.direction_vector, Vector([1, 0, 0]))

    def test_rotate_z(self):
        """Tests rotation of a line around the z-axis"""
        g = Line(
            Vector([1, 0, 0]),
            Vector([1, 0, 0])
        )

        g2 = g.rotate(90, "z")

        assert close(g2.support_vector, Vector([0, 1, 0]))
        assert close(g2.direction_vector, Vector([0, 1, 0]))

    def test_reflect_on_point(self):
        """Tests reflection of a line about a point"""
        g = Line(
            Vector([1, 2, 3]),
            Vector([1, 0, 0])
        )

        g2 = g.reflect_on_point(Vector([0, 0, 0]))

        assert close(g2.support_vector, Vector([-1, -2, -3]))
        assert close(g2.direction_vector, Vector([-1, 0, 0]))

    def test_reflect_on_line(self):
        """Tests reflection of a line about a line"""
        axis = Line(
            Vector([0, 0, 0]),
            Vector([1, 0, 0])
        )

        g = Line(
            Vector([0, 1, 0]),
            Vector([1, 0, 0])
        )

        g2 = g.reflect_on_line(axis)

        assert close(g2.support_vector, Vector([0, -1, 0]))
        assert close(g2.direction_vector, Vector([1, 0, 0]))

    def test_reflect_on_plane(self):
        """Tests reflection of a line about a plane"""
        E = Plane(
            Vector([0, 0, 0]),
            Vector([0, 0, 1])
        )

        g = Line(
            Vector([1, 2, 3]),
            Vector([1, 0, 0])
        )

        g2 = g.reflect_on_plane(E)

        assert close(g2.support_vector, Vector([1, 2, -3]))
        assert close(g2.direction_vector, Vector([1, 0, 0]))