from ..geometry.point import Point

class Camera:
    def __init__(self):
        self.offsetx = 960
        self.offsety = 540
        self.scale = 50

        self.x_rot = 45
        self.y_rot = 45
        self.fov = 90

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

    

