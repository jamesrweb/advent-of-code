from functools import reduce
from typing import Dict, Tuple, List

Lines = List[str]
Node = Tuple[str, int]
NodeList = List[Node]
Graph = Dict[str, NodeList]


class BagGraph(object):
    def __init__(self, lines: Lines):
        super().__init__()
        self.graph = self.__parse(lines)

    def __details_reducer(self, accumulator: NodeList, current: str) -> NodeList:
        tokens = current.split(" ")
        node = (f"{tokens[1]} {tokens[2]}", int(tokens[0]))
        return accumulator + [node]

    def __parse_details(self, details: str) -> NodeList:
        if "no other bags" in details:
            return []

        return reduce(self.__details_reducer, details.split(", "), [])

    def __parse(self, lines: Lines) -> Graph:
        graph: Graph = {}
        for line in lines:
            index = line.find("bags")
            start = line[: index - 1]
            details = line[index + len("bags contain ") :]
            graph[start] = self.__parse_details(details)
        return graph


def dfs(graph: Graph, start: str, search: str) -> bool:
    if start == search:
        return True

    for next, _ in graph[start]:
        if dfs(graph, next, search):
            return True

    return False


def dfs_count(graph: Graph, start: str) -> int:
    def count_reducer(accumulator: int, current: Node) -> int:
        return accumulator + current[1] * dfs_count(graph, current[0])

    return reduce(count_reducer, graph[start], 1)


def solve_part_one(graph: Graph, search: str) -> int:
    def part_one_reducer(accumulator: int, current: str) -> int:
        if current != search and dfs(graph, current, search):
            accumulator += 1
        return accumulator

    return reduce(part_one_reducer, graph.keys(), 0)


def solve_part_two(graph: Graph, search: str) -> int:
    return dfs_count(graph, search) - 1


with open("input.txt", "r") as f:
    lines = f.readlines()
    graph = BagGraph(lines).graph
    search = "shiny gold"
    print(f"part_one: {solve_part_one(graph, search)}")
    print(f"part_two: {solve_part_two(graph, search)}")
