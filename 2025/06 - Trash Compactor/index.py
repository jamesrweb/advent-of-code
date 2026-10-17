from functools import reduce
from typing import List, Literal

type Operator = Literal["/", "*", "+", "-"]
type Problem = List[int | Operator]
type Homework = List[Problem]


def parse_operator(token: str) -> Operator:
    """
    Convert the given worksheet token into an `Operator`.

    Operators are single mathematical symbols ("/", "*", "+", "-").

    Any other token is not a valid worksheet operator and will result in a `ValueError`.

    Args:
        token: The raw token that was parsed from the worksheet.

    Returns:
        The operator symbol that the token represents.
    """
    operators: dict[str, Operator] = {"/": "/", "*": "*", "+": "+", "-": "-"}
    operator = operators.get(token)

    if operator is None:
        raise ValueError(f"Unknown worksheet operator: {token}")

    return operator


def parse_token(part: str) -> int | Operator:
    """
    Convert the given worksheet token into an `int` or an `Operator`.

    Numeric tokens are converted into integers, and every other token is parsed as an operator.

    Args:
        part: The raw whitespace-separated token that was parsed from a worksheet row.

    Returns:
        The integer for a numeric token, otherwise the operator that the token represents.
    """
    stripped = part.strip()

    return int(stripped) if stripped.isnumeric() else parse_operator(stripped)


def calculate(accumulator: int, problem: Problem) -> int:
    """
    Attempt to calculate the worksheet's running grand total including the given problem.

    The problems' numbers are folded together with its operator, and the result is added onto the accumulator.

    Args:
        accumulator: The grand total accumulated so far.
        problem: The problem numbers, followed by its operator.

    Returns:
        The running total including the given problems answer.
    """
    operator = problem[-1]
    numbers = problem[:-1]

    return accumulator + reduce(
        lambda a, b: eval(f"{a} {operator} {b}"), numbers[1:], numbers[0]
    )


def solve(homework: Homework) -> int:
    """
    Attempt to calculate the worksheet's grand total.

    Every problem answer is summed into the single grand total that the cephalopods expect from the worksheet.

    Args:
        homework: The worksheet problems.

    Returns:
        The grand total of all the individual problem answers.
    """
    return reduce(calculate, homework, 0)


def parse_rows(lines: List[str]) -> Homework:
    """
    Parse the worksheet lines into problems, one problem per number column.

    The lines are split into whitespace-separated tokens, transposed, and every transposed column reads as one problems
    numbers followed by its operator.

    Args:
        lines: The raw worksheet lines.

    Returns:
        The worksheet problems as number lists followed by their operator.
    """
    matrix = [[parse_token(part) for part in line.split()] for line in lines]
    worksheet = [list(column) for column in zip(*matrix)]

    return worksheet


def parse_columns(lines: List[str]) -> Homework:
    """
    Parse the worksheet lines into problems, one problem per group of character columns.

    The operator row is parsed separately into operator tokens, the remaining lines are transposed into character columns, and each contiguous group of columns containing digits forms one problem. Every number is read by joining a column's digits from top to bottom.

    Only "*" and "+" appear on the worksheet, and both are commutative, so reading the number groups left-to-right does not change any answer.

    Args:
        lines: The raw worksheet lines.

    Returns:
        The worksheet problems as number lists followed by their operator.
    """
    operators = [parse_operator(token) for token in lines[-1].split()]
    numeric_lines = lines[:-1]
    width = max(len(line) for line in numeric_lines)
    padded = [line.ljust(width) for line in numeric_lines]
    columns = zip(*padded)

    groups: List[List[int]] = []
    numbers: List[int] = []

    for column in columns:
        digits = "".join(character for character in column if character.isdigit())

        if digits == "":
            groups.append(numbers)
            numbers = []
            continue

        numbers.append(int(digits))

    groups.append(numbers)
    groups = [group for group in groups if group]

    problems: Homework = []

    for group, operator in zip(groups, operators):
        problems.append([*group, operator])

    return problems


with open("input.txt") as f:
    input_lines = f.read().splitlines()
    row_wise = parse_rows(input_lines)
    column_wise = parse_columns(input_lines)

    print(f"part_one: {solve(row_wise)}")
    print(f"part_two: {solve(column_wise)}")
