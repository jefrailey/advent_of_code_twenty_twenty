"""
--- Day 18: Operation Order ---

As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71

Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51

Here are a few more examples:

    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?
"""

from typing import Any, Callable, Sequence

import operator
import math


def evaluate(expression: str) -> int:
    """
    Evaluate a mathematical expression with addition and multiplication having the same precedence.
    """
    value = 0
    op = None
    op_map = {"*": operator.mul, "+": operator.add}
    idx = 0
    while idx < len(expression):
        current = expression[idx]
        if current.isnumeric():
            if op is None:
                value = int(current)
            else:
                value = op(value, int(current))
        elif current in op_map:
            op = op_map[current]
        elif current == "(":
            # find the closing parenthesis and recurse on the slice without the outermost parenthesis
            # set index to the closing parenthesis
            paren_count = 1
            runner = idx
            while paren_count != 0:
                runner += 1
                candidate = expression[runner]
                if candidate == ")":
                    paren_count -= 1
                elif candidate == "(":
                    paren_count += 1
            evaluated = evaluate(expression[idx + 1 : runner])
            idx = runner
            if op is None:
                value = evaluated
            else:
                value = op(value, evaluated)
        elif current != " ":
            raise ValueError(f"Unexpected expression character: '{current}'.")
        idx += 1
    return value


def part_one(expressions: Sequence[str]) -> int:
    """
    Return the sum of each expression in the expressions.
    """
    return sum(evaluate(expression) for expression in expressions)


"""
--- Part Two ---

You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231

Here are the other examples from above:

    1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
    2 * 3 + (4 * 5) becomes 46.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

What do you get if you add up the results of evaluating the homework problems using these new rules?
"""

def part_two(expressions: Sequence[str]) -> int:
    """
    Return the sum of each expression in the expressions.
    """
    return sum(evaluate_part_two(expression) for expression in expressions)


def evaluate_part_two(expression: str) -> int:
    """
    Evaluate the mathematical expression with addition having higher precedence than multiplication.
    """
    tokens = []
    idx = 0
    while idx < len(expression):
        current = expression[idx]
        if current.isnumeric():
            tokens.append(int(current))
        elif current == "(":
            runner = idx
            paren_count = 1
            while paren_count > 0:
                runner += 1
                if expression[runner] == "(":
                    paren_count += 1
                elif expression[runner] == ")":
                    paren_count -= 1
            tokens.append(evaluate_part_two(expression[idx + 1 : runner]))
            idx = runner
        elif current in {"+", "*"}:
            tokens.append(current)
        idx += 1
    remainder = []
    idx = 0
    while idx < len(tokens):
        current = tokens[idx]
        if current == "+":
            next_ = tokens[idx + 1]
            previous = remainder.pop()
            remainder.append(previous + int(next_))
            idx += 1
        elif isinstance(current, int):
            remainder.append(current)
        idx += 1
    return math.prod(remainder)


if __name__ == "__main__":

    def verify(expected: Any, actual: Any) -> None:
        assert expected == actual, f"{expected} != {actual}"

    diagnostic = [
        ("1 + 2 * 3 + 4 * 5 + 6", 71),
        ("1 + (2 * 3) + (4 * (5 + 6))", 51),
        ("2 * 3 + (4 * 5)", 26),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
    ]
    for expression, expected in diagnostic:
        verify(expected, evaluate(expression))

    level_three_diagnostic = [
        ("1 + 2 * 3 + 4 * 5 + 6", 231),
        ("1 + (2 * 3) + (4 * (5 + 6))", 51),
        ("2 * 3 + (4 * 5)", 46),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
        ("(2 + 4 * 9)", 54),
        ("(6 + 9 * 8 + 6)", 210),
        ("((6 + 9 * 8 + 6) + 6)", 216),
        ("(2 + 4 * 9) * (6 + 9 * 8 + 6)", 11340),
        ("((1 + 2) * (1 + 2) + 1)", 12),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6)", 11664),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4", 11670),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
    ]

    for expression, expected in level_three_diagnostic:
        verify(expected, evaluate_part_two(expression))

    from eighteen_input import input_

    print("Part one: ", part_one(input_))
    print("Part two: ", part_two(input_))