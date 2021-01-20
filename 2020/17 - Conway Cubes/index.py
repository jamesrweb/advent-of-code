from itertools import product
from collections import Counter as Count
from typing import List, Tuple, Counter

Coords = Tuple[int, ...]


def neighbour_coordinates(coordinate: Coords) -> List[Coords]:
    return [
        tuple(a + b for a, b in zip(coordinate, variation))
        for variation in product([-1, 0, 1], repeat=len(coordinate))
        if any(variation)
    ]


def simulate(lines: List[str], dimensions: int) -> int:
    active: List[Coords] = [
        (x, y) + (0,) * (dimensions - 2)
        for y, line in enumerate(lines)
        for x, cell in enumerate(line) if cell == '#'
    ]

    for _ in range(6):
        neighbours: Counter[Coords] = Count(
            coord
            for coordinate in active
            for coord in neighbour_coordinates(coordinate)
        )

        active = [
            coord for coord, count in neighbours.items()
            if (coord in active and count == 2) or count == 3
        ]

    return len(active)


with open("input.txt", "r") as f:
    lines = f.readlines()
    print(f"part_one: {simulate(lines, 3)}")
    print(f"part_two: {simulate(lines, 4)}")
