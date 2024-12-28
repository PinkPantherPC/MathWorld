import pytest
from mathworld import Point, Line, Segment, sp


def test_point():
    # Test Point class
    p1 = Point(3, 4)
    p2 = Point(-3, -4)

    assert str(p1) == "(3, 4)"
    assert not p1.isorigin()
    assert p2.quadrant == 3
    assert p1.distancePoint(p2) == sp.sqrt((3 - (-3))**2 + (4 - (-4))**2)

    line = Line("y = 2*x + 1")
    assert p1.distanceLine(line) == sp.Abs(-2*3 + 4 - 1) / sp.sqrt(2**2 + 1**2)

    segment = Segment(Point(0, 0), Point(6, 8))
    assert p1.ison(segment)
    assert not p2.ison(segment)

    p1 = Point(1, 2)
    p2 = Point(3, 4)

    distance = sp.sqrt(2)
    new_points = Point.findPoint(line, p1, distance)
    assert len(new_points) == 2
    for p in new_points:
        assert p.distancePoint(p1) == distance


def test_line():
    # Test Line class
    line1 = Line("y = 2*x + 3")
    line2 = Line("y = -1*x/2 - 2")

    assert line1.isHorizontal() is False
    assert line2.isVertical() is False
    assert line1.isParallel(Line("y = 2*x + 7"))
    assert line1.isPerpendicular(line2)

    intersection = line1.intersection(line2)
    assert intersection.x == sp.Integer(
        -2) and intersection.y == sp.Integer(-1)

    p1 = Point(1, 2)
    p2 = Point(3, 4)

    line = Line.findLine(p1, p2)
    assert line.slope == sp.Rational(2, 2)
    assert line.intercept == 1


def test_segment():
    # Test Segment class
    p1 = Point(0, 0)
    p2 = Point(6, 8)
    segment = Segment(p1, p2)

    assert segment.length == sp.sqrt(6**2 + 8**2)
    assert str(segment.middle) == "(3, 4)"
    assert segment.line.slope == sp.Rational(4, 3)

    perp_line = segment.axe
    assert perp_line.isPerpendicular(segment.line)
