<p align="center">

![Pure Python](https://img.shields.io/badge/Pure-Python-3776AB?logo=python&logoColor=white)
![3D Geometry](https://img.shields.io/badge/3D-Analytical%20Geometry-2E7D32)
![Custom Vector Engine](https://img.shields.io/badge/Vector%20Engine-Custom-00695C)
![Object-Oriented](https://img.shields.io/badge/API-Object--Oriented-1565C0)
![No Dependencies](https://img.shields.io/badge/Dependencies-None-success)
![Unit Tests](https://img.shields.io/badge/120%2B-Unit%20Tests-success)
![MIT License](https://img.shields.io/badge/License-MIT-6A1B9A)

</p>

# Geom3py

**geom3py** is a library developed entirely in **Pure Python** for analytical geometry calculations in three-dimensional space. It features its own vector and linear algebra engine and provides an object-oriented API for **vectors, points, lines, planes and faces** including geometric transformations such as **scaling, rotation, translation and reflection**.

The library has no external dependencies and is suitable for teaching and study as well as a foundation for geometric applications, visualization or CAD-related projects.

---

# Features

## Vectors (`Vector`)

* Vector addition and subtraction
* Scalar multiplication
* Magnitude
* Dot product
* Cross product
* Normalization
* Angle calculation
* Transformations

  * Scale
  * Translate
  * Rotate
  * Reflect on point
  * Reflect on line
  * Reflect on plane

---

## Points (`Point`)

* Creation of points in ℝ³
* Distance between points
* Direction vector between two points
* All geometric transformations

---

## Lines (`Line`)

* Creation from

  * two points
  * support and direction vector
* Calculation of any point on the line
* Foot point of a point
* Intercept points
* Distances to

  * points
  * lines
* Intersection with lines
* Positional relationships

  * identical
  * parallel
  * intersecting
  * skew
* Angle calculations
* Geometric transformations

---

## Planes (`Plane`)

* Creation from

  * point and normal vector
  * point and two direction vectors
* Foot point of a point
* Intersection line of two planes
* Intersection with lines
* Intercept points
* Distances to

  * points
  * lines
  * planes
* Intersection angles
* Positional relationships

  * identical
  * parallel
  * intersecting
* Geometric transformations

---

## Faces (`Face`)

Representation of bounded planar quadrilaterals.

Supports among others:

* Center point
* Perimeter
* Area
* Normal vector
* Point-in-face test
* Positional relationships between faces

  * identical
  * parallel
  * intersecting
  * outside
  * coplanar intersecting
  * coplanar outside
  * on edge
  * touching
  * edge intersecting
* Distance between faces
* Intersection point (if unique)
* Geometric transformations

---

# Properties

* ✅ Completely in **Pure Python**
* ✅ No external dependencies
* ✅ Custom vector engine
* ✅ Custom linear algebra helper functions
* ✅ Object-oriented API
* ✅ Numerically robust calculations using custom tolerance functions
* ✅ Geometric transformations for all objects
* ✅ Extensive unit tests
* ✅ Suitable for teaching, study and technical applications

---

# Installation

```bash
pip install geom3py
```
---

# 📚 Examples

## Basic Geometry

```python
from geom3py import Point, Line

A = Point([0, 0, 0])
B = Point([2, 2, 2])

g = Line.from_points(A, B)

print(A.distance_to_point(B))
print(g.point_at(0.5))
print(g.contains_point(A))
```

---

## Planes

```python
from geom3py import Point, Plane

E = Plane([1, 2, 3], [1, 1, 1])
P = Point([4, 5, 6])

print(E.distance_point(P))
print(E.contains_point(P))
print(E.intercept_points())
```

---

## Transformations

```python
from geom3py import Line

g = Line(Point(1, 2, 3), Point(1, 0, 0))

g2 = g.scale(2)
g3 = g.translate(Point(5, 0, 0))
g4 = g.rotate(90, "z")
g5 = g.reflect_on_point(Point(0, 0, 0))
```

---

## Face

```python
from geom3py import Point, Face

face = Face(
    [0, 0, 0],
    [10, 0, 0],
    [10, 8, 0],
    [0, 8, 0]
)

print(face.area())
print(face.perimeter())
print(face.center)

P = Point([5, 4, 0])
print(face.contains_point(P))
```

---

## Intersection Between Line and Plane

```python
from geom3py import Line, Plane

g = Line([0, 0, 0], [1, 1, 1])
E = Plane([1, 0, 0], [0, 1, 0])

print(E.position_line(g))
print(E.intersection_line(g))
```

---

## Angle Calculations

```python
from geom3py import Line, Plane

g1 = Line([0, 0, 0], [1, 0, 0])
g2 = Line([0, 0, 0], [1, 1, 0])

print(g1.angle_lines(g2, deg=True))

E = Plane([0, 0, 0], [0, 0, 1])
print(E.angle_line(g1, deg=True))

E2 = Plane([0, 0, 0], [1, 1, 0])
print(E.angle_plane(E2, deg=True))
```

---

## Dependencies

* Python ≥ 3.10

---

## License

MIT License.
