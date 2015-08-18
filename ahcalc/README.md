# ahcalc
(C) Alex Hurst, 2015

When run on the command line, ahcalc presents a usage message and waits for user input. The user may type an arithmetic string to be evaluated.

When imported as a module, the calc() function can be called with a string as argument, and it will return the calculated value as a float.

Features supported are:

- Implied multiplication, such as '3(4+5)'
- Negated numbers or parentheses, such as '-4 * -(5+6)'
- Arbitrarily nested parentheses, such as '((5+3)*2)^(((-3/2)))'
- Mixed parentheses and square brackets
- The four basic operators, along with factorials (!) and exponents (^)
- Integers or floats

Future improvements:

- Make the command line more user-friendly (history, etc)
- Accommodate very large numbers