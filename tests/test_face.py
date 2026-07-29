import math
from geom3py.geometry.face import Face
from geom3py.geometry.point import Point
from geom3py.geometry.vector import Vector
from geom3py.geometry.plane import Plane
from geom3py.geometry.line import Line
from geom3py.utils.linal_utils import close

class TestFaceSquarePlanar:
    """
    Tests a simple square face in the xy-plane (z = 0).
    Size: 2x2, corners at (0,0,0), (2,0,0), (2,2,0) and (0,2,0).
    """

    def setup_method(self):
        """Creates a square face in the xy-plane"""
        self.f = Face(
            [0, 0, 0],
            [2, 0, 0],
            [2, 2, 0],
            [0, 2, 0]
        )

    def test_area(self):
        """Checks if the area is correctly calculated as 4.0"""
        assert close(self.f.area(), 4.0)

    def test_center(self):
        """Checks if the center point is at (1, 1, 0)"""
        assert close(self.f.center, [1.0, 1.0, 0.0])

    def test_contains_point_inside(self):
        """Tests a point inside the face"""
        p = Point([1, 1, 0])
        assert self.f.contains_point(p) is True

    def test_contains_point_outside(self):
        """Tests a point far outside the face"""
        p = Point([3, 1, 0])
        assert self.f.contains_point(p) is False

    def test_contains_point_on_edge(self):
        """Tests a point exactly on the bottom edge"""
        p = Point([1, 0, 0])
        assert self.f.contains_point(p) is True

    def test_contains_point_on_corner(self):
        """Tests a point exactly on one of the corners"""
        p = Point([0, 0, 0])
        assert self.f.contains_point(p) is True

    def test_contains_point_not_in_plane(self):
        """Tests a point that is in the 'shadow' but at z=1 (not in the plane)"""
        p = Point([1, 1, 1])
        assert self.f.contains_point(p) is False

    def test_contains_point_below_edge(self):
        """Tests a point in the plane but below the face"""
        p = Point([1, -1, 0])
        assert self.f.contains_point(p) is False
    
    def test_contains_point_left_outside(self):
        """Tests a point in the plane but left outside the face"""
        p = Point([-1, 1, 0])
        assert self.f.contains_point(p) is False

    def test_contains_point_near_corner_outside(self):
        """
        Tests a point just outside a corner (e.g. near (2,2,0)).
        Important to test edge cases of foot point or angle sum.
        """
        p = Point([2.1, 2.1, 0.0])
        assert self.f.contains_point(p) is False

    def test_contains_point_center(self):
        p = Point([1, 1, 0])
        assert self.f.contains_point(p) is True

    def test_contains_point_very_close_to_edge(self):
        p = Point([1e-7, 1, 0])
        assert self.f.contains_point(p) is True

    def test_contains_point_very_close_outside(self):
        p = Point([-1e-7, 1, 0])
        assert self.f.contains_point(p) is False

    def test_contains_point_almost_corner(self):
        p = Point([2-1e-7, 2-1e-7, 0])
        assert self.f.contains_point(p) is True

    def test_contains_point_almost_outside_corner(self):
        p = Point([2+1e-4, 2+1e-4, 0])
        assert self.f.contains_point(p) is False

class TestFaceInclined3D:
    """
    Tests an inclined face in true 3D space (skew plane).
    This ensures that the foot point and projection methods work
    independently of the spatial orientation of the face.
    """

    def setup_method(self):
        """
        Creates an inclined rectangle in space.
        Width = 2, Height = sqrt(2). Area should be 2 * sqrt(2) ≈ 2.828427.
        """
        self.f = Face(
            [0, 0, 0],
            [2, 0, 0],
            [2, 1, 1],  # Tilted up by 45 degrees on the yz-axis
            [0, 1, 1]
        )

    def test_area_inclined(self):
        """Checks the area of the inclined face (width * height)"""
        expected_area = 2.0 * math.sqrt(2.0)
        assert close(self.f.area(), expected_area)

    def test_contains_point_inside_inclined(self):
        """Tests the exact center point of the inclined face"""
        # The center of the inclined face is at (1.0, 0.5, 0.5)
        p = Point([1.0, 0.5, 0.5])
        assert self.f.contains_point(p) is True

    def test_contains_point_outside_plane_inclined(self):
        """Tests a point that would be 'inside' but lies flat on the ground (z=0)"""
        # Lies in the 2D shadow at (1, 0.5, 0), but is not on the inclined plane
        p = Point([1.0, 0.5, 0.0])
        assert self.f.contains_point(p) is False

    def test_contains_point_on_inclined_edge(self):
        """Tests a point exactly on the inclined top edge"""
        # The top edge runs from (2,1,1) to (0,1,1). The middle is (1,1,1)
        p = Point([1.0, 1.0, 1.0])
        assert self.f.contains_point(p) is True

    def test_contains_point_inclined_outside(self):
        """Tests a point on the inclined plane but outside the top boundary"""
        # We go further up along the plane: (1, 2, 2)
        p = Point([1.0, 2.0, 2.0])
        assert self.f.contains_point(p) is False

