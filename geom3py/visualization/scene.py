import tkinter as tk
from .camera import Camera
from ..geometry.point import Point
from ..geometry.vector import Vector

class Scene:
    def __init__(self, width=1920, height=1080):
        self.root = tk.Tk()
        self.root.title("Geom3py Viewer")

        self.width = width
        self.height = height
        self.canvas = tk.Canvas(
            self.root,
            width = width,
            height = height,
            bg = "white"
        )

        self.canvas.pack()

        self.camera = Camera()
        self.objects = []

        self._bind_events()
        self.camera.set_scene(self)


    def _draw_axes(self, show_ticks=True, tick_spacing=1.0):
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
                tags=("axes", )
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
        self.objects.append((obj, kwargs))
        self.render()

    def render(self):
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
        self.canvas.bind('<Up>', self._on_arrow_up)
        self.canvas.bind('<Down>', self._on_arrow_down)
        self.canvas.bind('<Left>', self._on_arrow_left)
        self.canvas.bind('<Right>', self._on_arrow_right)

        self.canvas.bind('<MouseWheel>', self._on_mouse_wheel)

        self.canvas.focus_set()

    def _on_arrow_down(self, event):
        self.camera.update(dx_rot=5, dy_rot=0, d_zoom=0)

    def _on_arrow_up(self, event):
        self.camera.update(dx_rot=-5, dy_rot=0, d_zoom=0)

    def _on_arrow_right(self, event):
        self.camera.update(dx_rot=0, dy_rot=5, d_zoom=0)

    def _on_arrow_left(self, event):
        self.camera.update(dx_rot=0, dy_rot=-5, d_zoom=0)

    def _on_mouse_wheel(self, event):
        if event.delta > 0:
            self.camera.update(0, 0, 45)
        else:
            self.camera.update(0, 0, -45)
                
        self.render()

    def show(self):
        self.root.mainloop()
