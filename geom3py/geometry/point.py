from .vector import Vector
from ..utils.linal_utils import close

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
    def __eq__(self, p2):
        return self.equals(p2)
    
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

    def equals(self, p2):
        """
        Calculates wether two points are equal or not
        -------
        Returns
            boolean: wether they are equal or not
        """
        if close(self.distance_point(p2), 0):
            return True

        else:
            return False
        
    # ======================================================================
    # Visualization
    # ======================================================================

    def draw_on_canvas(self, canvas, camera, **kwargs):
        """
        Draws the point on a Tkinter canvas.

        Parameters
        ----------
        canvas : tk.Canvas
            The canvas to draw on
        camera : Camera
            The camera for 3D to 2D projection
        **kwargs : dict
            Styling options:
            - radius : int
                Radius of the point in pixels (default: 4)
            - color : str
                Color of the point (default: 'red')

        Returns
        -------
        None

        Notes
        -----
        If the point is behind the camera (projection returns None),
        nothing is drawn.

        Examples
        --------
        >>> point = Point(1, 2, 3)
        >>> scene.add(point, color='blue', radius=6)
        """
        x, y = camera.project(self)
        
        # If point is behind camera, don't draw
        if x is None or y is None:
            return
        
        radius = kwargs.get("radius", 4)
        color = kwargs.get("color", "red")

        canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline=color,
            tags=("point",)
        )

    def get_depth(self, camera):
        """
        Calculates the depth of the point with respect to the camera.

        Parameters
        ----------
        camera : Camera
            The camera for depth calculation

        Returns
        -------
        float
            The depth (Z-coordinate) of the point in camera space

        Notes
        -----
        This is used for z-ordering when rendering multiple objects.
        Objects with larger depth values are drawn first (farther away).

        Examples
        --------
        >>> p = Point(1, 2, 3)
        >>> depth = p.get_depth(camera)
        """
        projected = camera.remapping(self)
        return projected.z