class TestFaceSuperIrregular3D:
    """
    Tests the `contains_point` method with an absolutely irregular quadrilateral
    (trapezoid with no parallel sides or equal angles), inclined in space.
    
    Geometry in flat state:
      - X1 = [0, 0, 0]
      - X2 = [5, -1, 0]
      - X3 = [4, 3, 0]
      - X4 = [-0.5, 2.5, 0]
      
    Rotated by 45 degrees around the x-axis:
      - y_rot = y * cos(45°) - z * sin(45°) = y * 0.7071
      - z_rot = y * sin(45°) + z * cos(45°) = y * 0.7071
    """

    def setup_method(self):
        """Creates the inclined, completely asymmetric trapezoid"""
        c = math.cos(math.radians(45))  # approx. 0.70710678
        
        self.f = Face(
            [0.0, 0.0, 0.0],          # X1
            [5.0, -1.0 * c, 1.0 * c],  # X2 (originally [5, -1, 0])
            [4.0, 3.0 * c, 3.0 * c],   # X3 (originally [4, 3, 0])
            [-0.5, 2.5 * c, 2.5 * c]   # X4 (originally [-0.5, 2.5, 0])
        )

    def test_contains_point_inside_chaos(self):
        """
        A point deep inside the irregular quadrilateral.
        Flat: [2.0, 1.5, 0.0]
        Rotated: [2.0, 1.5 * cos(45°), 1.5 * sin(45°)]
        """
        c = math.cos(math.radians(45))
        p = Point([2.0, 1.5 * c, 1.5 * c])
        assert self.f.contains_point(p) is True

    def test_contains_point_outside_near_indentation(self):
        """
        A point just outside where the quadrilateral runs asymmetrically.
        Flat: [-1.0, 1.0, 0.0] (Lies left outside edge X4-X1)
        Rotated: [-1.0, 1.0 * cos(45°), 1.0 * sin(45°)]
        """
        c = math.cos(math.radians(45))
        p = Point([-1.0, 1.0 * c, 1.0 * c])
        assert self.f.contains_point(p) is False

    def test_contains_point_near_corner_outside(self):
        """
        Tests a point near the sharp corner X2, but just outside edge X1-X2.
        Flat: [4.0, -1.5, 0.0]
        Rotated: [4.0, -1.5 * cos(45°), -1.5 * sin(45°)]
        """
        c = math.cos(math.radians(45))
        p = Point([4.0, -1.5 * c, -1.5 * c])
        assert self.f.contains_point(p) is False

    def test_contains_point_not_coplanar_chaos(self):
        """
        Tests a point that fits in 2D but floats above the inclined face in 3D.
        """
        c = math.cos(math.radians(45))
        # Correct interior point, but z-coordinate manipulated (+1.0)
        p = Point([2.0, 1.5 * c, (1.5 * c) + 1.0])
        assert self.f.contains_point(p) is False

