# ahcalc.py
(C) Alex Hurst, 2015

User-friendly arithmetic.

## Usage

- **On the command line**: `ahcalc`
    - You'll receive some usage tips and a REPL loop. Type any standard arithmetic notation to get the result.
- **As a Python module**: `import ahcalc`
    - When imported as a module, `ahcalc.calc(expression)` takes a string with an arithmetic expression, and returns the calculated value as a float.

ahcalc robustly supports whatever standard arithmetic notation you throw at it, including:

- Implied multiplication, such as '3(4+5)'
- Negated numbers or parentheses, such as '-4 * -(5+6)'
- Arbitrarily nested parentheses, such as '((5+3)*2)^(((-3/2)))'
- Mixed parentheses and square brackets
- The four basic operators, along with factorials (!) and exponents (^)
- Integers or floats

The parser is implemented from scratch in Python, and doesn't rely on Python's standard arithmetic operators, but it may behave similarly for many cases. Intelligent error messages are given for all syntax errors. Parentheses and brackets are recursively traversed.


Future improvements:

- Make the command line more user-friendly (history, chained evaluations, etc)
- Accommodate very large numbers: prevent overflow errors, and return scientific notation when the number of digits is unreasonable.
