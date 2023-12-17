from typing import List, Text, NamedTuple


class Galaxy(NamedTuple):
    x: int
    y: int


GalaxyMap = List[Galaxy]


def create_row_prefix_sum_array(lines: List[Text], scale: int) -> List[int]:
    row_prefix_sum_array = [0]

    for row in lines:
        row_prefix_sum_array.append(
            row_prefix_sum_array[-1] + scale
            if all(column == "." for column in row)
            else row_prefix_sum_array[-1] + 1
        )

    return row_prefix_sum_array


def create_column_prefix_sum_array(lines: List[Text], scale: int) -> List[int]:
    column_prefix_sum_array = [0]

    for column in zip(*lines):
        column_prefix_sum_array.append(
            column_prefix_sum_array[-1] + scale
            if all(column == "." for column in column)
            else column_prefix_sum_array[-1] + 1
        )

    return column_prefix_sum_array


def generate_galaxy_map(lines: List[Text]) -> GalaxyMap:
    return [
        Galaxy(column_index, row_index)
        for row_index, row in enumerate(lines)
        for column_index, column in enumerate(row)
        if column == "#"
    ]


def solve(
    row_prefix_sum_array: List[int],
    column_prefix_sum_array: List[int],
    galaxy_map: GalaxyMap,
) -> int:
    return int(
        sum(
            [
                row_prefix_sum_array[max(y1, y2)]
                - row_prefix_sum_array[min(y1, y2)]
                + column_prefix_sum_array[max(x1, x2)]
                - column_prefix_sum_array[min(x1, x2)]
                for index, (x1, y1) in enumerate(galaxy_map)
                for (x2, y2) in galaxy_map[:index]
            ]
        )
    )


def solve_part_one(lines: List[Text], galaxy_map: Galaxy) -> int:
    row_prefix_sum_array = create_row_prefix_sum_array(lines, 2)
    column_prefix_sum_array = create_column_prefix_sum_array(lines, 2)

    return solve(row_prefix_sum_array, column_prefix_sum_array, galaxy_map)


def solve_part_two(lines: List[Text], galaxy_map: Galaxy) -> int:
    row_prefix_sum_array = create_row_prefix_sum_array(lines, 1e6)
    column_prefix_sum_array = create_column_prefix_sum_array(lines, 1e6)

    return solve(row_prefix_sum_array, column_prefix_sum_array, galaxy_map)


with open("input.txt", "r") as file:
    lines = file.read().splitlines()
    galaxy_map = generate_galaxy_map(lines)
    part_one = solve_part_one(lines, galaxy_map)
    part_two = solve_part_two(lines, galaxy_map)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
