from typing import List, Tuple


def digits_to_int(digits: List[int]) -> int:
    return int("".join(list(map(str, digits))))


def solve(instructions: List[str]) -> int:
    terms: List[Tuple[int, int, int]] = []
    output_digits_min: List[int] = [1] * 14
    output_digits_max: List[int] = [9] * 14
    instruction_stack: List[Tuple[int, int]] = []

    for i in range(0, len(instructions), 18):
        terms.append([int(instructions[i + j].split(" ").pop()) for j in [4, 5, 15]])

    for i, (a, b, c) in enumerate(terms):
        if a == 1:
            instruction_stack.append((i, c))
            continue

        j, prev_c = instruction_stack.pop()
        complement = prev_c + b
        output_digits_max[j] = min(9, 9 - complement)
        output_digits_max[i] = output_digits_max[j] + complement
        output_digits_min[j] = max(1, 1 - complement)
        output_digits_min[i] = output_digits_min[j] + complement

    return (digits_to_int(output_digits_max), digits_to_int(output_digits_min))


with open("input.txt", "r") as f:
    instructions = f.readlines()
    part_one, part_two = solve(instructions)

    print(f"part_one: {part_one}")
    print(f"part_two: {part_two}")
