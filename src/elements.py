__author__ = 'Tobia Petrolini'
__file__ = 'elements.py'

from equations import *

class Point():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.x = sympy_value(self.x, 'x')
        
        self.y = sympy_value(self.y, 'y')
        
        self.cordinates = self.x, self.y

        if float(self.x) > 0 and float(self.y) > 0:
            self.quadrant = 1
        elif float(self.x) < 0 and float(self.y) > 0:
            self.quadrant = 2
        elif float(self.x) < 0 and float(self.y) < 0:
            self.quadrant = 3
        elif float(self.x) > 0 and float(self.y) < 0:
            self.quadrant = 2

    def __str__(self) -> str:
        return f"{self.cordinates}"
    
    def isorigin(self) -> bool:
        return float(self.x) == 0 and float(self.y) == 0
        
    def distancePoint(self, point: 'Point') -> sp.Expr:
        return sp.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

    def distanceLine(self, line: 'Line') -> sp.Expr:
        return sp.Abs(line.a*self.x + line.b*self.y + line.c) / sp.sqrt(line.a**2 + line.b**2)
        
    def ison(self, element) -> bool:
        if isinstance(element, Point):
            return element.cordinates == self.cordinates
        elif isinstance(element, Line):
            return sp.simplify(element.a * self.x + element.b * self.y + element.c) == 0
        elif isinstance(element, Segment):
            min_x = min(element.point1.x, element.point2.x)
            max_x = max(element.point1.x, element.point2.x)
            min_y = min(element.point1.y, element.point2.y)
            max_y = max(element.point1.y, element.point2.y)
            return self.ison(element.line) and (self.x >= min_x and self.x <= max_x) and (self.y >= min_y and self.y <= max_y)
            
ORIGIN = Point(sp.Integer(0), sp.Integer(0))

class Line():

    def __init__(self, equation):
        self.equation = equation
        if isinstance(self.equation, str):
            self.equation = read_equation(self.equation)
        elif isinstance(self.equation, sp.Equality):
            pass
        else:
            raise ValueError("equation must be an Equality or str")
        
        if 'y' in str(self.equation):
            self.equation = sp.Eq(expression('y'), expression(str(sp.solve(self.equation, 'y')[0])))

            lhs, rhs = self.equation.lhs, self.equation.rhs
            lcm_denoms = sp.lcm([term.as_numer_denom()[1] for term in (lhs - rhs).as_ordered_terms()])
            scaled_lhs = (lhs - rhs) * lcm_denoms

            self.implicitEquation = sp.Eq(scaled_lhs.simplify(), 0)
            
            self.slope = sp.simplify(sp.diff(self.equation.rhs, sp.Symbol('x')))
            
            self.intercept = sp.solve(self.equation, 'y')[0].subs('x', 0)

            x, y = sp.symbols('x y')

            self.a = self.implicitEquation.lhs.as_coefficients_dict().get(x, 0)
            self.b = self.implicitEquation.lhs.as_coefficients_dict().get(y, 0)
            self.c = self.implicitEquation.lhs.as_coefficients_dict().get(1, 0)

        else:
            self.equation = sp.Eq(expression('x'), expression(str(sp.solve(self.equation, 'x')[0])))
            
            # Ensure implicitEquation maintains integers when possible
            lhs, rhs = self.equation.lhs, self.equation.rhs
            lcm_denoms = sp.lcm([term.as_numer_denom()[1] for term in (lhs - rhs).as_ordered_terms()])
            scaled_lhs = (lhs - rhs) * lcm_denoms

            self.implicitEquation = sp.Eq(scaled_lhs.simplify(), 0)

            x = sp.symbols('x')

            self.a = self.implicitEquation.lhs.as_coefficients_dict().get(x, 0)
            self.b = sp.Integer(0)
            self.c = self.implicitEquation.lhs.as_coefficients_dict().get(1, 0)

            self.slope = sp.oo
            self.intercept = None

    def __str__(self) -> str:
        return f'{self.equation.lhs} = {self.equation.rhs}'
    
    def isHorizontal(self) -> bool:
        return self.slope == 0
    
    def isVertical(self) -> bool:
        return self.slope == sp.oo

    def isParallel(self, line: 'Line') -> bool:
        return self.slope == line.slope
    
    def isPerpendicular(self, line: 'Line') -> bool:
        return self.slope * line.slope == -1
    
    def intersection(self, line: 'Line') -> Point:
        x, y = sp.symbols('x y')
        sol = sp.solve([self.equation, line.equation], (x, y))
        return Point(sol[x], sol[y])

    def isAxe(self, segment: 'Segment') -> bool:
        return str(self.equation) == str(segment.axe.equation)
            
    def isBisector(self, line1: 'Line', line2: 'Line') -> bool:
        intersection_point = line1.intersection(line2)

        test_point = Point(intersection_point.x + 1, intersection_point.y + self.slope) if not self.isVertical() else Point(intersection_point.x, intersection_point.y + 1)

        distance_to_line1 = test_point.distanceLine(line1)
        distance_to_line2 = test_point.distanceLine(line2)

        return sp.simplify(distance_to_line1 - distance_to_line2) == 0

    def findParallel(self, point: Point) -> 'Line':
        if self.isVertical():
            return Line(sp.Eq(expression('x'), point.x))
        else:
            intercept = point.y - self.slope * point.x
            return Line(sp.Eq(expression('y'), self.slope * expression('x') + intercept))

    def findPerpendicular(self, point: Point) -> 'Line':
        if self.isVertical():
            return Line(sp.Eq(expression('y'), point.y))
        elif self.isHorizontal():
            return Line(sp.Eq(expression('x'), point.x))
        else:
            perpendicular_slope = -1 / self.slope
            intercept = point.y - perpendicular_slope * point.x
            return Line(sp.Eq(expression('y'), perpendicular_slope * expression('x') + intercept))

    def findBisector(self, line: 'Line') -> tuple['Line', 'Line']:
        x, y = sp.symbols('x y')

        distance_self = (self.a * x + self.b * y + self.c) / sp.sqrt(self.a**2 + self.b**2)
        distance_line = (line.a * x + line.b * y + line.c) / sp.sqrt(line.a**2 + line.b**2)

        eq1 = sp.Eq(distance_self, distance_line)
        eq2 = sp.Eq(distance_self, -distance_line)

        if not self.isVertical():
            solutions1 = sp.solve(eq1, y)
            solutions2 = sp.solve(eq2, y)
            solutions = solutions1 + solutions2
        else:
            solutions1 = sp.solve(eq1, x)
            solutions2 = sp.solve(eq2, x)
            solutions = solutions1 + solutions2

        if len(solutions) == 2:
            line1 = Line(sp.Eq(y, solutions[0])) if not self.isVertical() else Line(sp.Eq(x, solutions[0]))
            line2 = Line(sp.Eq(y, solutions[1])) if not self.isVertical() else Line(sp.Eq(x, solutions[1]))
            return line1, line2
        else:
            return Line(sp.Eq(y, solutions[0])) if not self.isVertical() else Line(sp.Eq(x, solutions[0]), None)


