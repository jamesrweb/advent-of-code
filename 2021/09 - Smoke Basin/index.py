from typing import List

Column = int
Row = List[Column]
Grid = List[Row]

def solve_part_one(grid: Grid) -> int:
    low_points = []
    rows = range(len(grid))
    columns = range(len(grid[0]))

    for row in rows: 
        for column in columns:
            risk_levels = []

            if row - 1 >= 0: risk_levels.append(grid[row - 1][column])
            if row + 1 < len(grid): risk_levels.append(grid[row + 1][column])
            if column - 1 >= 0: risk_levels.append(grid[row][column -1])
            if column + 1 < len(grid[0]): risk_levels.append(grid[row][column + 1])
        
            if grid[row][column] < min(risk_levels):
                low_points.append(grid[row][column])

    return sum(low_points) + len(low_points)

def solve_part_two(grid: Grid) -> int:
    basins = []
    rows = range(len(grid))
    columns = range(len(grid[0]))

    for row in rows: 
        for column in columns:
            risk_levels = []
            if row - 1 >= 0: risk_levels.append(grid[row - 1][column])
            if row + 1 < len(grid): risk_levels.append(grid[row + 1][column])
            if column - 1 >= 0: risk_levels.append(grid[row][column -1])
            if column + 1 < len(grid[0]): risk_levels.append(grid[row][column + 1])
        
            if grid[row][column] < min(risk_levels):
                basin = [[row, column]]

                for basin_row, basin_column in basin:
                    if basin_row - 1 >= 0 and grid[basin_row - 1][basin_column] != 9 and [basin_row - 1, basin_column] not in basin:
                        basin.append([basin_row - 1, basin_column])

                    if basin_row + 1 < len(grid) and grid[basin_row + 1][basin_column] != 9 and [basin_row + 1, basin_column] not in basin:
                        basin.append([basin_row + 1, basin_column])

                    if basin_column - 1 >= 0 and grid[basin_row][basin_column - 1] != 9 and [basin_row, basin_column - 1] not in basin:
                        basin.append([basin_row, basin_column - 1])

                    if basin_column + 1 < len(grid[0]) and grid[basin_row][basin_column + 1] != 9 and [basin_row, basin_column + 1] not in basin:
                        basin.append([basin_row, basin_column + 1])

                basins.append(len(basin))

    basins.sort()

    return basins[-1] * basins[-2] * basins[-3]

with open("input.txt", "r") as f:
    lines = f.readlines()
    grid: Grid = [[int(char) for char in line if char.isdigit()] for line in lines]

    print(f"part_one: {solve_part_one(grid)}")
    print(f"part_two: {solve_part_two(grid)}")