from os import path


def find_antennas(grid):
    antennas = {}

    for y, row in enumerate(grid):
        for x, column in enumerate(row):
            if column != ".":
                if column not in antennas:
                    antennas[column] = []

                antennas[column].append((y, x))

    return antennas


def find_antinodes(grid, antennas, account_for_t_frequencies):
    rows = len(grid)
    columns = len(grid[0])
    antinodes = set()

    for locations in antennas.values():
        for i in range(len(locations)):
            if not account_for_t_frequencies:
                for j in range(i + 1, len(locations)):
                    y1, x1 = locations[i]
                    y2, x2 = locations[j]

                    antinodes.add((2 * y1 - y2, 2 * x1 - x2))
                    antinodes.add((2 * y2 - y1, 2 * x2 - x1))
            else:
                for j in range(len(locations)):
                    if i == j:
                        continue

                    y1, x1 = locations[i]
                    y2, x2 = locations[j]
                    dy = y2 - y1
                    dx = x2 - x1
                    row = y1
                    column = x1

                    while 0 <= row < rows and 0 <= column < columns:
                        antinodes.add((row, column))
                        row += dy
                        column += dx

    return antinodes


def unique_antinode_locations(grid, account_for_t_frequencies):
    if len(grid) < 1:
        raise "Invalid grid provided"

    rows = len(grid)
    columns = len(grid[0])
    antennas = find_antennas(grid)
    antinodes = find_antinodes(grid, antennas, account_for_t_frequencies)

    if not account_for_t_frequencies:
        return len(
            [
                0
                for row, column in antinodes
                if 0 <= row < rows and 0 <= column < columns
            ]
        )
    else:
        return len(antinodes)


with open(path.dirname(path.realpath(__file__)) + "/input.txt") as file:
    grid = [line.strip() for line in file.readlines()]

    part_one = unique_antinode_locations(grid.copy(), False)
    part_two = unique_antinode_locations(grid.copy(), True)

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
