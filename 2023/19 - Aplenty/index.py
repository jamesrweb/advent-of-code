from math import prod
from typing import List, Text, Dict, Tuple

ops = {">": int.__gt__, "<": int.__lt__}
Rule = List[Tuple[Text, Text, int, Text]]
Workflows = Dict[Text, Tuple[Rule, Text]]


def build_workflows(workflow_definitions: Text) -> Workflows:
    workflows = {}

    for line in workflow_definitions.splitlines():
        name, rest = line[:-1].split("{")
        rules = rest.split(",")
        workflows[name] = ([], rules.pop())

        for rule in rules:
            comparison, goto = rule.split(":")
            target = comparison[0]
            operator = comparison[1]
            n = int(comparison[2:])
            workflows[name][0].append((target, operator, n, goto))

    return workflows


def accept(workflows: Workflows, item: Dict[Text, int], name: Text = "in") -> bool:
    if name == "R":
        return False

    if name == "A":
        return True

    rules, fallback = workflows[name]

    for target, operator, n, goto in rules:
        if ops[operator](item[target], n):
            return accept(workflows, item, goto)

    return accept(workflows, item, fallback)


def count(
    workflows: Workflows, ranges: Dict[Text, Tuple[int, int]], name: Text = "in"
) -> int:
    if name == "R":
        return 0

    if name == "A":
        return prod([high - low + 1 for low, high in ranges.values()])

    rules, fallback = workflows[name]
    total = 0

    for target, operator, n, goto in rules:
        low, high = ranges[target]
        T = (low, min(n - 1, high)) if operator == "<" else (max(n + 1, low), high)
        F = (max(n, low), high) if operator == "<" else (low, min(n, high))

        if T[0] <= T[1]:
            copy = dict(ranges)
            copy[target] = T
            total += count(workflows, copy, goto)

        if F[0] <= F[1]:
            ranges = dict(ranges)
            ranges[target] = F
        else:
            break
    else:
        total += count(workflows, ranges, fallback)

    return total


def solve_part_one(workflows: Workflows, rating_definitions: Text) -> int:
    total = 0

    for line in rating_definitions.splitlines():
        item = {}

        for segment in line[1:-1].split(","):
            target, n = segment.split("=")
            item[target] = int(n)

        if accept(workflows, item):
            total += sum(item.values())

    return total


def solve_part_two(workflows: Workflows) -> int:
    return count(workflows, {key: (1, 4000) for key in "xmas"})


with open("input.txt", "r") as file:
    workflow_definitions, rating_definitions = file.read().split("\n\n")
    workflows = build_workflows(workflow_definitions)
    part_one = solve_part_one(workflows, rating_definitions)
    part_two = solve_part_two(workflows)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
