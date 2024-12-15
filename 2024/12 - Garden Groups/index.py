from collections import deque
from os import path


def build_regions(grid):
    rows = len(grid)
    columns = len(grid[0])
    regions = []
    seen = set()

    for row in range(rows):
        for column in range(columns):
            if (row, column) in seen:
                continue

            seen.add((row, column))
            region = {(row, column)}
            queue = deque([(row, column)])
            crop = grid[row][column]

            while queue:
                cr, cc = queue.popleft()

                for nr, nc in [(cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)]:
                    if nr < 0 or nc < 0 or nr >= rows or nc >= columns:
                        continue

                    if grid[nr][nc] != crop:
                        continue

                    if (nr, nc) in region:
                        continue

                    region.add((nr, nc))
                    queue.append((nr, nc))

            seen |= region
            regions.append(region)

    return regions


def perimeter_for_region(region):
    output = 0

    for r, c in region:
        output += 4

        for nr, nc in [(r + 1, c), (r - 1, c), (r, c - 1), (r, c + 1)]:
            if (nr, nc) in region:
                output -= 1

    return output


def sides(region):
    corners = 0
    corner_candidates = set()

    for row, column in region:
        for cr, cc in [
            (row - 0.5, column - 0.5),
            (row + 0.5, column - 0.5),
            (row + 0.5, column + 0.5),
            (row - 0.5, column + 0.5),
        ]:
            corner_candidates.add((cr, cc))

    for cr, cc in corner_candidates:
        config = [
            (sr, sc) in region
            for sr, sc in [
                (cr - 0.5, cc - 0.5),
                (cr + 0.5, cc - 0.5),
                (cr + 0.5, cc + 0.5),
                (cr - 0.5, cc + 0.5),
            ]
        ]
        count = sum(config)

        if count == 1:
            corners += 1
        elif count == 2:
            options = [[True, False, True, False], [False, True, False, True]]
            corners += 2 if config in options else 0
        elif count == 3:
            corners += 1

    return corners


def calculate_fencing_cost(grid):
    regions = build_regions(grid)

    return sum(len(region) * perimeter_for_region(region) for region in regions)


def calculate_fencing_cost_with_discount(grid):
    regions = build_regions(grid)

    return sum(len(region) * sides(region) for region in regions)


with open(path.dirname(path.realpath(__file__)) + "/input.txt") as file:
    grid = [list(line.strip()) for line in file.readlines()]
    part_one = calculate_fencing_cost(grid.copy())
    part_two = calculate_fencing_cost_with_discount(grid.copy())

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
