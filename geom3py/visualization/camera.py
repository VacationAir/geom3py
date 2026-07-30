from ..geometry.point import Point

class Camera:
    def __init__(self):
        self.offsetx = 960
        self.offsety = 540
        self.scale = 50

        self.x_rot = -45
        self.y_rot = 45
        self.fov = 90

        self._scene = None

    def remapping(self, point3d):
        remapped = Point(point3d.x, point3d.z, point3d.y)
        return remapped.rotate(self.y_rot, "y").rotate(self.x_rot, "x")


    def project(self, point3d):
        projection = self.remapping(point3d)
        z = projection.z + self.fov

        if z <= 0:
            return None

        px =   projection.x * (self.fov / z) * self.scale + self.offsetx
        py = - projection.y * (self.fov / z) * self.scale + self.offsety

        return px, py

    def set_scene(self, scene):
        self._scene = scene

    def update(self, dx_rot, dy_rot, d_zoom):
        self.x_rot += dx_rot
        self.y_rot += dy_rot
        self.fov += d_zoom
        self._scene.render()

