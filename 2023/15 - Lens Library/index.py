from typing import Text


def hash(input: Text) -> int:
    hash = 0

    for character in input:
        hash = (hash + ord(character)) * 17 % 256

    return hash


def solve_part_one(input: Text) -> int:
    return sum(map(hash, input.split(",")))


def solve_part_two(input: Text) -> int:
    boxes = [dict() for _ in range(256)]

    for step in input.split(","):
        if step[-1] == "-":
            label = step[:-1]
            boxes[hash(label)].pop(label, None)
        else:
            label, focus = step.split("=")
            boxes[hash(label)][label] = int(focus)

    return sum(
        [
            box_index * focus_index * focus
            for box_index, box in enumerate(boxes, 1)
            for focus_index, focus in enumerate(box.values(), 1)
        ]
    )


with open("input.txt", "r") as file:
    input = file.read()
    part_one = solve_part_one(input)
    part_two = solve_part_two(input)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
