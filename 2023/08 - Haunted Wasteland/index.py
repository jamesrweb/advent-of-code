from math import lcm
from typing import Text, List, Dict

Network = Dict[Text, List[Text]]


def build_network(nodes: List[Text]) -> Network:
    network = {}

    for node in nodes:
        position, targets = map(lambda x: x.strip(), node.split("="))
        network[position] = [
            target
            for target in map(
                lambda x: x.strip(), targets.lstrip("(").rstrip(")").split(",")
            )
        ]

    return network


def solve_part_one(
    steps: Text,
    network: Network,
    current_position: Text = "AAA",
    target_position: Text = "ZZZ",
) -> int:
    step_count = 0
    next_position = current_position
    path = steps

    while next_position != target_position:
        step_count += 1
        node = network[next_position]
        next_position = node[0] if path[0] == "L" else node[1]
        path = path[1:] + path[0]

    return step_count


def solve_part_two(steps: Text, network: Network) -> int:
    start_positions = [key for key in network if key.endswith("A")]
    cycles = []

    for position in start_positions:
        step_count = 0
        path = steps
        cycle = []
        first_z = None
        next_position = position

        while True:
            while step_count == 0 or not next_position.endswith("Z"):
                step_count += 1
                node = network[next_position]
                next_position = node[0] if path[0] == "L" else node[1]
                path = path[1:] + path[0]

            cycle.append(step_count)

            if next_position == first_z:
                break

            if first_z is None:
                first_z = next_position
                step_count = 0

        cycles.append(cycle)

    return lcm(*[cycle[0] for cycle in cycles])


with open("input.txt", "r") as file:
    steps, _, *nodes = file.read().splitlines()
    network = build_network(nodes)
    part_one = solve_part_one(steps, network)
    part_two = solve_part_two(steps, network)

    print("Part one: " + str(part_one))
    print("Part two: " + str(part_two))
