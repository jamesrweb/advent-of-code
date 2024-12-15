from functools import cache
from os import path


@cache
def count(stone, steps):
    if steps == 0:
        return 1

    if stone == 0:
        return count(1, steps - 1)

    string = str(stone)
    length = len(string)

    if length % 2 == 0:
        return count(int(string[: length // 2]), steps - 1) + count(
            int(string[length // 2 :]), steps - 1
        )

    return count(stone * 2024, steps - 1)


with open(path.dirname(path.realpath(__file__)) + "/input.txt") as file:
    stones = [int(stone.strip()) for stone in file.read().split()]
    part_one = sum([count(stone, 25) for stone in stones])
    part_two = sum([count(stone, 75) for stone in stones])

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
