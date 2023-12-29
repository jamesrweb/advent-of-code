from copy import deepcopy
from math import gcd
from typing import List, Text, Dict, Tuple
from collections import deque


class Module:
    def __init__(self, name: Text, type: Text, outputs: List[Text]):
        self.name = name
        self.type = type
        self.outputs = outputs
        self.memory = "off" if type == "%" else {}


Modules = Dict[Text, Module]
BroadcastTargets = List[Text]
Configuration = Tuple[Modules, BroadcastTargets]


def build_configuration(lines: List[Text]) -> Configuration:
    modules: Modules = {}
    broadcast_targets: BroadcastTargets = []

    for line in lines:
        left, right = line.strip().split(" -> ")
        outputs = right.split(", ")

        if left == "broadcaster":
            broadcast_targets = outputs
            continue

        type = left[0]
        name = left[1:]
        modules[name] = Module(name, type, outputs)

    for name, module in modules.items():
        for output in module.outputs:
            if output in modules and modules[output].type == "&":
                modules[output].memory[name] = "low"

    return modules, broadcast_targets


def solve_part_one(configuration: Configuration) -> int:
    modules, broadcast_targets = configuration
    low = 0
    high = 0

    for _ in range(1000):
        low += 1
        queue = deque(
            [
                ("broadcaster", broadcast_target, "low")
                for broadcast_target in broadcast_targets
            ]
        )

        while queue:
            origin, target, pulse = queue.popleft()

            if pulse == "low":
                low += 1
            else:
                high += 1

            if target not in modules:
                continue

            module = modules[target]

            if module.type == "%":
                if pulse != "low":
                    continue

                module.memory = "on" if module.memory == "off" else "off"
                outgoing = "high" if module.memory == "on" else "low"

                for output in module.outputs:
                    queue.append((module.name, output, outgoing))
            else:
                module.memory[origin] = pulse
                outgoing = (
                    "low"
                    if all(value == "high" for value in module.memory.values())
                    else "high"
                )

                for output in module.outputs:
                    queue.append((module.name, output, outgoing))

    return low * high


def solve_part_two(configuration: Configuration) -> int:
    modules, broadcast_targets = configuration
    cycle_lengths = {}
    presses = 0
    (feed,) = [name for name, module in modules.items() if "rx" in module.outputs]
    seen = {name: 0 for name, module in modules.items() if feed in module.outputs}

    while True:
        presses += 1
        queue = deque(
            [
                ("broadcaster", broadcast_target, "low")
                for broadcast_target in broadcast_targets
            ]
        )

        while queue:
            origin, target, pulse = queue.popleft()

            if target not in modules:
                continue

            module = modules[target]

            if module.name == feed and pulse == "high":
                seen[origin] += 1

                if origin in cycle_lengths:
                    assert presses == seen[origin] * cycle_lengths[origin]

                cycle_lengths[origin] = presses

                if all(seen.values()):
                    product = 1

                    for cycle_length in cycle_lengths.values():
                        product = product * cycle_length // gcd(product, cycle_length)

                    return product

            if module.type == "%":
                if pulse != "low":
                    continue

                module.memory = "on" if module.memory == "off" else "off"
                outgoing = "high" if module.memory == "on" else "low"

                for output in module.outputs:
                    queue.append((module.name, output, outgoing))
            else:
                module.memory[origin] = pulse
                outgoing = (
                    "low"
                    if all(value == "high" for value in module.memory.values())
                    else "high"
                )

                for output in module.outputs:
                    queue.append((module.name, output, outgoing))


with open("input.txt", "r") as file:
    lines = file.read().splitlines()
    configuration = build_configuration(lines)
    part_one = solve_part_one(deepcopy(configuration))
    part_two = solve_part_two(deepcopy(configuration))

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
