from typing import List
from itertools import combinations

InputData = List[str]
ParsedData = List[int]


def parse_lines(lines: InputData) -> ParsedData:
    return list(map(lambda line: int(line), lines))


def solve_part_one(lines: ParsedData, preamble: int) -> int:
    for index in range(preamble, len(lines)):
        current = lines[index]
        haystack = lines[index-preamble:index]
        possibilities = combinations(haystack, 2)

        for a, b in possibilities:
            if a + b == current:
                break
        else:
            return current

    return -1


def part_two_helper(lines: ParsedData, target: int, index: int = 0) -> int:
    if index == len(lines) - 1:
        return -1

    total = 0
    totaled = []
    pointer = index

    while total < target:
        totaled.append(lines[pointer])
        total = sum(totaled)
        pointer += 1

    if total == target:
        arranged = sorted(totaled)
        return arranged[0] + arranged[-1]

    return part_two_helper(lines, target, index + 1)


def solve_part_two(lines: ParsedData, preamble: int) -> int:
    target = solve_part_one(lines, preamble)
    return part_two_helper(lines, target)


with open("input.txt", "r") as f:
    lines = parse_lines(f.readlines())
    preamble = 25
    print(f"part_one: {solve_part_one(lines, preamble)}")
    print(f"part_two: {solve_part_two(lines, preamble)}")
