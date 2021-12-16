from math import inf as infinity
from heapq import heapify, heappop, heappush
from typing import List

Column = int
Row = List[Column]
Grid = List[Row]


def solve(grid: Grid, grid_dimension_multiplier: int) -> int:
    # Take the default grid size of the input data
    row_count = len(grid)
    column_count = len(grid[0])

    # Allow scaling for part 2
    scaled_row_count = row_count * grid_dimension_multiplier
    scaled_column_count = column_count * grid_dimension_multiplier

    # Directions: left, down, right, up
    row_directions = [-1, 0, 1, 0]
    column_directions = [0, 1, 0, -1]

    # Start at ditance 0 from position 0,0
    vertices = [(0, 0, 0)]

    # Set initial "costs" for each column in each row to initially be -infinity
    distance_costs = [
        [-infinity for _ in range(scaled_column_count)] for _ in range(scaled_row_count)
    ]

    # Transform our vertex list to a heap structure
    heapify(vertices)

    # While we still have items in the heap to check
    while len(vertices) > 0:
        # Take the next position from the heap
        (distance, row, column) = heappop(vertices)

        # If it is out of bounds, discard it
        if (
            row < 0
            or row >= scaled_row_count
            or column < 0
            or column >= scaled_column_count
        ):
            continue

        # Calculate the risk level of moving to this position
        risk_level = (
            grid[row % row_count][column % column_count]
            + (row // row_count)
            + (column // column_count)
        )

        # If the risk level is higher than 9 we need to wrap around the matrix
        while risk_level > 9:
            risk_level -= 9

        # Take the current cost for this position and the newly calculated cost
        current_cost = distance_costs[row][column]
        next_cost = distance + risk_level

        # If the cost is too high, discard this position as a posibility
        if current_cost != -infinity and next_cost >= current_cost:
            continue

        # Set the position to have the new lower cost
        distance_costs[row][column] = next_cost
        max_row_index = scaled_row_count - 1
        max_column_index = scaled_column_count - 1

        # If we made it to the bottom right corner, we are finished and can exit the loop
        if row == max_row_index and column == max_column_index:
            break

        # Update the vertices heap with all possible positions to check from the current position
        for direction_index in range(4):
            next_row_check_index = row + row_directions[direction_index]
            next_column_check_index = column + column_directions[direction_index]
            vertex = (
                distance_costs[row][column],
                next_row_check_index,
                next_column_check_index,
            )
            heappush(vertices, vertex)

    # Return the cost minus the top left corner risk level since we don't count that
    return distance_costs[max_row_index][max_column_index] - grid[0][0]


with open("input.txt", "r") as f:
    lines = f.read().split("\n")
    grid = [[int(value) for value in line.strip()] for line in lines]

    print(f"part_one: {solve(grid, 1)}")
    print(f"part_two: {solve(grid, 5)}")
