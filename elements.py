__version__ = '0.1'
__author__ = 'Tobia Petrolini'

from equations import *

def sympy_value(value, name: str = 'value') -> sp.Expr:
    if isinstance(value, int):
        value = sp.simplify(sp.Integer(value))
    elif isinstance(value, sp.Integer):
        value = sp.simplify(value)
    elif isinstance(value, float):
        value = sp.simplify(sp.Rational(value))
    elif isinstance(value, sp.Rational):
        value = sp.simplify(value)
    elif isinstance(value, sp.Expr):
        pass
    elif isinstance(value, str):
        value = read_expression(value)
    else:
        raise ValueError(f"{name} must be an integer, float, Rational, Expr or str")
    
    return value

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
    
    def isonXaxe(self) -> bool:
        return float(self.y) == 0
    
    def isonYaxe(self) -> bool:
        return float(self.x) == 0
        
    def distancePoint(self, point: 'Point') -> sp.Expr:
        return sp.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

    def distanceLine(self, line: 'Line') -> sp.Expr:
        return sp.Abs(line.a*self.x + line.b*self.y + line.c) / sp.sqrt(line.a**2 + line.b**2)
        
    def ison(self, element) -> bool:
        if isinstance(element, Point):
            return element.cordinates == self.cordinates
        elif isinstance(element, Line):
            return sp.simplify(f'{self.y} - ({element.slope} * {self.x} + {element.intercept})') == 0
            

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

            # Ensure directEquation maintains integers when possible
            lhs, rhs = self.equation.lhs, self.equation.rhs
            lcm_denoms = sp.lcm([term.as_numer_denom()[1] for term in (lhs - rhs).as_ordered_terms()])
            scaled_lhs = (lhs - rhs) * lcm_denoms

            self.directEquation = sp.Eq(scaled_lhs.simplify(), 0)
            
            self.slope = sp.simplify(sp.diff(self.equation.rhs, sp.Symbol('x')))
            
            self.intercept = sp.solve(self.equation, 'y')[0].subs('x', 0)

            x, y = sp.symbols('x y')

            self.a = self.directEquation.lhs.as_coefficients_dict().get(x, 0)
            self.b = self.directEquation.lhs.as_coefficients_dict().get(y, 0)
            self.c = self.directEquation.lhs.as_coefficients_dict().get(1, 0)

        else:
            self.equation = sp.Eq(expression('x'), expression(str(sp.solve(self.equation, 'x')[0])))
            
            # Ensure directEquation maintains integers when possible
            lhs, rhs = self.equation.lhs, self.equation.rhs
            lcm_denoms = sp.lcm([term.as_numer_denom()[1] for term in (lhs - rhs).as_ordered_terms()])
            scaled_lhs = (lhs - rhs) * lcm_denoms

            self.directEquation = sp.Eq(scaled_lhs.simplify(), 0)

            x = sp.symbols('x')

            self.a = self.directEquation.lhs.as_coefficients_dict().get(x, 0)
            self.b = sp.Integer(0)
            self.c = self.directEquation.lhs.as_coefficients_dict().get(1, 0)

            self.slope = sp.oo
            self.intercept = None

    def __str__(self) -> str:
        return f'{self.equation.lhs} = {self.equation.rhs}'
    
    def isXaxe(self) -> bool:
        return self.slope == 0
    
    def isYaxe(self) -> bool:
        return self.slope == sp.oo

    def isParallel(self, line: 'Line') -> bool:
        return self.slope == line.slope
    
    def isPerpendicular(self, line: 'Line') -> bool:
        return self.slope * line.slope == -1

    def isAxe(self) -> bool:
        ...

    def isBisector(self) -> bool:
        ...

    def isMedian(self) -> bool:
        ...


BISECTOR1_3 = Line(equation('y = x'))
BISECTOR2_4 = Line(equation('y = -x'))
    
def findLine(Point1: Point = None, Point2: Point = None , slope = None, intercept = None, isvertical: bool = False) -> Line:
    if intercept is not None:
        intercept = sympy_value(intercept, 'intercept')

    if isvertical:
        if Point1 is not None and Point2 is not None:
            pass
        elif Point1 is not None and intercept is not None:
            Point2 = Point(intercept, 0)
        elif Point2 is not None and intercept is not None:
            Point1 = Point(intercept, 0)
        else:
            raise ValueError("Two of the three parameters (Point1, Point2, intercept) must be provided")
        
        return Line(sp.Eq(expression('x'), Point1.x))
    else:
        if slope is not None:
            slope = sympy_value(slope, 'slope')

        if Point1 is not None and Point2 is not None:
            if Point1.x == Point2.x:
                return Line(sp.Eq(expression('x'), Point1.x))
            else:
                slope = (Point2.y - Point1.y) / (Point2.x - Point1.x)
                intercept = Point1.y - slope * Point1.x
        elif Point1 is not None and slope is not None:
            intercept = Point1.y - slope * Point1.x
        elif Point1 is not None and intercept is not None:
            slope = (Point1.y - intercept) / Point1.x
        elif Point2 is not None and slope is not None:
            intercept = Point2.y - slope * Point2.x
        elif Point2 is not None and intercept is not None:
            slope = (Point2.y - intercept) / Point2.x
        else:
            raise ValueError("Two of the four parameter must be given")

    return Line(sp.Eq(expression('y'), slope*expression('x') + intercept)) ### DA SISTEMARE

class Segment:

    def __init__(self, Point1: Point, Point2: Point):
        self.Point1 = Point1
        self.Point2 = Point2

        self.length = sp.sqrt((self.Point2.x - self.Point1.x)**2 + (self.Point2.y - self.Point1.y)**2)

        self.middle = Point((self.Point1.x + self.Point2.x) / 2, (self.Point1.y + self.Point2.y) / 2)

    def line(self) -> Line:
        return findLine(self.Point1, self.Point2)



