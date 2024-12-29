## Reading functions

- `sympy_value(value, name: str) -> sp.Expr`

  ```
  Convert a value into a sympy expression.

  Args:
      value (int | float | str | sp.Expr): The value to convert.
      name (str): A name used in error messages.

  Returns:
      sp.Expr: The converted value as a sympy expression.

  Raises:
      ValueError: If the input value is of an unsupported type.
  ```

- `expression(expression: str) -> sp.Expr`

  ```
  Parses a mathematical expression into a SymPy expression object.

  Args:
      expression (str): The mathematical expression in string format.

  Returns:
      sp.Expr: A SymPy expression object representing the parsed expression.
  ```

- `equation(equation: str) -> sp.Equality`

  ```
  Parses an equation into a SymPy equality object.

  Args:
      equation (str): The equation in string format.

  Returns:
      sp.Equality: A SymPy equality object representing the parsed equation.
  ```

- `read(input: str) -> sp.Expr | sp.Equality`

  ```
  Reads a mathematical input and determines if it's an expression or an equation.

  Args:
      input: The mathematical input in string format.

  Returns:
      sp.Expr | sp.Equality: A SymPy expression object if the input is an expression, or a SymPy equality object if the input is an equation.
  ```

### Examples

```python
from mathworld import sympy_value

# Test sympy_value with a float
n = 0.2
n_sympy = sympy_value(n)
print(n_sympy) # Expected output: 1/5
```

## Solving functions

- `solve_equation(_equation: str, variable: str = 'x') -> list[sp.Expr] | None`

  ```
  Solves a symbolic equation for a given variable.

  Args:
      _equation (str): The equation in string format.
      variable (str): The variable to solve for.

  Returns:
      tuple[sp.Expr] | None: A list of solutions as SymPy expressions.
      Return None if no real solutions exist or the equation is complex-valued.
  ```

- `solve_system(equations: list[str], variables: list[str]) -> tuple[tuple[sp.Expr]] | None`

  ```
  Solves a system of symbolic equations for multiple variables.

  Args:
      equations (str): A list of equations in string format.
      variables (str): A list of variables to solve for.

  Returns:
      tuple[tuple[sp.Expr]] | None: A tuple of solution tuples, where each inner tuple represents the solution values for the variables.
      Returns None if no real solutions exist.
  ```