class TestFaceInteractions3D:
    """
    Tests advanced interactions between two faces in space:
    Position, distance and intersection area/points.
    """

    def setup_method(self):
        """Creates the base face (F1) in the xy-plane (z=0)"""
        self.f1 = Face(
            [0, 0, 0],
            [2, 0, 0],
            [2, 2, 0],
            [0, 2, 0]
        )

    #-----------------------------------------------------------------------#
    # 1. Tests for POSITION_FACE & INTERSECTION_FACE (Spatial Intersection)
    #-----------------------------------------------------------------------#

    def test_interaction_identical(self):
        """Two exactly identical faces"""
        f2 = Face([0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0])
        assert self.f1.position_face(f2) == "identical"
        
        # Intersection of identical face returns the face itself
        intersection = self.f1.intersection_face(f2)
        assert isinstance(intersection, Face)
        assert close(intersection.center, self.f1.center)

    def test_interaction_parallel(self):
        """Face shifted parallel to z = 5.0"""
        f2 = Face([0, 0, 5], [2, 0, 5], [2, 2, 5], [0, 2, 5])
        assert self.f1.position_face(f2) == "parallel"
        assert self.f1.intersection_face(f2) is None
        assert close(self.f1.distance_face(f2), 5.0)

    def test_interaction_intersecting_perfect(self):
        """
        F2 intersects F1 exactly in the middle like a T-junction.
        F2 stands perpendicular to F1 at x = 1.0.
        """
        f2 = Face(
            [1, 0, -1],
            [1, 2, -1],
            [1, 2, 1],
            [1, 0, 1]
        )
        assert self.f1.position_face(f2) == "intersecting"
        
        # The intersection must return the infinite intersection line of the planes
        gS = self.f1.intersection_face(f2)
        assert gS is not None
        # The line must pass through the intersection area (e.g. point [1, 1, 0])
        assert close(gS.distance_point(Vector(1, 1, 0)), 0.0)

    def test_interaction_outside(self):
        """
        The planes intersect but the faces miss each other in space.
        F2 is perpendicular but shifted far away at x = 10.0.
        """
        f2 = Face([10, 0, -1], [10, 2, -1], [10, 2, 1], [10, 0, 1])
        assert self.f1.position_face(f2) == "outside"
        assert self.f1.intersection_face(f2) is None
        # The distance should be the distance between the closest edges (10 - 2 = 8)
        assert close(self.f1.distance_face(f2), 8.0)

    #-----------------------------------------------------------------------#
    # 2. Tests for COPLANAR Cases (Same plane z=0)
    #-----------------------------------------------------------------------#

    def test_interaction_coplanar_outside(self):
        """In the same plane but shifted far away (no contact)"""
        f2 = Face([5, 0, 0], [7, 0, 0], [7, 2, 0], [5, 2, 0])
        assert self.f1.position_face(f2) == "coplanar_outside"
        assert self.f1.intersection_face(f2) is None
        assert close(self.f1.distance_face(f2), 3.0)  # Distance between x=2 and x=5

    def test_interaction_edge_intersecting(self):
        """
        Two frames cross in the same plane at exactly one point.
        F2 is a skewed quadrilateral that pokes the edge of F1 at exactly one point.
        """
        # A triangle/quadrilateral that intersects edge x=2 of F1 exactly at [2, 1, 0]
        f2 = Face([2, 1, 0], [4, 0, 0], [4, 2, 0], [3, 1, 0])
        assert self.f1.position_face(f2) == "edge_intersecting"
        
        # Should return exactly the single intersection point of the frames
        intersection_pt = self.f1.intersection_face(f2)
        assert intersection_pt is not None
        assert close(intersection_pt, [2.0, 1.0, 0.0])
        assert close(self.f1.distance_face(f2), 0.0)

    def test_interaction_coplanar_intersecting(self):
        """
        Overlap like two cards on the table.
        F2 is shifted 1.0 right and 1.0 up.
        Overlap area is the square from [1,1,0] to [2,2,0].
        """
        f2 = Face([1, 1, 0], [3, 1, 0], [3, 3, 0], [1, 3, 0])
        assert self.f1.position_face(f2) == "coplanar_intersecting"
        
        # Your brilliant method creates a new intersection face here!
        f_intersection = self.f1.intersection_face(f2)
        assert isinstance(f_intersection, Face)
        # The area of the overlapping 1x1 square must be 1.0
        assert close(f_intersection.area(), 1.0)
        assert close(self.f1.distance_face(f2), 0.0)

    def test_interaction_on_edge(self):
        """Two faces perfectly edge to edge (curb contact)"""
        f2 = Face([2, 0, 0], [4, 0, 0], [4, 2, 0], [2, 2, 0])
        assert self.f1.position_face(f2) == "on_edge"
        assert close(self.f1.distance_face(f2), 0.0)

    def test_interaction_touching_corner(self):
        """Two faces touch exactly at a single corner (e.g. at [2,2,0])"""
        f2 = Face([2, 2, 0], [4, 2, 0], [4, 4, 0], [2, 4, 0])
        assert self.f1.position_face(f2) == "touching"
        
        intersection_pt = self.f1.intersection_face(f2)
        assert intersection_pt is not None
        assert close(intersection_pt, [2.0, 2.0, 0.0])
        assert close(self.f1.distance_face(f2), 0.0)

    def test_interaction_on_edge_partial(self):
        f2 = Face(
            [2, 1, 0],
            [4, 1, 0],
            [4, 2, 0],
            [2, 2, 0],
        )

        assert self.f1.position_face(f2) == "on_edge"
        assert close(self.f1.distance_face(f2), 0.0)

    def test_interaction_collinear_separated(self):
        f2 = Face(
            [2, 3, 0],
            [4, 3, 0],
            [4, 5, 0],
            [2, 5, 0],
        )

        assert self.f1.position_face(f2) == "coplanar_outside"

    def test_interaction_only_one_corner_point(self):
        f2 = Face(
            [2,2,0],
            [3,2,0],
            [3,3,0],
            [2,3,0],
        )

        assert self.f1.position_face(f2) == "touching"

    def test_interaction_edge_contained(self):
        f2 = Face(
            [2,0.5,0],
            [3,0.5,0],
            [3,1.5,0],
            [2,1.5,0],
        )

        assert self.f1.position_face(f2) == "on_edge"

    def test_interaction_on_edge_only_end(self):
        f2 = Face(
            [2,2,0],
            [4,2,0],
            [4,3,0],
            [2,3,0],
        )

        assert self.f1.position_face(f2) == "touching"
    
    def test_interaction_on_edge_only_start(self):
        f2 = Face(
            [2,-2,0],
            [4,-2,0],
            [4,0,0],
            [2,0,0],
        )

        assert self.f1.position_face(f2) == "touching"

    def test_intersection_face_on_edge(self):
        f2 = Face(
            [2,0,0],
            [4,0,0],
            [4,2,0],
            [2,2,0],
        )

        assert self.f1.position_face(f2) == "on_edge"
        assert self.f1.intersection_face(f2) is None
        assert self.f1.distance_face(f2) == 0.0

