from math import floor
from collections import deque
from typing import Text, List, Optional, NamedTuple, Set

Grid = List[List[Text]]


class Coordinate(NamedTuple):
    column_index: int
    row_index: int


def build_grid(lines: List[str]) -> Grid:
    return [line for line in lines]


def find_start_position(grid: Grid) -> Optional[Coordinate]:
    for row_index, row in enumerate(grid):
        for column_index, column in enumerate(row):
            if column == "S":
                return Coordinate(column_index, row_index)

    return None


def character_at_position(grid: Grid, position: Coordinate) -> Text:
    return grid[position.row_index][position.column_index]


def is_valid_north_character(
    grid: Grid, current_position: Coordinate, north: Coordinate
) -> bool:
    try:
        north_character = character_at_position(grid, north)

        return current_position.row_index > 0 and north_character in "|7F"
    except:
        return False


def is_valid_south_character(
    grid: Grid, current_position: Coordinate, south: Coordinate
) -> bool:
    try:
        south_character = character_at_position(grid, south)

        return current_position.row_index < len(grid) - 1 and south_character in "|JL"
    except:
        return False


def is_valid_east_character(
    grid: Grid, current_position: Coordinate, east: Coordinate
) -> bool:
    try:
        east_character = character_at_position(grid, east)

        return current_position.column_index > 0 and east_character in "-LF"
    except:
        return False


def is_valid_west_character(
    grid: Grid, current_position: Coordinate, west: Coordinate
) -> bool:
    try:
        west_character = character_at_position(grid, west)

        return (
            current_position.column_index < len(grid[current_position.row_index]) - 1
            and west_character in "-J7"
        )
    except:
        return False


def identify_tiles_outside_the_loop(grid: Grid) -> Set[Coordinate]:
    outside = set()

    for row_index, row in enumerate(grid):
        within = False
        up = None

        for column_index, column in enumerate(row):
            if column == "|":
                within = not within
            elif column in "LF":
                up = column == "L"
            elif column in "7J":
                if column != ("J" if up else "7"):
                    within = not within

                up = None
            elif column == ".":
                pass

            if not within:
                outside.add(Coordinate(column_index, row_index))

    return outside


def solve(grid: Grid, start_position: Coordinate, is_part_one: bool) -> int:
    seen = set([start_position])
    queue = deque([start_position])
    maybe_s = {"|", "-", "J", "L", "7", "F"}

    while len(queue) > 0:
        current_position = queue.popleft()
        current_character = character_at_position(grid, current_position)
        north = Coordinate(
            current_position.column_index, current_position.row_index - 1
        )
        south = Coordinate(
            current_position.column_index, current_position.row_index + 1
        )
        east = Coordinate(current_position.column_index - 1, current_position.row_index)
        west = Coordinate(current_position.column_index + 1, current_position.row_index)

        if (
            current_character in "S|JL"
            and is_valid_north_character(grid, current_position, north)
            and north not in queue
        ):
            seen.add(north)
            queue.append(north)

            if not is_part_one and current_character == "S":
                maybe_s &= {"|", "J", "L"}

        if (
            current_character in "S|7F"
            and is_valid_south_character(grid, current_position, south)
            and south not in seen
        ):
            seen.add(south)
            queue.append(south)

            if not is_part_one and current_character == "S":
                maybe_s &= {"|", "7", "F"}

        if (
            current_character in "S-J7"
            and is_valid_east_character(grid, current_position, east)
            and east not in seen
        ):
            seen.add(east)
            queue.append(east)

            if not is_part_one and current_character == "S":
                maybe_s &= {"-", "J", "7"}

        if (
            current_character in "S-LF"
            and is_valid_west_character(grid, current_position, west)
            and west not in seen
        ):
            seen.add(west)
            queue.append(west)

            if not is_part_one and current_character == "S":
                maybe_s &= {"-", "L", "F"}

    if is_part_one:
        return floor(len(seen) / 2)

    assert len(maybe_s) == 1

    s = maybe_s.pop()
    updated_grid = [row.replace("S", s) for row in grid]
    updated_grid = [
        "".join(
            column if Coordinate(column_index, row_index) in seen else "."
            for column_index, column in enumerate(row)
        )
        for row_index, row in enumerate(updated_grid)
    ]
    outside = identify_tiles_outside_the_loop(updated_grid)

    return len(updated_grid) * len(updated_grid[0]) - len(outside | seen)


def solve_part_one(grid: Grid, start_position: Coordinate) -> int:
    return solve(grid, start_position, True)


def solve_part_two(grid: Grid, start_position: Coordinate) -> int:
    return solve(grid, start_position, False)


with open("input.txt", "r") as file:
    lines = file.read().splitlines()
    grid = build_grid(lines)
    start_position = find_start_position(grid)
    part_one = solve_part_one(grid, start_position)
    part_two = solve_part_two(grid, start_position)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
