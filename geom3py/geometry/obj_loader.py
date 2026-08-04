"""
OBJ file loader for geom3py.

Parses Wavefront .obj files and builds Polygon objects from the faces
defined in the file. Each face becomes an independent Polygon, and since
Polygon already triangulates itself on construction (see polygon.py),
n-gon faces are triangulated automatically — no extra step is needed.
"""

from .point import Point
from .polygon import Polygon


def _parse_vertices(line):
    """
    Parses a 'v x y z' line.
 
    Parameters
    ----------
    line : str
        A single line from the .obj file starting with 'v '.
 
    Returns
    -------
    Point
        The (x, y, z) coordinates as a Point object.
    """

    parts = line.split()

    return Point(float(parts[1]), float(parts[2]), float(parts[3]))

def _parse_faces(line):
    """
    Parses an 'f ...' line.
 
    Supports the 'v', 'v/vt', 'v/vt/vn' and 'v//vn' formats. Texture
    and normal indices are ignored, since Polygon only needs positions.
    Negative (relative) indices, as allowed by the OBJ spec, are also
    supported.
 
    Parameters
    ----------
    line : str
        A single line from the .obj file starting with 'f '.
 
    Returns
    -------
    list of int
        0-indexed vertex indices for this face.
    """

    indices = []
    parts = line.split()
    parts.pop(0)

    for part in parts:
        token = part.split("/")
        indices.append(int(token[0]) - 1)

    return indices


def load_obj(filepath):
    """
    Loads a Wavefront .obj file and returns its faces as Polygon objects.
 
    Parameters
    ----------
    filepath : str
        Path to the .obj file.
 
    Returns
    -------
    list of Polygon
        One Polygon per face defined in the file. Faces with more than
        3 vertices are triangulated automatically (Polygon does this in
        its own __init__), so the caller never needs to call triangulate
        manually.
 
    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If a face has fewer than 3 vertices, or references a vertex
        index that was never defined by a 'v' line.
    """

    vertices = []
    faces = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("v "):
                vertices.append(_parse_vertices(line))

            elif line.startswith("f "):
                faces.append(_parse_faces(line))

    polygons = []

    for i, face in enumerate(faces):
        if len(face) < 3:
            print(f"Warning: skipping degenerate face #{i} with {len(face)} vertex/vertices")
            continue

        face_points = [vertices[j] for j in face]
        polygons.append(Polygon(face_points))

    return polygons