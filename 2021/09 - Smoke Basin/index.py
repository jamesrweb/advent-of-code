from typing import Callable, List

Column = int
Row = List[Column]
Grid = List[Row]
LowPoints = List[int]
SolveCallback = Callable[[Grid, Row, Column], None]


def solve(grid: Grid, callback: SolveCallback):
    rows = range(len(grid))
    columns = range(len(grid[0]))

    for row in rows:
        for column in columns:
            risk_levels = []

            if row - 1 >= 0:
                risk_levels.append(grid[row - 1][column])
            if row + 1 < len(grid):
                risk_levels.append(grid[row + 1][column])
            if column - 1 >= 0:
                risk_levels.append(grid[row][column - 1])
            if column + 1 < len(grid[0]):
                risk_levels.append(grid[row][column + 1])

            if grid[row][column] < min(risk_levels):
                callback(grid, row, column)


def append_to_low_points(low_points: LowPoints) -> None:
    def append_to_low_points_from_grid(grid: Grid, row: Row, column: Column) -> None:
        low_points.append(grid[row][column])

    return append_to_low_points_from_grid


def construct_basins_for_low_points(low_points: LowPoints) -> SolveCallback:
    def construct_basins(grid: Grid, row: Row, column: Column) -> None:
        basins = [[row, column]]

        for basin_row, basin_column in basins:
            if (
                basin_row - 1 >= 0
                and grid[basin_row - 1][basin_column] != 9
                and [basin_row - 1, basin_column] not in basins
            ):
                basins.append([basin_row - 1, basin_column])

            if (
                basin_row + 1 < len(grid)
                and grid[basin_row + 1][basin_column] != 9
                and [basin_row + 1, basin_column] not in basins
            ):
                basins.append([basin_row + 1, basin_column])

            if (
                basin_column - 1 >= 0
                and grid[basin_row][basin_column - 1] != 9
                and [basin_row, basin_column - 1] not in basins
            ):
                basins.append([basin_row, basin_column - 1])

            if (
                basin_column + 1 < len(grid[0])
                and grid[basin_row][basin_column + 1] != 9
                and [basin_row, basin_column + 1] not in basins
            ):
                basins.append([basin_row, basin_column + 1])

        low_points.append(len(basins))
        low_points.sort()

    return construct_basins


def solve_part_one(grid: Grid) -> int:
    low_points = []

    solve(grid, append_to_low_points(low_points))

    return sum(low_points) + len(low_points)


def solve_part_two(grid: Grid) -> int:
    low_points = []

    solve(grid, construct_basins_for_low_points(low_points))

    return low_points[-1] * low_points[-2] * low_points[-3]


with open("input.txt", "r") as f:
    lines = f.readlines()
    grid: Grid = [[int(char) for char in line if char.isdigit()] for line in lines]

    print(f"part_one: {solve_part_one(grid)}")
    print(f"part_two: {solve_part_two(grid)}")
