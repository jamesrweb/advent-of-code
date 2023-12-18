from typing import List, Text, Tuple
from collections import deque


def calculate(grid: List[Text], init: Tuple[int, int, int, int]) -> int:
    seen = set()
    queue = deque([init])

    while len(queue) > 0:
        state = queue.popleft()

        if state in seen:
            continue

        seen.add(state)

        row, column, row_direction, column_direction = state

        row += row_direction
        column += column_direction

        if row < 0 or row >= len(grid) or column < 0 or column >= len(grid[0]):
            continue

        character = grid[row][column]

        if (
            character == "."
            or character == "-"
            and column_direction != 0
            or character == "|"
            and row_direction != 0
        ):
            queue.append((row, column, row_direction, column_direction))
        elif character == "/":
            queue.append((row, column, -column_direction, -row_direction))
        elif character == "\\":
            queue.append((row, column, column_direction, row_direction))
        else:
            if character == "|":
                queue.append((row, column, -1, 0))
                queue.append((row, column, 1, 0))
            else:
                queue.append((row, column, 0, -1))
                queue.append((row, column, 0, 1))

    coordinates = set([(row, column) for (row, column, _, _) in seen])

    return len(coordinates) - 1


def solve_part_one(grid: List[Text]) -> int:
    return calculate(grid, (0, -1, 0, 1))


def solve_part_two(grid: List[Text]) -> int:
    maximum_energized_titles = 0

    for row in range(len(grid)):
        maximum_energized_titles = max(
            maximum_energized_titles, calculate(grid, (row, -1, 0, 1))
        )
        maximum_energized_titles = max(
            maximum_energized_titles, calculate(grid, (row, len(grid[0]), 0, -1))
        )

    for column in range(len(grid)):
        maximum_energized_titles = max(
            maximum_energized_titles, calculate(grid, (-1, column, 1, 0))
        )
        maximum_energized_titles = max(
            maximum_energized_titles, calculate(grid, (len(grid), column, -1, 0))
        )

    return maximum_energized_titles


with open("input.txt", "r") as file:
    input = file.read().splitlines()
    part_one = solve_part_one(input)
    part_two = solve_part_two(input)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
