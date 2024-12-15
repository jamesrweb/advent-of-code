from os import path
from re import findall


def count_cheapest_token_count_to_victory(blocks, handle_conversion_error):
    total = 0

    for block in blocks:
        ax, ay, bx, by, px, py = map(int, findall(r"\d+", block))

        if handle_conversion_error:
            px += 10000000000000
            py += 10000000000000

        a_presses_count = (px * by - py * bx) / (ax * by - ay * bx)
        b_presses_count = (px - ax * a_presses_count) / bx

        if a_presses_count % 1 == b_presses_count % 1 == 0:
            if not handle_conversion_error:
                if a_presses_count <= 100 and b_presses_count <= 100:
                    total += int(a_presses_count * 3 + b_presses_count)
            else:
                total += int(a_presses_count * 3 + b_presses_count)

    return total


with open(path.dirname(path.realpath(__file__)) + "/input.txt") as file:
    blocks = [block.strip() for block in file.read().split("\n\n")]
    part_one = count_cheapest_token_count_to_victory(blocks.copy(), False)
    part_two = count_cheapest_token_count_to_victory(blocks.copy(), True)

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
