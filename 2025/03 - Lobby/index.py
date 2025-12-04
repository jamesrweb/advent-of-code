from typing import List


def solve(battery_banks: List[List[int]], is_part_one: bool) -> int:
    size = 2 if is_part_one else 12
    total = 0

    for battery_bank in battery_banks:
        jolts = 0

        for index in range(size - 1):
            digit = max(battery_bank[: index - (size - 1)])
            battery_bank = battery_bank[battery_bank.index(digit) + 1 :]
            jolts = (jolts * 10) + digit

        jolts = (jolts * 10) + max(battery_bank)
        total += jolts

    return total


with open("input.txt", "r") as f:
    battery_banks = [
        [int(battery) for battery in line if battery.isnumeric()]
        for line in f.readlines()
    ]

    print(f"part_one: {solve(battery_banks, True)}")
    print(f"part_two: {solve(battery_banks, False)}")
