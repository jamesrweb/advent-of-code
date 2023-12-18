from typing import List, Text

Grid = List[Text]
Grids = List[Grid]


def generate_grids(lines: List[Text]) -> Grids:
    return [line.splitlines() for line in lines]


def to_binary(text: Text) -> int:
    return sum(2**index if column == "#" else 0 for index, column in enumerate(text))


def find_mirror_part_one(binaries: List[int]) -> int:
    for index in range(1, len(binaries)):
        outer_index = index
        inner_index = index - 1

        while outer_index < len(binaries) and inner_index >= 0:
            if binaries[outer_index] != binaries[inner_index]:
                break

            outer_index += 1
            inner_index -= 1
        else:
            return index

    return 0


def find_mirror_part_two(binaries: List[int]) -> int:
    for index in range(1, len(binaries)):
        outer_index = index
        inner_index = index - 1
        error = False

        while outer_index < len(binaries) and inner_index >= 0:
            if binaries[outer_index] != binaries[inner_index]:
                if error:
                    break

                difference = binaries[outer_index] ^ binaries[inner_index]

                if difference & (difference - 1) == 0:
                    error = True
                else:
                    break

            outer_index += 1
            inner_index -= 1
        else:
            if error:
                return index

    return 0


def solve_part_one(grids: Grids) -> int:
    mirrors = 0

    for grid in grids:
        rows = [to_binary(row) for row in grid]
        columns = [to_binary(column) for column in zip(*grid)]

        mirrors += find_mirror_part_one(rows) * 100 + find_mirror_part_one(columns)

    return mirrors


def solve_part_two(grids: Grids) -> int:
    mirrors = 0

    for grid in grids:
        rows = [to_binary(row) for row in grid]
        columns = [to_binary(column) for column in zip(*grid)]

        mirrors += 100 * find_mirror_part_two(rows) or find_mirror_part_two(columns)

    return mirrors


with open("input.txt", "r") as file:
    lines = file.read().split("\n\n")
    grids = generate_grids(lines)
    part_one = solve_part_one(grids)
    part_two = solve_part_two(grids)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
