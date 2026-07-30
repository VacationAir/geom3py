import tkinter as tk
from .camera import Camera
from ..geometry.point import Point
from ..geometry.vector import Vector

class Scene:
    """
    A 3D visualization scene for displaying geometric objects.

    This class creates an interactive Tkinter window where geometric objects
    can be displayed, rotated, and explored in real-time.

    Parameters
    ----------
    width : int, optional
        Width of the canvas in pixels (default: 1920)
    height : int, optional
        Height of the canvas in pixels (default: 1080)

    Attributes
    ----------
    root : tk.Tk
        The main Tkinter window
    canvas : tk.Canvas
        The drawing canvas
    camera : Camera
        The 3D camera for projection
    objects : list
        List of (object, kwargs) tuples to display

    Examples
    --------
    >>> from geom3py import Point, Box
    >>> from geom3py.visualization import Scene
    >>> scene = Scene()
    >>> scene.add(Point(1, 2, 3), color='red')
    >>> scene.add(Box([0,0,0], [2,2,2]), fill='lightblue')
    >>> scene.show()
    """

    def __init__(self, width=1920, height=1080):
        """
        Initializes a new 3D visualization scene.

        Parameters
        ----------
        width : int, optional
            Width of the canvas in pixels (default: 1920)
        height : int, optional
            Height of the canvas in pixels (default: 1080)
        """
        self.root = tk.Tk()
        self.root.title("Geom3py Viewer")

        self.width = width
        self.height = height
        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg="white"
        )

        self.canvas.pack()

        self.camera = Camera()
        self.objects = []

        self._bind_events()
        self.camera.set_scene(self)

    def _draw_axes(self, show_ticks=True, tick_spacing=1.0):
        """
        Draws the coordinate axes X, Y, Z on the canvas.

        Parameters
        ----------
        show_ticks : bool, optional
            Whether to show tick marks on the axes (default: True)
        tick_spacing : float, optional
            Spacing between tick marks in 3D units (default: 1.0)
        """
        colors = {
            'x': '#ff0000',
            'y': '#00cc00',
            'z': '#0066ff',
            'tick': '#888888'
        }

        len_x = self.width/(self.camera.scale)
        len_y = self.height/(self.camera.scale)
        len_z = (len_x + len_y)

        axes_info = {
            'x': (Vector(1, 0, 0), len_x, 'X', colors['x']),
            'y': (Vector(0, 1, 0), len_y, 'Y', colors['y']),
            'z': (Vector(0, 0, 1), len_z, 'Z', colors['z'])
        }

        origin = Point(0, 0, 0)
        ox, oy = self.camera.project(origin)

        if ox is None or oy is None:
            return None

        for axis, (direction, length, label, color) in axes_info.items():
            end = direction * length
            x1, y1 = self.camera.project(Point(end.x, end.y, end.z))
            x2, y2 = self.camera.project(Point(-end.x, -end.y, -end.z))

            self.canvas.create_line(
                ox, oy, x1, y1,
                fill=color,
                width=2,
                tags=('axes',)
            )

            self.canvas.create_line(
                x2, y2, ox, oy,
                fill=color,
                width=2,
                tags=("axes",)
            )

            label_pos = direction * (length + 0.5)
            lx1, ly1 = self.camera.project(Point(label_pos.x, label_pos.y, label_pos.z))
            lx2, ly2 = self.camera.project(Point(-label_pos.x, -label_pos.y, -label_pos.z))
            self.canvas.create_text(
                lx1, ly1,
                text=label,
                fill=color,
                font=('Arial', 12, 'bold'),
                tags=('axes',)
            )

            self.canvas.create_text(
                lx2, ly2,
                text=label,
                fill=color,
                font=('Arial', 12, 'bold'),
                tags=('axes',)
            )

            if show_ticks:
                step = tick_spacing
                max_ticks = int(length / step)

                for i in range(1, max_ticks + 1):
                    pos = direction * (i * step)
                    x1, y1 = self.camera.project(Point(pos.x, pos.y, pos.z))
                    x2, y2 = self.camera.project(Point(-pos.x, -pos.y, -pos.z))
                    self.canvas.create_text(
                        x1, y1 - 12,
                        text=str(round(i * step, 1)),
                        fill=colors['tick'],
                        font=('Arial', 8),
                        tags=('axes',)
                    )

                    self.canvas.create_text(
                        x2, y2 - 12,
                        text=str(round(-i * step, 1)),
                        fill=colors['tick'],
                        font=('Arial', 8),
                        tags=('axes',)
                    )

    def add(self, obj, **kwargs):
        """
        Adds a geometric object to the scene.

        Parameters
        ----------
        obj : object
            The geometric object to add (Point, Line, Face, Box, Polygon, etc.)
        **kwargs : dict
            Styling options for the object:
            - fill : str
                Fill color for faces and polygons (default: 'lightblue')
            - outline : str
                Outline color (default: 'blue')
            - color : str
                Color for lines and points (default: varies)
            - width : int
                Line width in pixels (default: 2)
            - size : int
                Point size in pixels (default: 5)

        Returns
        -------
        None

        Examples
        --------
        >>> scene.add(Point(1, 2, 3), color='red', size=8)
        >>> scene.add(Box([0,0,0], [2,2,2]), fill='lightblue', outline='blue')
        >>> scene.add(Line([0,0,0], [2,2,2]), color='green', width=3)
        """
        self.objects.append((obj, kwargs))
        self.render()

    def render(self):
        """
        Renders all objects in the scene.

        This method clears the canvas, draws the axes, and redraws all objects
        in depth-sorted order. It is called automatically after adding objects
        or changing the camera.

        Returns
        -------
        None
        """
        self.canvas.delete("all")
        self._draw_axes()

        objects_depth = []
        for obj, kwargs in self.objects:

            try:
                depth = obj.get_depth(self.camera)
            except AttributeError:
                depth = 0

            objects_depth.append((depth, obj, kwargs))

        objects_depth.sort(key=lambda x: x[0], reverse=True)

        for _, obj, kwargs in objects_depth:
            obj.draw_on_canvas(self.canvas, self.camera, **kwargs)

    def _bind_events(self):
        """
        Binds keyboard and mouse events to their handlers.

        This method sets up the event bindings for:
        - Arrow keys for rotation
        - Mouse wheel for zoom

        Returns
        -------
        None
        """
        self.canvas.bind('<Up>', self._on_arrow_up)
        self.canvas.bind('<Down>', self._on_arrow_down)
        self.canvas.bind('<Left>', self._on_arrow_left)
        self.canvas.bind('<Right>', self._on_arrow_right)

        self.canvas.bind('<MouseWheel>', self._on_mouse_wheel)

        self.canvas.focus_set()

    def _on_arrow_down(self, event):
        """
        Handles the Down arrow key press.

        Rotates the camera downward around the X-axis.

        Parameters
        ----------
        event : tk.Event
            The Tkinter event object

        Returns
        -------
        None
        """
        self.camera.update(dx_rot=5, dy_rot=0, d_zoom=0)

    def _on_arrow_up(self, event):
        """
        Handles the Up arrow key press.

        Rotates the camera upward around the X-axis.

        Parameters
        ----------
        event : tk.Event
            The Tkinter event object

        Returns
        -------
        None
        """
        self.camera.update(dx_rot=-5, dy_rot=0, d_zoom=0)

    def _on_arrow_right(self, event):
        """
        Handles the Right arrow key press.

        Rotates the camera to the right around the Y-axis.

        Parameters
        ----------
        event : tk.Event
            The Tkinter event object

        Returns
        -------
        None
        """
        self.camera.update(dx_rot=0, dy_rot=5, d_zoom=0)

    def _on_arrow_left(self, event):
        """
        Handles the Left arrow key press.

        Rotates the camera to the left around the Y-axis.

        Parameters
        ----------
        event : tk.Event
            The Tkinter event object

        Returns
        -------
        None
        """
        self.camera.update(dx_rot=0, dy_rot=-5, d_zoom=0)

    def _on_mouse_wheel(self, event):
        """
        Handles mouse wheel events for zooming.

        Parameters
        ----------
        event : tk.Event
            The Tkinter event object containing delta information

        Returns
        -------
        None

        Notes
        -----
        - Positive delta (scroll up): Zoom in
        - Negative delta (scroll down): Zoom out
        """
        if event.delta > 0:
            self.camera.update(0, 0, 45)
        else:
            self.camera.update(0, 0, -45)

        self.render()

    def show(self):
        """
        Displays the scene window and starts the interactive viewer.

        This method enters the Tkinter main loop and blocks until the
        window is closed.

        Returns
        -------
        None

        Examples
        --------
        >>> scene = Scene()
        >>> scene.add(Point(0, 0, 0))
        >>> scene.show()  # Window opens and blocks
        """
        self.root.mainloop()