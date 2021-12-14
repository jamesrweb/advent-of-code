from functools import reduce
from typing import List, Tuple, Set
from re import search

Point = Tuple[int, int]
Fold = Tuple[str, int]
Points = Set[Point]
Folds = List[Fold]

CHAR_WIDTH = 4
CHAR_HEIGHT = 6
CHAR_COUNT_TO_FIND = 8


def apply_folds(points: Points, axis: str, position: int) -> Points:
    if axis == "y":
        return {
            (x, y - (y - position) * 2) if y > position else (x, y) for x, y in points
        }

    return {(x - (x - position) * 2, y) if x > position else (x, y) for x, y in points}


def display_code(points: Points) -> str:
    spaces = CHAR_COUNT_TO_FIND - 1
    width = CHAR_WIDTH * CHAR_COUNT_TO_FIND + spaces
    paper = [[" "] * width for _ in range(CHAR_HEIGHT)]

    for x, y in points:
        paper[y][x] = "#"

    found_characters = "\n".join("".join(row) for row in paper)

    return "\n" + found_characters


def point_from_coord(coord: str) -> Point:
    x, y = coord.split(",")

    return int(x), int(y)


def fold_from_fold_instruction(fold_instruction: str) -> Fold:
    result = search("(\w){1}=(\d+)$", fold_instruction)

    return str(result[1]), int(result[2])


def solve_part_one(points: Points, folds: Folds) -> int:
    axis, position = folds[0]
    fold_result = apply_folds(points, axis, position)

    return len(fold_result)


def fold_reducer(accumulator: Points, current: Fold) -> Points:
    axis, position = current

    return apply_folds(accumulator, axis, position)


def solve_part_two(points: Points, folds: Folds) -> str:
    fold_result = reduce(fold_reducer, folds, points)

    return display_code(fold_result)


with open("input.txt", "r") as f:
    EOL = "\n"
    coords, fold_instructions = f.read().split(EOL + EOL)
    points: Points = {point_from_coord(coord) for coord in coords.split(EOL)}
    folds: Folds = [
        fold_from_fold_instruction(fold_instruction)
        for fold_instruction in fold_instructions.split(EOL)
    ]

    print(f"part_one: {solve_part_one(points, folds)}")
    print(f"part_two: {solve_part_two(points, folds)}")
