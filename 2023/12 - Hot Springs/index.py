from typing import List, Text, Tuple
from functools import lru_cache


class Record:
    configuration: Text
    condition_records: Tuple[int]

    def __init__(self, configuration: Text, condition_records: Tuple[int]) -> None:
        self.configuration = configuration
        self.condition_records = condition_records

    def calculate_arrangements(self) -> int:
        @lru_cache
        def count_arrangements(
            configuration: Text, condition_records: Tuple[int]
        ) -> int:
            if not condition_records:
                return 0 if "#" in configuration else 1
            if not configuration:
                return 1 if not condition_records else 0

            result = 0

            if configuration[0] in ".?":
                result += count_arrangements(configuration[1:], condition_records)
            if configuration[0] in "#?":
                if (
                    condition_records[0] <= len(configuration)
                    and "." not in configuration[: condition_records[0]]
                    and (
                        condition_records[0] == len(configuration)
                        or configuration[condition_records[0]] != "#"
                    )
                ):
                    result += count_arrangements(
                        configuration[condition_records[0] + 1 :], condition_records[1:]
                    )

            return result

        return count_arrangements(self.configuration, self.condition_records)


def parse_input(lines: List[Text]) -> List[Record]:
    records = []

    for line in lines:
        configuration, numbers = line.split()
        condition_records = map(int, numbers.split(","))

        records.append(Record(configuration, tuple(condition_records)))

    return records


def solve_part_one(records: List[Record]) -> int:
    return sum([record.calculate_arrangements() for record in records])


def solve_part_two(records: List[Record]) -> int:
    updated_records = [
        Record("?".join([record.configuration] * 5), record.condition_records * 5)
        for record in records
    ]
    return sum([record.calculate_arrangements() for record in updated_records])


with open("input.txt", "r") as file:
    lines = file.read().splitlines()
    records = parse_input(lines)
    part_one = solve_part_one(records)
    part_two = solve_part_two(records)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
