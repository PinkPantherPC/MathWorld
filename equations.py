__version__ = '0.1'
__author__ = 'Tobia Petrolini'

import re
import sympy as sp

def format_expression(expression: str, lower: bool = True) -> str:
    # Mapping of mathematical functions to Chinese characters
    function_mapping = {
        'cos': chr(21455),
        'sin': chr(21456),
        'tan': chr(21457),
        'acos': chr(21458),
        'asin': chr(21459),
        'atan': chr(21460),
        'cosh': chr(21461),
        'sinh': chr(21462),
        'tanh': chr(21463),
        'acosh': chr(21464),
        'asinh': chr(21465),
        'atanh': chr(21466),
        'exp': chr(21467),
        'log': chr(21468),
        'sqrt': chr(21469),
        'Abs': chr(21470)
    }

    # Replace functions with Chinese characters
    for func, char in function_mapping.items():
        expression = expression.replace(f'{func}(', char)

    # Standardize the expression
    expression = expression.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')  # e.g., [x] -> (x)
    expression = expression.replace('^', '**')  # e.g., x^2 -> x**2
    expression = expression.replace(')(', ')*(')  # e.g., )( -> )*(

    # Add multiplication signs where necessary
    expression = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', expression)  # e.g., 2x -> 2*x
    expression = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expression)  # e.g., x( -> x*(
    expression = re.sub(r'(\))([a-zA-Z(])', r'\1*\2', expression)  # e.g., )(y -> )*y
    expression = re.sub(r'(\))(\d+)', r'\1*\2', expression)  # e.g., )(2 -> )*2
    expression = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expression)  # e.g., xy -> x*y
    expression = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expression)
    expression = re.sub(r'(\d+)(\()', r'\1*\2', expression)  # e.g., 2( -> 2*(

    # Add multiplication signs for Chinese characters
    for char in function_mapping.values():
        expression = re.sub(r'([a-zA-Z0-9])(' + re.escape(char) + r')', r'\1*\2', expression)  # e.g., 2㐭 -> 2*㐭
        #expression = re.sub(r'(' + re.escape(char) + r')([a-zA-Z0-9])', r'\1*\2', expression)  # e.g., 㐭x -> 㐭*x

    # Remove unnecessary multiplication within parentheses
    expression = re.sub(r'\(\(([^()]+)\)\)', r'(\1)', expression)  # e.g., ((x)) -> (x)

    # Convert to lowercase if specified
    if lower:
        expression = expression.lower()

    # Revert Chinese characters back to function names
    for func, char in function_mapping.items():
        expression = expression.replace(f'{char}', f'{func}(')

    return expression


def find_variables(expression: str) -> tuple:
    # Find all variables in the expression
    variables = set(re.findall(r'[a-zA-Z]', expression))
    return tuple(variables)

def isexpression(expression: str) -> bool:
    # Check if the expression is valid
    try:
        sp.sympify(expression)
        return True
    except:
        return False

def is_sympy_expression(expression) -> bool:
    # Check if the expression is valid for sympy
    if isinstance(expression, sp.Expr):
        return True

def isequation(equation: str) -> bool:
    # Check if the equation is valid for sympy
    try:
        lhs, rhs = equation.split("=")
        sp.sympify(lhs)
        sp.sympify(rhs)
        return True
    except:
        return False

def is_sympy_equation(equation) -> bool:
    if isinstance(equation, sp.Equality):
        return True

def expression(expression: str) -> sp.Expr:
    # Convert the expression to a sympy expression
    symbols = find_variables(expression)
    for symbol in symbols:
        exec(symbol + " = sp.symbols('" + symbol + "')")
    return sp.sympify(expression)

def equation(equation: str) -> sp.Equality:
    # Convert the equation to sympy expressions
    lhs, rhs = equation.split("=")
    symbols = find_variables(equation)
    for symbol in symbols:
        exec(symbol + " = sp.symbols('" + symbol + "')")
    return sp.Eq(sp.sympify(lhs), sp.sympify(rhs))

def read_expression(_expression: str) -> sp.Expr:
    # Read the expression
    _expression = format_expression(_expression)
    if not isexpression(_expression):
        raise ValueError("Invalid expression")
    return expression(_expression)

def read_equation(_equation: str) -> sp.Equality:
    # Read the equation
    _equation = format_expression(_equation)
    if not isequation(_equation):
        raise ValueError("Invalid equation")
    return equation(_equation)

def read(input: str) -> sp.Expr:
    # Read the input
    if "=" in input:
        return read_equation(input)
    else:
        return read_expression(input)
    
    
