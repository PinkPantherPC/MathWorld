# MathWorld

A python module for using sympy with analytic geometry

To install _mathworld_ you can use pip (if you already have python installed) by typing the following command in your terminal

```bash
pip install mathworld
```

Alternatively, you can download it from this repo (_src\mathworld_)

## `class Point`

### Attributes

- `x`: The x-coordinate of the point.
- `y`: The y-coordinate of the point.
- `cordinates`: A tuple representing the x and y coordinates.
- `quadrant`: The quadrant of the Cartesian plane the point lies in.

### Methods

- `__init__(x, y)`:
  ```
  Initializes the Point object with x and y coordinates.
  ```
- `__str__() -> str`:
  ```
  Returns a string representation of the coordinates.
  ```
- `isorigin() -> bool`:

  ```
  Checks if the point is the origin.

  Returns:
      bool: True if the point is the origin, False otherwise.
  ```

- `distancePoint(point: 'Point') -> sp.Expr`:

  ```
  Calculate the Euclidean distance to another point.

  Args:
      point (Point): The other point to calculate the distance from.

  Returns:
      sp.Expr: The distance as a SymPy expression.
  ```

- `distanceLine(line: 'Line') -> sp.Expr`:

  ```
  Calculate the perpendicular distance from the point to a line.

  Args:
      line (Line): The line to calculate the distance from.

  Returns:
      sp.Expr: The distance as a SymPy expression.
  ```

- `ison(element) -> bool`:

  ```
  Determine if the point lies on a given geometric element.

  Args:
      element: The geometric element (Point, Line, or Segment).

  Returns:
      bool: True if the point lies on the element.
  ```

### Example

```python
from mathworld import Point

# Create a Point object at coordinates (3, 4)
point1 = Point(3, 4)
print(point1)  # Expected output: (3, 4)

# Check if point1 is the origin
is_origin = point1.isorigin()
print(is_origin)  # Expected output: False

# Create another Point object at (0, 0)
point2 = Point(0, 0)

# Calculate the distance between point1 and point2
distance = point1.distancePoint(point2)
print(distance)  # Expected output: 5
```

## `class Line`

### Attributes

- `equation`: The equation of the line (can be explicit or implicit).
- `implicitEquation`: The implicit equation of the line.
- `slope`: The slope of the line.
- `intercept`: The y-intercept of the line.
- `a`, `b`, `c`: Coefficients for the implicit line equation `ax + by + c = 0`.

### Methods

- `__init__(equation)`:

  ```
  Initializes the Line object from an equation.

  Args:
      equation (str | sp.Equality): The equation defining the line.

  Raises:
      ValueError: If the provided equation format is invalid.
  ```

- `__str__() -> str`:
  ```
  Returns the equation of the line as a string.
  ```
- `isHorizontal() -> bool`:

  ```
  Check if the line is horizontal.

  Returns:
      bool: True if the line is horizontal.
  ```

- `isVertical() -> bool`:

  ```
  Check if the line is vertical.

  Returns:
      bool: True if the line is vertical.
  ```

- `isParallel(line: 'Line') -> bool`:

  ```
  Check if the line is parallel to another line.

  Args:
      line (Line): The other line.

  Returns:
      bool: True if the lines are parallel.
  ```

- `isPerpendicular(line: 'Line') -> bool`:

  ```
  Check if the line is perpendicular to another line.

  Args:
      line (Line): The other line.

  Returns:
      bool: True if the lines are perpendicular.
  ```

- `intersection(line: 'Line') -> Point`:

  ```
  Calculate the intersection point with another line.

  Args:
      line (Line): The other line.

  Returns:
      Point: The intersection point.
  ```

- `isAxe(segment: 'Segment') -> bool`:

  ```
  Check if the line is the axis of a given segment.

  Args:
      segment (Segment): The segment to check.

  Returns:
      bool: True if the line is the axis of the segment.
  ```

- `isBisector(line1: 'Line', line2: 'Line') -> bool`:

  ```
  Check if the line is the bisector of two lines.

  Args:
      line1 (Line): The first line.
      line2 (Line): The second line.

  Returns:
      bool: True if the line is the bisector of the two lines.
  ```

