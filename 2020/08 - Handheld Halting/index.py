from copy import deepcopy
from typing import List, Set, Tuple

Ops = List[str]
ExecutedOps = Set[int]
OpDefinition = Tuple[str, str]


def convert(line: str) -> OpDefinition:
    current = line.replace("\n", "")
    operation, value = current.split(" ")
    return (operation, value)


def solve_part_one(
    lines: Ops, index: int = 0, accumulator: int = 0, visited: ExecutedOps = set()
) -> int:
    if index in visited:
        return accumulator

    visited.add(index)
    operation, value = convert(lines[index])

    if operation == "nop":
        index += 1

    if operation == "acc":
        accumulator += int(value)
        index += 1

    if operation == "jmp":
        index += int(value)

    return solve_part_one(lines, index, accumulator, visited)


def solve_part_two(lines: Ops, index: int = 0) -> int:
    clone = deepcopy(lines)
    instruction, _ = convert(clone[index])

    if instruction == "jmp":
        clone[index] = clone[index].replace("jmp", "nop")
    elif instruction == "nop":
        clone[index] = clone[index].replace("nop", "jmp")

    pointer = 0
    accumulator = 0
    visited: ExecutedOps = set()

    while pointer not in visited:
        visited.add(pointer)
        operation, value = clone[pointer].split()

        if operation == "nop":
            pointer += 1
        elif operation == "jmp":
            pointer += int(value)
        elif operation == "acc":
            accumulator += int(value)
            pointer += 1

        if pointer == (len(clone) - 1):
            return accumulator

    return solve_part_two(lines, index + 1)


with open("input.txt", "r") as f:
    lines: Ops = f.readlines()
    print(f"part_one: {solve_part_one(lines)}")
    print(f"part_two: {solve_part_two(lines)}")
