from copy import deepcopy
from math import inf
from typing import Literal, List, Tuple, Optional, Dict

type Point = Tuple[int, int, Symbol]
type Points = List[Point]
type Symbol = Literal["start", "splitter", "beam", "empty"]
type LabMap = List[Points]
type TimelinePoint = Tuple[int, int]
type TimelineHits = Dict[TimelinePoint, int]


def char_to_symbol(char: str) -> Symbol:
    """
    Convert the given character into a `Symbol`.

    Semantically relevant characters ("S" and "^") are preserved, and any other character is normalised into an empty cell.

    Args:
        char: The raw character that was parsed from the manifold diagram.

    Returns:
        The `Symbol` that the character represents.
    """
    match char:
        case "S":
            return "start"
        case "^":
            return "splitter"
        case _:
            return "empty"


def in_bounds(lab: LabMap, row_index: int, column_index: int) -> bool:
    """
    Checks whether a given row / column index pair falls within the laboratory map.

    Args:
        lab: The laboratory map.
        row_index: The row to check.
        column_index: The column within the row to check.

    Returns:
        True when both indices fall within the map otherwise False.
    """
    return 0 <= row_index < len(lab) and 0 <= column_index < len(lab[row_index])


def get_cell(lab: LabMap, row_index: int, column_index: int) -> Optional[Point]:
    """
    Attempts to get the value of the point at a given row / column index pair within the laboratory map.

    Args:
        lab: The laboratory map.
        row_index: The row to lookup.
        column_index: The column within the row to lookup.

    Returns:
        The `Point`, or `None` when the indices fall outside the map.
    """
    if not in_bounds(lab, row_index, column_index):
        return None

    return lab[row_index][column_index]


def set_cell(lab: LabMap, row_index: int, column_index: int, symbol: Symbol) -> LabMap:
    """
    Attempts to set the `Symbol` of the `Point` at a given row / column index pair within the laboratory map.

    The written `Point` carries its own coordinates, and the map is returned unchanged when the indices fall outside it.

    Args:
        lab: The laboratory map.
        row_index: The row to update.
        column_index: The column within the row to update.
        symbol: The `Symbol` to write into the point.

    Returns:
        The laboratory map with the `Point` updated when the indices fall within the map.
    """
    if not in_bounds(lab, row_index, column_index):
        return lab

    lab[row_index][column_index] = (row_index, column_index, symbol)

    return lab


def should_exit(lab: LabMap, max_depth: int) -> bool:
    """
    Checks whether the beam simulation has finished.

    The sweep cascades through the whole manifold within a single pass.

    Args:
        lab: The laboratory map.
        max_depth: The row depth the beams must have reached.

    Returns:
        True when the simulation has finished, or there are still beams in motion, otherwise False.
    """
    min_depth = inf

    for row in lab:
        for row_index, _, symbol in row:
            if symbol == "beam":
                min_depth = min(min_depth, row_index)

    return False if min_depth == inf else min_depth >= max_depth


def calculate_timelines(lab: LabMap, timeline_hits: TimelineHits) -> int:
    """
    Attempt to calculate the number of timelines flowing out of the manifolds final row.

    Only timeline counts sitting within the maps last row are summed, so each timeline is read out exactly once as it
    exits the manifold.

    Args:
        lab: The laboratory map.
        timeline_hits: The number of timelines attached to each position the beams have reached.

    Returns:
        The total number of timelines that left the manifold through its final row.
    """
    return sum(
        value for (row, _), value in timeline_hits.items() if row == len(lab) - 1
    )


