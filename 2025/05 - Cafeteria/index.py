from typing import List

type FreshStockRanges = List[range]
type IngredientStockIds = List[int]


def ingredient_range(bounds: List[int]) -> range:
    """
    Convert the given inclusive bounds into a `range`.

    The upper bound is inclusive, so it is shifted by one to produce the exclusive stop of the range.

    Args:
        bounds: The inclusive lower and upper bounds of an ingredient ID range.

    Returns:
        The range covering every ingredient ID within the given bounds.
    """
    return range(bounds[0], bounds[1] + 1)


def overlapping(range_one: range, range_two: range) -> bool:
    """
    Checks whether two ranges intersect or merely touch at a bound.

    Args:
        range_one: The first range.
        range_two: The second range.

    Returns:
        True when the ranges touch at a bound otherwise False.
    """
    return range_one.start <= range_two.stop and range_one.stop >= range_two.start


def solve_part_one(
    fresh_ranges: FreshStockRanges, available_stock_ids: IngredientStockIds
) -> int:
    """
    Attempt to calculate how many of the available stock IDs are considered fresh.

    An ingredient ID is considered fresh when it falls within any of the fresh ingredient ranges.

    Args:
        fresh_ranges: The fresh ingredient ID ranges.
        available_stock_ids: The ingredient IDs available in stock.

    Returns:
        How many of the available stock IDs are considered fresh.
    """
    freshness_status = dict()

    for ingredient_stock_id in available_stock_ids:
        freshness_status.setdefault(ingredient_stock_id, False)

        for fresh_range in fresh_ranges:
            is_fresh = freshness_status.pop(ingredient_stock_id)
            in_fresh_range = ingredient_stock_id in fresh_range

            freshness_status[ingredient_stock_id] = True if is_fresh else in_fresh_range

    return list(freshness_status.values()).count(True)


def solve_part_two(fresh_ranges: FreshStockRanges) -> int:
    """
    Attempt to calculate how many ingredient IDs are considered to be fresh.

    Overlapping and adjacent ranges are consolidated before counting, so ingredient IDs shared between ranges are only counted once.

    Args:
        fresh_ranges: The fresh ingredient ID ranges.

    Returns:
        How many ingredient IDs are considered to be fresh.
    """
    consolidated_ranges = []

    for fresh_range in sorted(fresh_ranges, key=lambda key: key.start):
        empty = len(consolidated_ranges) == 0

        if empty or not overlapping(fresh_range, consolidated_ranges[-1]):
            consolidated_ranges.append(fresh_range)
            continue

        tail_range = consolidated_ranges[-1]
        limit = max(tail_range.stop, fresh_range.stop)
        consolidated_ranges[-1] = range(tail_range.start, limit)

    return sum(segment.stop - segment.start for segment in consolidated_ranges)


with open("input.txt") as f:
    ranges, ingredient_ids = f.read().split("\n\n")
    ingredient_stock_ids = [
        int(ingredient_id) for ingredient_id in ingredient_ids.splitlines()
    ]
    fresh_ingredient_ranges = [
        ingredient_range([int(value) for value in fresh_ingredient_id_range.split("-")])
        for fresh_ingredient_id_range in ranges.splitlines()
    ]

    print(f"part_one: {solve_part_one(fresh_ingredient_ranges, ingredient_stock_ids)}")
    print(f"part_two: {solve_part_two(fresh_ingredient_ranges)}")
