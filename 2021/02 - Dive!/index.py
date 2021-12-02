from typing import List

def solve_part_one(directions: List[str]) -> int:
    horizontal_position, depth = 0, 0

    for [direction, step] in directions:
        if direction == "forward":
            horizontal_position += int(step)
        if direction == "up":
            depth -= int(step)
        if direction == "down":
            depth += int(step)

    return horizontal_position * depth


def solve_part_two(directions: List[str]) -> int:
    horizontal_position, depth, aim = 0, 0, 0

    for [direction, step] in directions:
        if direction == "forward":
            horizontal_position += int(step)
            depth += aim * int(step)
        if direction == "up":
            aim -= int(step)
        if direction == "down":
            aim += int(step)

    return horizontal_position * depth


with open("input.txt", "r") as f:
    lines = f.readlines()
    directions = [line.split(" ") for line in lines]
    print(f"part_one: {solve_part_one(directions)}")
    print(f"part_two: {solve_part_two(directions)}")