class TestFaceTransformations:
    """
    Tests transformations of a square face in the xy-plane.
    Size: 2x2, corners at (0,0,0), (2,0,0), (2,2,0) and (0,2,0).
    """

    def setup_method(self):
        """Creates a square face in the xy-plane"""
        self.f = Face(
            [0, 0, 0],
            [2, 0, 0],
            [2, 2, 0],
            [0, 2, 0]
        )

    def test_scale(self):
        """Checks if the face is scaled correctly"""
        scaled = self.f.scale(2)

        assert close(scaled.X1, [0, 0, 0])
        assert close(scaled.X2, [4, 0, 0])
        assert close(scaled.X3, [4, 4, 0])
        assert close(scaled.X4, [0, 4, 0])

    def test_rotate_around_z_axis(self):
        """Checks a rotation of 90 degrees around the z-axis"""
        rotated = self.f.rotate(90, "z")

        assert close(rotated.X1, [0, 0, 0])
        assert close(rotated.X2, [0, 2, 0])
        assert close(rotated.X3, [-2, 2, 0])
        assert close(rotated.X4, [-2, 0, 0])

    def test_translate(self):
        """Checks a translation of the face"""
        v = Vector(1, 2, 3)

        translated = self.f.translate(v)

        assert close(translated.X1, [1, 2, 3])
        assert close(translated.X2, [3, 2, 3])
        assert close(translated.X3, [3, 4, 3])
        assert close(translated.X4, [1, 4, 3])

    def test_reflect_on_point(self):
        """Checks point reflection at the origin"""
        P = Point([0, 0, 0])

        reflected = self.f.reflect_on_point(P)

        assert close(reflected.X1, [0, 0, 0])
        assert close(reflected.X2, [-2, 0, 0])
        assert close(reflected.X3, [-2, -2, 0])
        assert close(reflected.X4, [0, -2, 0])

    def test_reflect_on_line(self):
        """Checks reflection about the x-axis"""
        g = Line(
            Point([0, 0, 0]),
            Vector(1, 0, 0)
        )

        reflected = self.f.reflect_on_line(g)

        assert close(reflected.X1, [0, 0, 0])
        assert close(reflected.X2, [2, 0, 0])
        assert close(reflected.X3, [2, -2, 0])
        assert close(reflected.X4, [0, -2, 0])

    def test_reflect_on_plane(self):
        """Checks reflection about the xy-plane"""
        E = Plane.from_parametric(
            Point([0, 0, 0]),
            Vector(1, 0, 0),
            Vector(0, 1, 0)
        )

        reflected = self.f.reflect_on_plane(E)

        assert close(reflected.X1, [0, 0, 0])
        assert close(reflected.X2, [2, 0, 0])
        assert close(reflected.X3, [2, 2, 0])
        assert close(reflected.X4, [0, 2, 0])