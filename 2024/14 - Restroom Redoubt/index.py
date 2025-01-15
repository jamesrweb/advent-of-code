from functools import reduce
from os import path
from re import findall
from typing import List, Tuple, Optional

# Types

InputPosition = str
InputPositions = List[InputPosition]
RobotPosition = Tuple[int, int]
RobotPositions = List[RobotPosition]
RobotPositionWithVelocity = Tuple[int, int, int, int]
RobotPositionsWithVelocity = List[RobotPositionWithVelocity]

# Constants

WIDTH = 101
HEIGHT = 103
VERTICAL_MIDDLE = (HEIGHT - 1) // 2
HORIZONTAL_MIDDLE = (WIDTH - 1) // 2


def find_robots_from_positions(
    input_positions: InputPositions,
) -> RobotPositionsWithVelocity:
    def to_robot_position(
        robot_positions: RobotPositionsWithVelocity, position: InputPosition
    ) -> RobotPositionsWithVelocity:
        x, y, dx, dy = map(int, findall(r"-?\d+", position))
        robot = (x, y, dx, dy)

        robot_positions.append(robot)

        return robot_positions

    return reduce(to_robot_position, input_positions, [])


def robot_positions_after_seconds(
    robot_positions_with_velocities: RobotPositionsWithVelocity, seconds: int
) -> RobotPositions:
    def to_position_after_seconds(
        robot_position_with_velocity: RobotPositionWithVelocity,
    ) -> RobotPosition:
        x, y, dx, dy = robot_position_with_velocity

        return (x + dx * seconds) % WIDTH, (y + dy * seconds) % HEIGHT

    return list(map(to_position_after_seconds, robot_positions_with_velocities))


def safety_factor_for_positions(robot_positions: RobotPositions) -> int:
    top_left = 0
    top_right = 0
    bottom_left = 0
    bottom_right = 0

    for x, y in robot_positions:
        if x == HORIZONTAL_MIDDLE or y == VERTICAL_MIDDLE:
            continue

        left = x < HORIZONTAL_MIDDLE
        top = y < VERTICAL_MIDDLE

        top_left += int(left and top)
        bottom_left += int(left and not top)
        top_right += int(not left and top)
        bottom_right += int(not left and not top)

    return top_left * top_right * bottom_left * bottom_right


def min_safety_factor_until_christmas_tree_positions(
    input_positions: InputPositions,
) -> Optional[int]:
    min_safety_factor = float("inf")
    best_iteration = None
    robots = find_robots_from_positions(input_positions)

    for seconds in range(WIDTH * HEIGHT):
        future_positions = robot_positions_after_seconds(robots, seconds)
        safety_factor = safety_factor_for_positions(future_positions)

        if safety_factor < min_safety_factor:
            min_safety_factor = safety_factor
            best_iteration = seconds

    return best_iteration


def calculate_safety_factor(input_positions: InputPositions) -> int:
    robots = find_robots_from_positions(input_positions)
    future_positions = robot_positions_after_seconds(robots, 100)

    return safety_factor_for_positions(future_positions)


with open(path.dirname(path.realpath(__file__)) + "/input.txt") as file:
    positions = file.readlines()
    part_one = calculate_safety_factor(positions.copy())
    part_two = min_safety_factor_until_christmas_tree_positions(positions.copy())

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
