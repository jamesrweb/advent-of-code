from copy import deepcopy
from typing import List, Literal, Optional

type Cell = Literal[".", "@", "x"]
type Cells = List[Cell]
type FactoryMap = List[Cells]


def cell(character: str) -> Cell:
    """
    Convert the given character into a `Cell`.

    Recognised paper roll characters ("@") are preserved, and any other character is normalised into an empty cell (".").

    Args:
        character: The raw character that was parsed from the factory map.

    Returns:
        "@" for a paper roll, or "." for an empty cell.
    """
    return "@" if character == "@" else "."


def in_bounds(factory: FactoryMap, row_index: int, column_index: int) -> bool:
    """
    Checks whether a given row / column index pair falls within the factory map.

    Args:
        factory: The factory map.
        row_index: The row to check.
        column_index: The column within the row to check.

    Returns:
        True when both indices fall within the map otherwise False.
    """
    return 0 <= row_index < len(factory) and 0 <= column_index < len(factory[row_index])


def get_cell(factory: FactoryMap, row_index: int, column_index: int) -> Optional[Cell]:
    """
    Attempts to get the value of a cell at a given row / column index pair within the factory map.

    Args:
        factory: The factory map.
        row_index: The row to lookup.
        column_index: The column within the row to lookup.

    Returns:
        The cell value or `None` when the indices fall outside the map.
    """
    if not in_bounds(factory, row_index, column_index):
        return None

    return factory[row_index][column_index]


def set_cell(
    factory: FactoryMap, row_index: int, column_index: int, value: Cell
) -> FactoryMap:
    """
    Attempts to set the value of a cell at a given row / column index pair within the factory map.

    The factory map is returned unchanged when the indices fall outside the map.

    Args:
        factory: The factory map.
        row_index: The row to update.
        column_index: The column within the row to update.
        value: The value to write into the cell.

    Returns:
        The factory map with the cell updated when the indices fall within the map.
    """
    if not in_bounds(factory, row_index, column_index):
        return factory

    factory[row_index][column_index] = value

    return factory


def solve(factory: FactoryMap, count: int, is_part_one: bool) -> int:
    """
    Attempt to calculate the number of paper rolls available to be moved.

    The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions.

    Args:
        factory: The factory map.
        count: The count of paper rolls we can remove.
        is_part_one: If the current solution is for part one of the challenge.

    Returns:
        How many paper rolls can be accessed by the forklifts available.
    """
    next_count = count
    next_factory_map = deepcopy(factory)

    for row_index, row in enumerate(factory):
        for column_index, column in enumerate(row):
            if column != "@":
                continue

            adjacent_cells = [
                get_cell(factory, row_index - 1, column_index - 1),
                get_cell(factory, row_index - 1, column_index),
                get_cell(factory, row_index - 1, column_index + 1),
                get_cell(factory, row_index, column_index - 1),
                get_cell(factory, row_index, column_index + 1),
                get_cell(factory, row_index + 1, column_index - 1),
                get_cell(factory, row_index + 1, column_index),
                get_cell(factory, row_index + 1, column_index + 1),
            ]

            if adjacent_cells.count("@") >= 4:
                continue

            next_count += 1
            next_factory_map = set_cell(next_factory_map, row_index, column_index, "x")

    if is_part_one or next_count == count:
        return next_count

    return solve(next_factory_map, next_count, is_part_one)


with open("input.txt") as f:
    factory_map: FactoryMap = [
        [cell(character) for character in line.strip()] for line in f.readlines()
    ]

    print(f"part_one: {solve(deepcopy(factory_map), 0, True)}")
    print(f"part_two: {solve(deepcopy(factory_map), 0, False)}")
