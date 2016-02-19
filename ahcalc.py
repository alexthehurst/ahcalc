#!/usr/bin/env python
# coding: utf-8

# (C) Alex Hurst, 2015

import math
import operator
import re
import string


def tokenize(input_string):
    """Convert a user's input into a list of tokens for processing.

    Take a string that we would like to calculate, in any normal
    arithmetic notation. Clean it up to a list of numbers, operators,
    and brackets. Make appropriate modifications for various kinds of
    notation: implied multiplication, negative numbers, different styles
    of brackets, negative parentheses, and nested parentheses."""

    # Validate for illegal characters
    if re.search(r'''[^0-9\.,\+\-\*/\(\)\[\]\!\^\s]''',
                 input_string, re.VERBOSE):
        raise(ValueError(
              "The only allowable characters are 0-9, +, -, *, /, !, "
              "^, ., comma, parentheses, and square brackets."))
        return

    # Validate for unbalanced brackets
    if (input_string.count('(') != input_string.count(')') or
            input_string.count('[') != input_string.count(']')):

        raise(ValueError("Unbalanced brackets or parentheses."))

    regularized_string = re.sub(r'[\s,]', '', input_string)
    regularized_string = regularized_string.translate(
                                           string.maketrans('[]', '()'))

    # Accept '**', which is equivalent to '^'. Convert it to '^' for standard
    # handling.

    regularized_string = re.sub(r'''\*\*''',
                                r'''^''',
                                regularized_string)

    # Easy way to convert negative numbers into a compatible form for
    # parsing. Convert hyphen-number at the start of the string, start
    # of brackets, or after another operator strings like this:
    # -5+6 becomes (0-1)*5+6
    # (-5+6) becomes ((0-1)*5+6)
    # 5*-6 becomes 5*(0-1)*6

    neg_at_start_regex = re.compile(r'''(^ - ([\d\.,]+) )''', re.X)
    neg_after_op_regex = re.compile(r'''((?<=[-+*/(]) - ([\d\.,]+) )''', re.X)

    regularized_string = re.sub(neg_at_start_regex,
                                r'''(0-1)*\2''', regularized_string)
    regularized_string = re.sub(neg_after_op_regex,
                                r'''(0-1)*\2''', regularized_string)

    # Similar way to convert negative parentheses into a compatible form
    # for parsing. Convert '-(' in places where it signifies a negative:
    # -(1+2) becomes (0-1)*(1+2)

    regularized_string = re.sub(r'''^-(\()''',
                                r'''(0-1)*\1''',
                                regularized_string)

    regularized_string = re.sub(r'''(?<=[-+*/(])-(\()''',
                                r'''(0-1)*\1''',
                                regularized_string)

    # Regularize multiplication in the form
    # 2(3+4),  (2+3)4, or  (2+3)(4+5) into the form
    # 2*(3+4), (2+3)*4, or (2+3)*(4+5)
    regularized_string = re.sub(r'''(\d)(\()''', r'''\1*\2''',
                                regularized_string)
    regularized_string = re.sub(r'''(\))(\d)''', r'''\1*\2''',
                                regularized_string)
    regularized_string = re.sub(r'''(\))(\()''', r'''\1*\2''',
                                regularized_string)

    tokenized_input = re.split(r'''([^\d\.,])''', regularized_string,
                               re.VERBOSE)

    # re.split creates unwanted null values when the split pattern
    # occurs at the end of the string (close brackets and !.)
    while '' in tokenized_input:
        tokenized_input.remove('')

    tokenized_input_cast = []
    for token in tokenized_input:
        try:
            token_cast = float(token)
        except ValueError:
            token_cast = token

        tokenized_input_cast.append(token_cast)

    return tokenized_input_cast


