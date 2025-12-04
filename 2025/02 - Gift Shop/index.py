from typing import Iterable, List


def fulfills_split_invalidity(id: int) -> bool:
    stringified_id = str(id)
    pivot = len(stringified_id) // 2
    left = stringified_id[:pivot]
    right = stringified_id[pivot:]

    return left == right


def fulfills_repeating_invalidity(id: int) -> bool:
    stringified_id = str(id)

    if len(stringified_id) < 2:
        return False

    temp = (stringified_id + stringified_id)[1:-1]

    return stringified_id in temp


class ProductIdRange:
    def __init__(self, start: int, end: int) -> None:
        self.start: int = start
        self.end: int = end
        self.range = range(self.start, self.end + 1)

    @staticmethod
    def from_string(product_id_range: str) -> "ProductIdRange":
        start, end = product_id_range.split("-")

        assert start.isnumeric() and end.isnumeric()

        return ProductIdRange(int(start), int(end))

    def list_invalid_ids(self, is_part_one: bool) -> List[int]:
        predicate = (
            fulfills_split_invalidity if is_part_one else fulfills_repeating_invalidity
        )

        return [product_id for product_id in self.range if predicate(product_id)]


def solve(product_id_ranges: Iterable[str], is_part_one: bool) -> int:
    product_ranges = [
        ProductIdRange.from_string(product_id_range)
        for product_id_range in product_id_ranges
    ]
    invalid_ids = [
        product_id
        for product_range in product_ranges
        for product_id in product_range.list_invalid_ids(is_part_one)
    ]

    return sum(invalid_ids)


with open("input.txt", "r") as f:
    product_id_ranges = f.read().split(",")

    print(f"part_one: {solve(product_id_ranges, True)}")
    print(f"part_two: {solve(product_id_ranges, False)}")
