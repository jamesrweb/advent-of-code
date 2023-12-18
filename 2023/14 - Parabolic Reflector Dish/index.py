from math import floor
from typing import Tuple, Text

Grid = Tuple[Text]


def cycle(grid: Grid) -> int:
    current_iteration = grid

    for _ in range(4):
        current_iteration = tuple(map("".join, zip(*current_iteration)))
        current_iteration = tuple(
            "#".join(
                [
                    "".join(sorted(tuple(group), reverse=True))
                    for group in row.split("#")
                ]
            )
            for row in current_iteration
        )
        current_iteration = tuple(row[::-1] for row in current_iteration)

    return current_iteration


def solve_part_one(grid: Grid) -> int:
    total = 0

    for column in zip(*grid):
        blocks = "".join(column).split("#")
        index = len(grid) + 1

        for block in blocks:
            n = block.count("O")

            total += (n * index - n * (n + 1) // 2) if n > 0 else 0
            index -= len(block) + 1

    return total


def solve_part_two(grid: Grid) -> int:
    states = []
    seen = set()
    index = 0
    current_iteration = grid

    while current_iteration not in seen:
        states.append(current_iteration)
        seen.add(current_iteration)
        current_iteration = cycle(current_iteration)
        index += 1

    offset = states.index(current_iteration)
    cycle_length = index - offset
    next_iteration = states[floor((1e9 - offset) % cycle_length + offset)]
    return sum(
        row.count("O") * (len(grid) - row_index)
        for row_index, row in enumerate(next_iteration)
    )


with open("input.txt", "r") as file:
    lines = file.read().splitlines()
    grid = tuple(lines)
    part_one = solve_part_one(grid)
    part_two = solve_part_two(grid)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
