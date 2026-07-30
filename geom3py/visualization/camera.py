from ..geometry.point import Point

class Camera:
    """
    A 3D camera for perspective projection and scene navigation.

    This class handles the transformation of 3D points to 2D screen coordinates
    using perspective projection with rotation capabilities.

    Parameters
    ----------
    None

    Attributes
    ----------
    offsetx : int
        X offset of the camera viewport center (default: 960)
    offsety : int
        Y offset of the camera viewport center (default: 540)
    scale : int
        Scale factor for the projection (default: 50)
    x_rot : float
        Rotation angle around the X-axis in degrees (default: -45)
    y_rot : float
        Rotation angle around the Y-axis in degrees (default: 45)
    fov : int
        Field of view for perspective projection (default: 90)
    _scene : Scene or None
        Reference to the parent scene for automatic redrawing

    Examples
    --------
    >>> from geom3py.visualization import Camera
    >>> camera = Camera()
    >>> point = Point(1, 2, 3)
    >>> x, y = camera.project(point)
    """

    def __init__(self):
        """
        Initializes a new camera with default parameters.

        Default settings:
        - Viewport center at (960, 540) for 1920x1080 display
        - Scale factor of 50
        - Initial rotation: -45° around X, 45° around Y
        - Field of view: 90°
        """
        self.offsetx = 960
        self.offsety = 540
        self.scale = 50

        self.x_rot = -45
        self.y_rot = 45
        self.fov = 90

        self._scene = None

    def remapping(self, point3d):
        """
        Applies coordinate remapping and rotation to a 3D point.

        The point is first remapped from (x, y, z) to (x, z, y) to align
        with the camera's coordinate system. Then rotations are applied
        around the Y-axis first, then the X-axis.

        Parameters
        ----------
        point3d : Point
            The 3D point to remap and rotate

        Returns
        -------
        Point
            The remapped and rotated point

        Examples
        --------
        >>> p = Point(1, 2, 3)
        >>> rotated = camera.remapping(p)
        """
        remapped = Point(point3d.x, point3d.z, point3d.y)
        return remapped.rotate(self.y_rot, "y").rotate(self.x_rot, "x")

    def project(self, point3d):
        """
        Projects a 3D point to 2D screen coordinates.

        This method applies perspective projection to convert a 3D point
        into 2D pixel coordinates on the screen. Points behind the camera
        (z <= 0) return None.

        Parameters
        ----------
        point3d : Point
            The 3D point to project

        Returns
        -------
        tuple or None
            A tuple (x, y) of screen coordinates in pixels, or None if the
            point is behind the camera

        Notes
        -----
        The projection uses the formula:
        px = (x * fov / (z + fov)) * scale + offsetx
        py = -(y * fov / (z + fov)) * scale + offsety

        Examples
        --------
        >>> p = Point(1, 2, 3)
        >>> screen_coords = camera.project(p)
        >>> if screen_coords:
        ...     x, y = screen_coords
        ...     print(f"Screen position: ({x:.0f}, {y:.0f})")
        """
        projection = self.remapping(point3d)
        z = projection.z + self.fov

        if z <= 0:
            return None

        px = projection.x * (self.fov / z) * self.scale + self.offsetx
        py = -projection.y * (self.fov / z) * self.scale + self.offsety

        return px, py

    def set_scene(self, scene):
        """
        Sets the parent scene for automatic redrawing.

        When the camera is updated, it will automatically trigger a
        redraw of the associated scene.

        Parameters
        ----------
        scene : Scene
            The parent scene to associate with this camera

        Returns
        -------
        None

        Examples
        --------
        >>> scene = Scene()
        >>> camera = Camera()
        >>> camera.set_scene(scene)
        """
        self._scene = scene

    def update(self, dx_rot, dy_rot, d_zoom):
        """
        Updates the camera parameters and triggers a redraw.

        This method applies incremental changes to the camera's rotation
        and field of view, then automatically redraws the scene.

        Parameters
        ----------
        dx_rot : float
            Change in X-axis rotation in degrees
        dy_rot : float
            Change in Y-axis rotation in degrees
        d_zoom : float
            Change in field of view (positive zooms in, negative zooms out)

        Returns
        -------
        None

        Notes
        -----
        After updating the camera, the scene is automatically redrawn
        if a scene has been set with `set_scene()`.

        Examples
        --------
        >>> # Rotate 5 degrees to the right
        >>> camera.update(0, 5, 0)
        >>> 
        >>> # Rotate up and zoom in
        >>> camera.update(-5, 0, 10)
        """
        self.x_rot += dx_rot
        self.y_rot += dy_rot
        self.fov += d_zoom
        self._scene.render()