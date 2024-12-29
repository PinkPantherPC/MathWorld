__author__ = 'Tobia Petrolini'
__file__ = 'equations.py'

import sympy as sp


def expression(expression: str) -> sp.Expr:
    """
    Parses a mathematical expression into a SymPy expression object.

    Args:
        expression (str): The mathematical expression in string format.

    Returns:
        sp.Expr: A SymPy expression object representing the parsed expression.
    """
    return sp.parse_expr(expression, transformations='all')


def sympy_value(value, name: str = 'value') -> sp.Expr:
    """
    Convert a value into a sympy expression.

    Args:
        value (int | float | str | sp.Expr): The value to convert.
        name (str): A name used in error messages.

    Returns:
        sp.Expr: The converted value as a sympy expression.

    Raises:
        ValueError: If the input value is of an unsupported type.
    """
    if isinstance(value, int):
        value = sp.Integer(value)
    elif isinstance(value, float):
        value = sp.Rational(str(value))
    elif isinstance(value, sp.Expr):
        pass
    elif isinstance(value, str):
        value = expression(value)
    else:
        raise ValueError(
            f"{name} must be an integer, float, Rational, Expr or str")

    return value


def equation(equation: str) -> sp.Equality:
    """
    Parses an equation into a SymPy equality object.

    Args:
        equation (str): The equation in string format (e.g., "x + 2 = y").

    Returns:
        sp.Equality: A SymPy equality object representing the parsed equation.
    """
    lhs, rhs = equation.split("=")
    return sp.Eq(expression(lhs), expression(rhs))


def read(input: str) -> sp.Expr | sp.Equality:
    """
    Reads a mathematical input and determines if it's an expression or an equation.

    Args:
        input: The mathematical input in string format.

    Returns:
        sp.Expr | sp.Equality: A SymPy expression object if the input is an expression, or a SymPy equality object if the input is an equation.
    """
    if "=" in input:
        return equation(input)
    else:
        return expression(input)


def solve_equation(_equation: str, variable: str = 'x') -> tuple[sp.Expr] | None:
    """
    Solves a symbolic equation for a given variable.

    Args:
        _equation (str): The equation in string format.
        variable (str): The variable to solve for.

    Returns:
        tuple[sp.Expr] | None: A list of solutions as SymPy expressions.
        Return None if no real solutions exist or the equation is complex-valued.
    """
    symbol = sp.symbols(variable[0])
    solutions = tuple(sp.solveset(equation(_equation), symbol))
    return solutions if sp.im(solutions[0]) == 0 else None


def solve_system(equations: list[str], variables: list[str]) -> tuple[tuple[sp.Expr]] | None:
    """
    Solves a system of symbolic equations for multiple variables.

    Args:
        equations (str): A list of equations in string format.
        variables (str): A list of variables to solve for.

    Returns:
        tuple[tuple[sp.Expr]] | None: A tuple of solution tuples, where each inner tuple represents the solution values for the variables. 
        Returns None if no real solutions exist.
    """
    symbols = sp.symbols(variables)

    parsed_equations = [equation(eq) for eq in equations]

    solutions = sp.solve(parsed_equations, symbols, dict=True)

    real_solutions = []
    for sol in solutions:
        # Check if all solution values are real numbers (no imaginary part)
        if all(sp.im(val) == 0 for val in sol.values()):
            real_solutions.append(tuple(sol.values()))

    return tuple(real_solutions) if len(real_solutions) > 0 else None
