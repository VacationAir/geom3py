import math

class Transformation:
    """
    A utility class providing geometric transformation methods for 3D objects.
    
    This class contains static methods for scaling, rotation, translation,
    and reflection operations on geometric objects.
    """
    
    @staticmethod
    def scale(obj, factor):
        """
        Scale an object by a given factor.
        
        Args:
            obj: The object to scale (must have x, y, z attributes)
            factor (float): The scaling factor
            
        Returns:
            The scaled object (same type as input)
        """
        return type(obj)(obj.x * factor, obj.y * factor, obj.z * factor)
    
    @staticmethod
    def _rotate_x(obj, angle):
        """
        Rotate an object around the X-axis.
        
        Args:
            obj: The object to rotate (must have x, y, z attributes)
            angle (float): Rotation angle in degrees
            
        Returns:
            The rotated object (same type as input)
        """
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        x_prime = obj.x
        y_prime = obj.x * 0 + obj.y * cos_a - obj.z * sin_a
        z_prime = obj.x * 0 + obj.y * sin_a + obj.z * cos_a

        return type(obj)(x_prime, y_prime, z_prime)

    @staticmethod
    def _rotate_y(obj, angle):
        """
        Rotate an object around the Y-axis.
        
        Args:
            obj: The object to rotate (must have x, y, z attributes)
            angle (float): Rotation angle in degrees
            
        Returns:
            The rotated object (same type as input)
        """
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        x_prime = obj.x * cos_a + obj.y * 0 + obj.z * sin_a
        y_prime = obj.y
        z_prime = -obj.x * sin_a + obj.y * 0 + obj.z * cos_a

        return type(obj)(x_prime, y_prime, z_prime)

    @staticmethod
    def _rotate_z(obj, angle):
        """
        Rotate an object around the Z-axis.
        
        Args:
            obj: The object to rotate (must have x, y, z attributes)
            angle (float): Rotation angle in degrees
            
        Returns:
            The rotated object (same type as input)
        """
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        x_prime = obj.x * cos_a - obj.y * sin_a + obj.z * 0
        y_prime = obj.x * sin_a + obj.y * cos_a + obj.z * 0
        z_prime = obj.z
        
        return type(obj)(x_prime, y_prime, z_prime)

    @staticmethod
    def rotate(obj, angle, axis):
        """
        Rotate an object around a specified axis.
        
        Args:
            obj: The object to rotate (must have x, y, z attributes)
            angle (float): Rotation angle in degrees
            axis (str): Rotation axis ('x', 'y', or 'z')
            
        Returns:
            The rotated object (same type as input)
            
        Raises:
            ValueError: If an invalid axis is specified
        """
        if axis == "x":
            return Transformation._rotate_x(obj, angle)
        elif axis == "y":
            return Transformation._rotate_y(obj, angle)
        elif axis == "z":
            return Transformation._rotate_z(obj, angle)
        else:
            raise ValueError(f"Invalid axis '{axis}'. Must be 'x', 'y', or 'z'.")

    @staticmethod
    def translate(obj, vector):
        """
        Translate an object by a vector.
        
        Args:
            obj: The object to translate (must have x, y, z attributes)
            vector: The translation vector (must have x, y, z attributes)
            
        Returns:
            The translated object (same type as input)
        """
        return type(obj)(obj.x + vector.x, obj.y + vector.y, obj.z + vector.z)

    @staticmethod
    def reflect_on_point(obj, point):
        """
        Reflect an object about a point.
        
        Args:
            obj: The object to reflect (must have x, y, z attributes)
            point: The point of reflection (must be position-aware)
            
        Returns:
            The reflected object (same type as input)
        """
        return type(obj)(point + point - obj)

    @staticmethod
    def reflect_on_line(obj, line):
        """
        Reflect an object about a line.
        
        Args:
            obj: The object to reflect (must have x, y, z attributes)
            line: The line of reflection (must have a foot_point method)
            
        Returns:
            The reflected object (same type as input)
        """
        foot_point = line.foot_point(obj)
        return Transformation.reflect_on_point(obj, foot_point)

    @staticmethod
    def reflect_on_plane(obj, plane):
        """
        Reflect an object about a plane.
        
        Args:
            obj: The object to reflect (must have x, y, z attributes)
            plane: The plane of reflection (must have point and normal vector)
            
        Returns:
            The reflected object (same type as input)
        """
        # Vector from plane point to the object
        ap = obj - plane.point
        
        # Projection scalar onto the normal vector
        projection_scalar = ap.dot(plane.normal_vector) / plane.normal_vector.dot(plane.normal_vector)
        
        # Foot point on the plane
        foot_point = obj - projection_scalar * plane.normal_vector
        
        return Transformation.reflect_on_point(obj, foot_point)