- `findParallel(point: Point) -> 'Line'`:

  ```
  Find a parallel line that passes through a given point.

  Args:
      point (Point): The point through which the parallel line passes.

  Returns:
      Line: The parallel line.
  ```

- `findPerpendicular(point: Point) -> 'Line'`:

  ```
  Find a perpendicular line that passes through a given point.

  Args:
      point (Point): The point through which the perpendicular line passes.

  Returns:
      Line: The perpendicular line.
  ```

- `findBisector(line: 'Line') -> tuple['Line', 'Line']`:

  ```
  Find the bisectors of the angles formed between the current line and another line.

  Args:
      line (Line): The other line.

  Returns:
      tuple[Line, Line]: The two angle bisectors as lines.
  ```

### Example

```python
from mathworld import Line

# Create a Line object from an equation
line_eq = Line('y - 1 = 2x')
print(line_eq)  # Expected output: y = 2*x + 1

# Check if line_eq is horizontal
is_horizontal = line_eq.isHorizontal()
print(is_horizontal)  # Expected output: False

# Create another Line object representing y = -x + 5
line2 = Line('y = -x + 5')

# Find intersection of two lines
intersection_point = line_eq.intersection(line2)
print(intersection_point)  # Expected output: (4/3, 11/3)
```

## `class Segment`

### Attributes

- `point1`: The first endpoint of the segment.
- `point2`: The second endpoint of the segment.
- `length`: The length of the segment.
- `middle`: The midpoint of the segment.
- `line`: The line containing the segment.
- `axe`: The perpendicular bisector of the segment.

### Methods

- `__init__(point1: Point, point2: Point)`:

  ```
  Initializes the Segment object with two points.

  Args:
      point1 (Point): The first endpoint of the segment.
      point2 (Point): The second endpoint of the segment.
  ```

### Example

```python
from mathworld import Point, Segment

# Create two Point objects for segment endpoints
pointA = Point(1, 2)
pointB = Point(4, 6)

# Initialize a Segment object with these points
segment = Segment(pointA, pointB)
print(segment.length)  # Expected output: 5
```

## External Functions

### `findLine(point1, point2, slope, intercept) -> Line`

```python
Generate a line based on given parameters.

Args:
    point1 (Point | None): The first point on the line.
    point2 (Point | None): The second point on the line.
    slope: The slope of the line.
    intercept: The y-intercept of the line.

Returns:
    Line: The constructed line object.

Raises:
    ValueError: If sufficient parameters are not provided.
```

### `findPoint(line, point, distance) -> tuple[Point, Point]`

```python
Finds two points on a given line at a specific distance from a reference point.

Args:
    line (Line): The line on which to find the points.
    point (Point): The reference point.
    distance: The desired distance from the reference point.

Returns:
    tuple[Point, Point]: A tuple containing two points at the given distance.

Raises:
    ValueError: If the reference point is not on the line.
```

### Examples

```python
from mathworld import Point, Line, findLine, findPoint

# Create two Point objects to define a line
pointA = Point(1, 1)   # First point at (1, 1)
pointB = Point(4, 3)   # Second point at (4, 3)

# Using findLine with two points to create a line equation
line_eq = findLine(pointA, pointB)
print(line_eq)  # Expected output: y = 2*x/3 + 1/3

pointA = Point(3, 2)
line = Line('y = -x + 5')

# Find one of the two points on the line at distance of 2 from pointA
points_at_distance = findPoint(line, pointA, 2)
print(points_at_distance[0])  # Expected output: (3 - sqrt(2), sqrt(2) + 2)
```

---

### Constants

- `ORIGIN`: A predefined point at (0, 0).
- `X_AXE`: Line representing the x-axis.
- `Y_AXE`: Line representing the y-axis.
- `BISECTOR_1_3`, `BISECTOR_2_4`: Lines representing specific angle bisectors of quadrants.

## Acknowledgments

This project makes use of [SymPy](https://www.sympy.org), a Python library for symbolic mathematics.

I gratefully acknowledge the developers and contributors of SymPy for their exceptional work in creating and maintaining this robust and versatile computational tool. SymPy is released under the [BSD license](https://github.com/sympy/sympy/blob/master/LICENSE).
