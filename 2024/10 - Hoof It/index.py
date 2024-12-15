from collections import deque
from os import path


def score_trailhead(grid, rows, columns, row, column):
    queue = deque([(row, column)])
    seen = {(row, column)}
    summits = 0

    while len(queue) > 0:
        cr, cc = queue.popleft()
        for nr, nc in [(cr - 1, cc), (cr, cc + 1), (cr + 1, cc), (cr, cc - 1)]:
            if nr < 0 or nc < 0 or nr >= rows or nc >= columns:
                continue
            if grid[nr][nc] != grid[cr][cc] + 1:
                continue
            if (nr, nc) in seen:
                continue
            seen.add((nr, nc))
            if grid[nr][nc] == 9:
                summits += 1
            else:
                queue.append((nr, nc))
    return summits


def count_distinct_hiking_trails_to_trailhead(grid, rows, columns, row, column):
    queue = deque([(row, column)])
    seen = {(row, column): 1}
    trails = 0

    while len(queue) > 0:
        y, x = queue.popleft()

        if grid[y][x] == 9:
            trails += seen[(y, x)]

        for ny, nc in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]:
            if ny < 0 or nc < 0 or ny >= rows or nc >= columns:
                continue

            if grid[ny][nc] != grid[y][x] + 1:
                continue

            if (ny, nc) in seen:
                seen[(ny, nc)] += seen[(y, x)]
                continue

            seen[(ny, nc)] = seen[(y, x)]
            queue.append((ny, nc))

    return trails


def score_trailheads(grid, unique):
    rows = len(grid)
    columns = len(grid[0])
    trailheads = [
        (row, column)
        for row in range(rows)
        for column in range(columns)
        if grid[row][column] == 0
    ]

    if not unique:
        return sum(
            score_trailhead(grid, rows, columns, row, column)
            for row, column in trailheads
        )
    else:
        return sum(
            count_distinct_hiking_trails_to_trailhead(grid, rows, columns, row, column)
            for row, column in trailheads
        )


with open(path.dirname(path.realpath(__file__)) + "/input.txt") as file:
    grid = [[int(char) for char in line.strip()] for line in file.readlines()]
    part_one = score_trailheads(grid, False)
    part_two = score_trailheads(grid, True)

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
