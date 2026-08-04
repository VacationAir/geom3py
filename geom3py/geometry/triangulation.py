from .triangle import Triangle
from .point import Point
from .line import Line


def triangulate(polygon):
    """
    Triangulates a polygon using the Ear Clipping algorithm.

    Converts a polygon into a list of triangles by repeatedly finding
    and removing "ears" (convex vertices with empty triangles).

    Parameters
    ----------
    polygon : Polygon
        The polygon to triangulate. Must be coplanar and have at least
        3 vertices.

    Returns
    -------
    list of Triangle
        A list of triangles that exactly cover the polygon's area.

    Raises
    ------
    ValueError
        If no ear can be found (usually means the polygon is not simple
        or has self-intersections).

    Notes
    -----
    This function is called automatically by Polygon.__init__, so most
    users never need to call it directly.

    For a polygon with N vertices, the result contains exactly N-2
    triangles.

    Examples
    --------
    >>> from geom3py import Polygon, triangulate
    >>> poly = Polygon([[0,0,0], [1,0,0], [1,1,0], [0,1,0]])
    >>> triangles = triangulate(poly)
    >>> len(triangles)
    2
    """
    if polygon.n == 3:
        return [Triangle(*polygon.vertices)]
    
    vertices = list(polygon.vertices)
    if polygon.normal_vector is not None:
        normal = polygon.normal_vector
    else:
        normal = polygon.newell_normal

    triangles = []

    while len(vertices) > 3:
        triangle = _find_ear(vertices, normal)

        if triangle is None:
            raise ValueError("Couldn't find any ear")

        vertices.remove(triangle.points[1])
        triangles.append(triangle)
        
    triangles.append(Triangle(*vertices))
    return triangles


def _find_ear(vertices, normal):
    """
    Finds an ear in a polygon.

    An ear is a vertex that is convex and whose triangle with its
    immediate neighbors contains no other vertices.

    Parameters
    ----------
    vertices : list of Point
        The vertices of the polygon in order.
    normal : Vector
        The normal vector of the polygon's plane, used to determine
        convexity.

    Returns
    -------
    Triangle or None
        The triangle formed by the ear vertex and its two neighbors,
        or None if no ear is found.

    Notes
    -----
    This is the core of the Ear Clipping algorithm. A vertex is considered
    convex if the cross product of its adjacent edges points in the same
    direction as the polygon's normal.

    The triangle is considered empty if no other vertex lies inside it.
    """
    n = len(vertices)

    for i in range(n):
        prev_idx = (i - 1) % n
        next_idx = (i + 1) % n
        
        A = vertices[prev_idx]
        B = vertices[i]
        C = vertices[next_idx]
        cross = (B - A).cross(C - B)

        # Check convexity: cross product must point in normal direction
        if cross.dot(normal) <= 0:
            continue

        is_ear = True
        triangle = Triangle(A, B, C)
        
        for P in vertices:
            # Skip the three vertices that form the ear
            if not P.equals(A) and not P.equals(B) and not P.equals(C):
                d1 = (B - A).cross(P - A).dot(normal)
                d2 = (C - B).cross(P - B).dot(normal)
                d3 = (A - C).cross(P - C).dot(normal)

                # If P has mixed signs, it's outside the triangle
                has_neg = d1 < 0 or d2 < 0 or d3 < 0
                has_pos = d1 > 0 or d2 > 0 or d3 > 0

                # If not (has_neg and has_pos), all signs are equal -> P is inside
                if not (has_neg and has_pos):
                    is_ear = False
                    break

        if is_ear:            
            return triangle

    return None