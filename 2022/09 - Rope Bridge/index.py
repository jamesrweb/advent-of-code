from typing import List, Tuple


class Coord(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def step(self, direction: chr) -> None:
        if direction == "U":
            self.y += 1
        if direction == "D":
            self.y -= 1
        if direction == "L":
            self.x -= 1
        if direction == "R":
            self.x += 1


class Head(Coord):
    def __init__(self):
        super().__init__()


class Tail(Coord):
    def __init__(self):
        super().__init__()

        self.history = set()

    def follow(self, coords: Tuple[int, int]) -> None:
        x, y = coords
        dist_x = x - self.x
        dist_y = y - self.y

        if abs(dist_x) == 2 and not dist_y:
            self.x += 1 if dist_x > 0 else -1

        elif abs(dist_y) == 2 and not dist_x:
            self.y += 1 if dist_y > 0 else -1

        elif (abs(dist_y) == 2 and abs(dist_x) in (1, 2)) or (
            abs(dist_x) == 2 and abs(dist_y) in (1, 2)
        ):
            self.x += 1 if dist_x > 0 else -1
            self.y += 1 if dist_y > 0 else -1

        self.history.add((self.x, self.y))


class Solution(object):
    def __init__(self, directions: List[str]) -> None:
        self.directions = directions

    def solve_part_one(self) -> int:
        head = Head()
        tail = Tail()

        for direction in self.directions:
            direction, steps = direction.split(" ")

            for _ in range(int(steps)):
                head.step(direction)
                tail.follow((head.x, head.y))

        return len(tail.history)

    def solve_part_two(self) -> int:
        head = Head()
        tails = [Tail() for _ in range(9)]

        for direction in self.directions:
            direction, steps = direction.split()
            for _ in range(int(steps)):
                head.step(direction)
                tails[0].follow((head.x, head.y))

                for index in range(1, 9):
                    last_tail = tails[index - 1]
                    tails[index].follow((last_tail.x, last_tail.y))

        return len(tails.pop().history)


with open("input.txt") as file:
    solution = Solution(file.readlines())

    print(f"Part one: {solution.solve_part_one()}")
    print(f"Part two: {solution.solve_part_two()}")