def set_timeline_target_count(
    timeline_hits: TimelineHits, row_index: int, column_index: int, carried: int
) -> TimelineHits:
    """
    Add the given carried timeline count onto the count attached to the given position.

    Positions without an existing count start from zero, and the position is assumed to be valid. No bounds checking
    takes place here.

    Args:
        timeline_hits: The timeline counts attached to the positions the beams have reached.
        row_index: The row of the position to update.
        column_index: The column within the row to update.
        carried: The number of timelines carried by the beam whose count is being moved.

    Returns:
        The timeline counts with the given positions count increased by the carried count.
    """
    target = (row_index, column_index)
    timeline_hits[target] = timeline_hits.get(target, 0) + carried

    return timeline_hits


def solve_helper(
    lab: LabMap,
    is_part_one: bool,
    started: bool,
    max_depth: int,
    total_splits: int,
    timeline_hits: TimelineHits,
) -> int:
    """
    Attempt to simulate the tachyon beam through the manifold for one part of the challenge.

    The rows are swept top-down over the mutable copy, so freshly written beams cascade the whole way down within a
    single pass. A fall to an empty slot continues the beam, a splitter stops it and emits children left and right.

    Each splitter event counts one split, and timeline counts (`carried`) attach to beams and move with them, doubling
    into each child at forks.

    Args:
        lab: The laboratory map.
        is_part_one: If the requested answer is for part one of the challenge.
        started: Whether the simulation has started, guarding against stopping before the first beam is emitted.
        max_depth: The row depth the simulation reports against.
        total_splits: The number of beam splits accumulated so far.
        timeline_hits: The number of timelines attached to each position the beams have reached.

    Returns:
        The total number of splits for part one, otherwise the total number of timelines flowing out of the
        manifolds final row.
    """
    if started and should_exit(lab, max_depth):
        return total_splits if is_part_one else calculate_timelines(lab, timeline_hits)

    next_lab = deepcopy(lab)
    next_timeline_hits = deepcopy(timeline_hits)
    next_total_splits = total_splits

    for row in next_lab:
        for row_index, column_index, symbol in row:
            carried = next_timeline_hits.get((row_index, column_index), 0)
            below = get_cell(next_lab, row_index + 1, column_index)

            if below is None or symbol not in ["start", "beam"]:
                continue

            _, _, below_symbol = below

            match below_symbol:
                case "splitter":
                    next_lab = set_cell(
                        next_lab, row_index + 1, column_index - 1, "beam"
                    )
                    next_lab = set_cell(
                        next_lab, row_index + 1, column_index + 1, "beam"
                    )
                    next_total_splits += 1

                    for side in (-1, 1):
                        next_timeline_hits = set_timeline_target_count(
                            next_timeline_hits,
                            row_index + 1,
                            column_index + side,
                            carried,
                        )
                case _:
                    next_lab = set_cell(next_lab, row_index + 1, column_index, "beam")
                    next_timeline_hits = set_timeline_target_count(
                        next_timeline_hits, row_index + 1, column_index, carried
                    )

    return solve_helper(
        next_lab, is_part_one, True, max_depth, next_total_splits, next_timeline_hits
    )


def solve(lab: LabMap, is_part_one: bool) -> int:
    """
    Attempt to repair the teleporter for the given part of the challenge.

    The map is searched for the beams start point, where a single timeline is seeded, before delegating the
    simulation to `solve_helper`.

    Args:
        lab: The laboratory map.
        is_part_one: If the requested answer is for part one of the challenge.

    Returns:
        The total number of splits for part one, otherwise the total number of timelines.
    """
    timelines: TimelineHits = dict()

    for row_index, row in enumerate(lab):
        for _, column_index, symbol in row:
            if symbol == "start":
                timelines[(row_index, column_index)] = 1

    return solve_helper(lab, is_part_one, False, 0, 0, timelines)


with open("input.txt") as f:
    laboratory_map = [
        [
            (row_index, column_index, char_to_symbol(column))
            for (column_index, column) in enumerate(row)
        ]
        for (row_index, row) in enumerate(f.readlines())
    ]

    print(f"part_one: {solve(laboratory_map, True)}")
    print(f"part_two: {solve(laboratory_map, False)}")
