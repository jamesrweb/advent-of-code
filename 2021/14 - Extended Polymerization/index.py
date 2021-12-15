from functools import cache
from collections import Counter
from typing import Dict, List, Tuple

Polymer = str
Rules = Dict[str, str]

EOL = "\n"


def parse_parts_from_lines(lines: List[str]) -> Tuple[Polymer, Rules]:
    initial_polymer, raw_rules = lines

    rules = {}
    for rule in raw_rules.split(EOL):
        pair, insertion = rule.split(" -> ")
        rules[pair] = insertion

    return initial_polymer, rules


def grow_polymer(polymer: Polymer, rules: Rules, depth: int) -> Counter[str, int]:
    @cache
    def grow_polymer_helper(polymer: str, depth: int) -> Counter:
        nonlocal rules

        polymer_counter = Counter()
        if depth > 0:
            for i in range(1, len(polymer)):
                element = rules[polymer[i - 1 : i + 1]]
                polymer_counter.update(element)
                new_polymer = polymer[i - 1] + element + polymer[i]
                new_polymer_counter = grow_polymer_helper(
                    new_polymer,
                    depth - 1,
                )
                polymer_counter += new_polymer_counter

        return polymer_counter

    start_count = Counter(polymer)
    char_count = start_count + grow_polymer_helper(polymer, depth)
    return char_count


def commonalityDifferential(polymer_element_counts: Counter[str, int]) -> int:
    sorted_counts = polymer_element_counts.most_common()

    return sorted_counts[0][1] - sorted_counts[-1][1]


def solve(polymer: Polymer, rules: Rules, depth: int) -> int:
    polymer_element_counts = grow_polymer(polymer, rules, depth)
    score = commonalityDifferential(polymer_element_counts)

    return score


with open("input.txt", "r") as f:
    lines = f.read().split(EOL + EOL)
    polymer, rules = parse_parts_from_lines(lines)

    print(f"part_one: {solve(polymer, rules, 10)}")
    print(f"part_two: {solve(polymer, rules, 40)}")
