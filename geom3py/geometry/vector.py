import math
from ..utils.transform_utils import Transformation

class Vector(tuple):
    """
    A 3D vector class with support for basic operations and geometric transformations.
    
    Attributes:
        x (float): X-coordinate of the vector
        y (float): Y-coordinate of the vector
        z (float): Z-coordinate of the vector
    """
    
    def __new__(cls, x, y=None, z=None):
        if y is None and z is None:
            # If passed a list or tuple like Vector([1, 2, 3])
            return super().__new__(cls, (float(x[0]), float(x[1]), float(x[2])))
        return super().__new__(cls, (float(x), float(y), float(z)))

    @property
    def x(self): return self[0]
    
    @property
    def y(self): return self[1]
    
    @property
    def z(self): return self[2]

    # Basic arithmetic operations
    def __add__(self, other):
        """Vector addition."""
        return Vector(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, scalar):
        """Scalar multiplication."""
        return Vector(self[0] * scalar, self[1] * scalar, self[2] * scalar)

    def __rmul__(self, scalar):
        """Scalar multiplication (reverse order)."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        """Scalar division."""
        return Vector(self[0] / scalar, self[1] / scalar, self[2] / scalar)

    def __neg__(self):
        """Negation of the vector."""
        return Vector(-self[0], -self[1], -self[2])
    
    def __abs__(self):
        """Magnitude (length) of the vector."""
        return math.sqrt(self[0]**2 + self[1]**2 + self[2]**2)

    def dot(self, other):
        """
        Compute the dot product with another vector.
        
        Args:
            other (Vector): The other vector
            
        Returns:
            float: The dot product
        """
        return self[0]*other[0] + self[1]*other[1] + self[2]*other[2]

    def cross(self, other):
        """
        Compute the cross product with another vector.
        
        Args:
            other (Vector): The other vector
            
        Returns:
            Vector: The cross product vector
        """
        return Vector(
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0]
        )

    def magnitude(self):
        """
        Calculate the magnitude (length) of the vector.
        
        Returns:
            float: The magnitude of the vector
        """
        return abs(self)

    def normalize(self):
        """
        Return a unit vector in the same direction.
        
        Returns:
            Vector: Normalized vector
            
        Raises:
            ValueError: If the vector has zero magnitude
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return self / mag

    def angle_with(self, other, degrees=False):
        """
        Calculate the angle between this vector and another.
        
        Args:
            other (Vector): The other vector
            degrees (bool): If True, return angle in degrees, else in radians
            
        Returns:
            float: The angle between the vectors
        """
        dot_product = self.dot(other)
        magnitudes = self.magnitude() * other.magnitude()
        if magnitudes == 0:
            raise ValueError("Cannot calculate angle with zero vector")
        
        cos_angle = dot_product / magnitudes
        # Clamp to avoid floating point errors
        cos_angle = max(-1.0, min(1.0, cos_angle))
        angle = math.acos(cos_angle)
        
        return math.degrees(angle) if degrees else angle

    # ======================================================================
    # Geometric Transformations
    # ======================================================================

    def scale(self, factor):
        """
        Scale the vector by a factor.
        
        Args:
            factor (float): Scaling factor
            
        Returns:
            Vector: The scaled vector
        """
        return Transformation.scale(self, factor)

    def rotate(self, angle, axis):
        """
        Rotate the vector around an axis.
        
        Args:
            angle (float): Rotation angle (in radians)
            axis (str): Rotation axis ('x', 'y', 'z', or a Vector)
            
        Returns:
            Vector: The rotated vector
        """
        return Transformation.rotate(self, angle, axis)

    def translate(self, vector):
        """
        Translate the vector by another vector.
        
        Args:
            vector (Vector): Translation vector
            
        Returns:
            Vector: The translated vector
        """
        return Transformation.translate(self, vector)

    def reflect_on_point(self, point):
        """
        Reflect the vector about a point.
        
        Args:
            point (Point): The point of reflection
            
        Returns:
            Vector: The reflected vector
        """
        return Transformation.reflect_on_point(self, point)

    def reflect_on_line(self, line):
        """
        Reflect the vector about a line.
        
        Args:
            line (Line): The line of reflection
            
        Returns:
            Vector: The reflected vector
        """
        return Transformation.reflect_on_line(self, line)

    def reflect_on_plane(self, plane):
        """
        Reflect the vector about a plane.
        
        Args:
            plane (Plane): The plane of reflection
            
        Returns:
            Vector: The reflected vector
        """
        return Transformation.reflect_on_plane(self, plane)

    def __repr__(self):
        """String representation of the vector."""
        return f"Vector({self[0]}, {self[1]}, {self[2]})"

    def __str__(self):
        """Human-readable string representation."""
        return f"({self[0]}, {self[1]}, {self[2]})"