X_AXE = Line(equation('y = 0'))
Y_AXE = Line(equation('x = 0'))
BISECTOR_1_3 = Line(equation('y = x'))
BISECTOR_2_4 = Line(equation('y = -x'))
    
def findLine(point1: Point | None = None, point2:  Point | None = None , slope = None, intercept = None) -> Line:
    isvertical = False
    try:
        if slope == sp.oo or point1.x == point2.x:
            isvertical = True
    except:
        pass

    if intercept is not None:
        intercept = sympy_value(intercept, 'intercept')

    if isvertical:
        if point1 is not None:
            return Line(sp.Eq(expression('x'), point1.x))
        elif point2 is not None:
            return Line(sp.Eq(expression('x'), point2.x))
        elif intercept is not None:
            return Line(sp.Eq(expression('x'), intercept))
        else:
            raise ValueError("One of the three parameter (point1, Pont2, intercept) must be given")
        
    else:
        if slope is not None:
            slope = sympy_value(slope, 'slope')

        if point1 is not None and point2 is not None:
            slope = (point2.y - point1.y) / (point2.x - point1.x)
            intercept = point1.y - slope * point1.x
        elif point1 is not None and slope is not None:
            intercept = point1.y - slope * point1.x
        elif point1 is not None and intercept is not None:
            slope = (point1.y - intercept) / point1.x
        elif point2 is not None and slope is not None:
            intercept = point2.y - slope * point2.x
        elif point2 is not None and intercept is not None:
            slope = (point2.y - intercept) / point2.x
        elif slope is not None and intercept is not None:
            pass
        else:
            raise ValueError("Two of the four parameter must be given")

    return Line(sp.Eq(expression('y'), slope*expression('x') + intercept))

class Segment:

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

        self.length = self.point1.distancePoint(self.point2)

        self.middle = Point((self.point1.x + self.point2.x) / 2, (self.point1.y + self.point2.y) / 2)

        self.line = findLine(self.point1, self.point2)

        self.axe = self.line.findPerpendicular(self.middle)

def findPoint(line: Line, point: Point, distance) -> tuple[Point, Point]:
    if point.ison(line):
        distance = sympy_value(distance, 'distance')

        equation1 = equation('(x - p)**2 + (y - q)**2 = d**2').subs('p', point.x).subs('q', point.y).subs('d', distance)

        x, y = sp.symbols('x y')
        sol = sp.solve([equation1, line.equation], (x, y))
        
        return Point(sol[0][0], sol[0][1]), Point(sol[1][0], sol[1][1])
    else:
        raise ValueError("The point must be on the line")