def buildtree(tokens):
    """Parse a list of tokens into an evaluable tree.

    Convert a list of tokens (as prepared by ahcalc.tokenize()) 
    into a nested tree of binary or unary functions and their arguments.
    Recursively process the list to accommodate arbitrarily nested
    parentheses. Process operators in the correct order to respect
    normal arithmetical order of operation."""

    math_funcs = {'^': pow,
                  '+': operator.add,
                  '-': operator.sub,
                  '!': math.factorial,
                  '*': operator.mul,
                  '/': operator.div}
    tree = tokens[:]

    # Recursive case: there is at least one level of nested parentheses
    # to process.
    while '(' in tree:

        paren_start = tree.index('(')
        paren_contents = []
        depth = 0

        for i, token in enumerate(tree[paren_start:]):
            if token == '(':
                depth += 1
            elif token == ')':
                depth -= 1
            if depth == 0:
                paren_len = i
                break

        # The for loop never hit a break, which means we didn't find a
        # matching close parenthesis.
        else:
            raise(ValueError("Unmatched parentheses."))

        paren_end = paren_start + paren_len

        # recursion magic: support arbitrarily deeply nested sets of
        # parentheses
        tree[paren_start:paren_end+1] = [buildtree(tree[
                                            paren_start+1 : paren_end])]

    # Base case: there are no parentheses in this list, and we can group
    # the other operators and return the tree.

    while '!' in tree:
        fact_idx = tree.index('!')
        if type(tree[fact_idx-1]) not in [float, list] or fact_idx == 0:
            raise(ValueError(
                  "Factorial without an appropriate group or number "
                  "preceding it."))
        else:
            tree[fact_idx-1 : fact_idx+1] = \
                [[math_funcs['!'], tree[fact_idx-1]]]

    while '^' in tree:
        exp_idx = tree.index('^')
        if (type(tree[exp_idx-1]) not in [float, list] or
                type(tree[exp_idx+1]) not in [float, list] or
                exp_idx in [0, len(tree)-1]):
            raise(ValueError(
                  "Exponent without appropriate groups or numbers "
                  "before and after it."))
        tree[exp_idx-1 : exp_idx+2] = \
            [[math_funcs['^'], tree[exp_idx-1], tree[exp_idx+1]]]

    while ('*' in tree) or ('/' in tree):

        # Which operator did we catch?
        # If multiple, select the first one.
        if '*' in tree and '/' in tree:
            muldiv_idx = min(tree.index('*'), tree.index('/'))
        elif '/' in tree:
            muldiv_idx = tree.index('/')
        elif '*' in tree:
            muldiv_idx = tree.index('*')
        else:
            raise(ValueError("How did we reach this point in the code?"))

        # Consume the first * or / and replace with a sub-expression of
        # it with its arguments.
        muldiv_char = tree[muldiv_idx]
        if (type(tree[muldiv_idx - 1]) not in [float, list] or
                type(tree[muldiv_idx + 1]) not in [float, list] or
                muldiv_idx in [0, len(tree)-1]):
            raise(ValueError(
                  "* or / without appropriate groups or numbers "
                  "before and after it."))
        tree[muldiv_idx-1 : muldiv_idx+2] = \
            [[math_funcs[muldiv_char],
                tree[muldiv_idx-1], tree[muldiv_idx+1]]]

    while ('+' in tree) or ('-' in tree):

        # Which operator did we catch?
        # If multiple, select the first one.
        if '+' in tree and '-' in tree:
            addsub_idx = min(tree.index('+'), tree.index('-'))
        elif '+' in tree:
            addsub_idx = tree.index('+')
        elif '-' in tree:
            addsub_idx = tree.index('-')
        else:
            raise(ValueError)

        # Consume the first + or - and replace with a sub-expression of
        # it with its arguments.
        addsub_char = tree[addsub_idx]
        if (type(tree[addsub_idx-1]) not in [float, list] or
                type(tree[addsub_idx+1]) not in [float, list] or
                addsub_idx in [0, len(tree)-1]):
            raise(ValueError(
                  "+ or - without appropriate groups or numbers "
                  "before and after it."))
        tree[addsub_idx-1 : addsub_idx+2] = \
            [[math_funcs[addsub_char],
                tree[addsub_idx-1], tree[addsub_idx+1]]]

    # We have consumed all the operators in order of precedence,
    # and at the end there's a nicely-arranged tree we can pass to
    # evaltree.
    return tree


def evaltree(expr):
    """Evaluate a tree created by buildtree.

    Recieve a list including, at minimum, a function object and the
    correct number of arguments to pass to that function. Any or all of
    the arguments in the list may be lists as well, with the same
    criteria. Lists may be nested to an arbitrary depth; evaluate
    the innermost function first, and pass its value up the chain.
    Functions with either one or two arguments (i.e. 2- or 3-element
    lists) are supported."""

    # base case: argument is a float.
    if type(expr) == float:
        return expr
    elif len(expr) == 1 and type(expr[0]) == float:
        return expr[0]

    # recursive case: argument is a tree.
    elif len(expr) == 1 and type(expr[0]) == list:
        return evaltree(expr[0])
    elif len(expr) == 2:
        return expr[0](evaltree(expr[1]))  # Better be a factorial.
    elif len(expr) == 3:
        return expr[0](evaltree(expr[1]), evaltree(expr[2]))
    else:
        raise(ValueError("evaltree received a list with an invalid length."))


def calc(mystring):
    """Get the numerical value of a string of arithmetic."""
    return(evaltree(buildtree(tokenize(mystring))))


if __name__ == '__main__':
    usage = """Usage: type any arithmetic sequence to calculate its value.
Use +, -, *, /, !, ^, **, (), or [].
Parentheses may be arbitrarily nested.
Whitespace is fine and will be discarded.
Use Control-C or type "exit" to exit this program."""

    print(usage)
    while True:
        user_string = raw_input('ahcalc: ')
        if user_string == '':
            continue
        elif user_string in ('q', 'quit','exit'):
            exit()
        elif user_string in ('h', 'help', '?'):
            print(usage)
            continue

        try:
            result = calc(user_string)
        except OverflowError:
            print("Incalculable! Wow, that's a really big number! You "
                  "probably can't use a number that large, anyway. Try "
                  "something more modest.")
            continue

        except ValueError as e:
            print(e)
            continue
        if int(result) == result:
            result = int(result)
        print(result)
