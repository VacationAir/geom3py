from .vector import Vector

class Point(Vector):
    """
    Represents a point in three-dimensional space.

    A point describes a position in the Cartesian coordinate system
    using its three coordinates (x, y, z). This class extends
    :class:`Vector` with point-specific operations, such as
    calculating the distance between two points or the direction vector
    between them.

    Parameters
    ----------
    point : array_like
        An iterable object with three coordinate values (x, y, z).

    Notes
    -----
    A point is mathematically closely related to a vector, but has a
    different geometric meaning. While a vector describes a direction or
    displacement, a point represents a fixed position in space.
    """

    def distance_point(self, p2):
        """
        Calculate the Euclidean distance to another point.

        The distance is calculated using the formula:
        d = sqrt((x-x')² + (y-y')² + (z-z')²)

        Parameters
        ----------
        other_point : array_like
            The coordinates of the second point as a list, tuple, or array.

        Returns
        -------
        float
            The Euclidean distance between the two points.
        """
        diff = self - p2
        return diff.magnitude()
    
    def point_point(self, p2):
        """
        Calculate the vector from this point to another point.

        The resulting vector points from the current point to the specified point.

        Parameters
        ----------
        other_point : array_like
            The coordinates of the target point as a list, tuple, or array.

        Returns
        -------
        Vector
            The connecting vector (other_point - self) as a Vector object.
        """
        return p2 - self