from dataclasses import dataclass
import math
from typing import Sequence, Union, Literal, Tuple, Optional, Set

from adventofcode.helpers import executor, parsers

ROW = parsers.DIGIT.at_least(1)

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)

Location = Tuple[int, int]
Direction = Union[
    Literal['up'],
    Literal['down'],
    Literal['left'],
    Literal['right'],
]


@dataclass(frozen=True, kw_only=True)
class Node:
    distance: int
    source_direction: Optional[Direction]
    source_location: Optional[Location]


WeightGrid = Sequence[Sequence[int]]
NodeGrid = Sequence[Sequence[Node]]


def find_closest_unvisited_location(
        *,
        node_grid: NodeGrid,
        unvisited_locations: Set[Location],
) -> Location:
    min_distance: int = math.inf
    min_location: Optional[Location] = None
    for location in unvisited_locations:
        node = node_grid[location[0]][location[1]]
        if node.distance < min_distance:
            min_distance = node.distance
            min_location = location

    if min_location is None:
        raise Exception('unexpected')

    return min_location


def invert_direction(*, direction: Direction) -> Direction:
    match direction:
        case 'up':
            return 'down'
        case 'down':
            return 'up'
        case 'left':
            return 'right'
        case 'right':
            return 'left'
        case _:
            raise Exception('unexpected direction')


def get_next_location(*, location: Location, direction: Direction) -> Location:
    match direction:
        case 'up':
            return (location[0] - 1, location[1])
        case 'down':
            return (location[0] + 1, location[1])
        case 'left':
            return (location[0], location[1] - 1)
        case 'right':
            return (location[0], location[1] + 1)
        case _:
            raise Exception('unexpected direction')


def is_location_in_grid(*, location: Location, weight_grid: WeightGrid) -> bool:
    if location[0] < 0:
        return False
    if location[0] >= len(weight_grid):
        return False
    if location[1] < 0:
        return False
    if location[1] >= len(weight_grid[0]):
        return False
    return True


def calculate_node_grid(*, weight_grid: WeightGrid) -> NodeGrid:
    node_grid: NodeGrid = []
    for row_index, row in enumerate(weight_grid):
        nodes = []
        for column_index in range(len(row)):
            nodes.append(
                Node(
                    distance=0 if row_index == 0 and column_index == 0 else math.inf,
                    source_direction=None,
                    source_location=None,
                )
            )

        node_grid.append(nodes)

    unvisited_locations = set([
        (row_index, column_index)
        for row_index, row in enumerate(weight_grid)
        for column_index in range(len(row))
    ])

    while len(unvisited_locations) > 0:
        current_location = find_closest_unvisited_location(
            node_grid=node_grid,
            unvisited_locations=unvisited_locations,
        )
        current_node = node_grid[current_location[0]][current_location[1]]
        cell_weight = weight_grid[current_location[0]][current_location[1]]

        for direction in ('up', 'down', 'left', 'right'):
            neighbor_location = get_next_location(
                location=current_location,
                direction=direction,
            )
            if not is_location_in_grid(location=neighbor_location, weight_grid=weight_grid):
                continue

            if neighbor_location not in unvisited_locations:
                continue

            inverted_direction = invert_direction(direction=direction)
            check_location = current_location
            for _ in range(2):
                check_location = get_next_location(
                    location=check_location,
                    direction=inverted_direction,
                )
                if not is_location_in_grid(location=check_location, weight_grid=weight_grid):
                    break

                check_node = node_grid[check_location[0]][check_location[1]]
                if check_node.source_direction != direction:
                    break
            else:
                # all 3 check directions were in a row
                continue

            neighbor_node = node_grid[neighbor_location[0]][neighbor_location[1]]
            new_distance = current_node.distance + cell_weight
            if new_distance < neighbor_node.distance:
                node_grid[neighbor_location[0]][neighbor_location[1]] = Node(
                    distance=new_distance,
                    source_direction=direction,
                    source_location=current_location,
                )

        unvisited_locations.remove(current_location)

        if current_location == (len(weight_grid) - 1, len(weight_grid[0]) - 1):
            break

    return node_grid


def print_node_grid(*, node_grid: NodeGrid) -> None:
    path: Set[Location] = set()
    current_location = (len(node_grid) - 1, len(node_grid[0]) - 1)
    while current_location != (0, 0):
        path.add(current_location)
        node = node_grid[current_location[0]][current_location[1]]
        current_location = node.source_location

    for row_index, row in enumerate(node_grid):
        for column_index, node in enumerate(row):
            location = (row_index, column_index)
            if location in path:
                match node.source_direction:
                    case 'up':
                        char = '^'
                    case 'down':
                        char = 'v'
                    case 'left':
                        char = '<'
                    case 'right':
                        char = '>'
                    case _:
                        raise Exception('unexpected direction')
            else:
                # char = str(node.distance)
                char = '0'

            print(char, end="")
        print()


def solution(content: str, /) -> int:
    weight_grid = CONTENT.parse(content)
    node_grid = calculate_node_grid(weight_grid=weight_grid)
    print_node_grid(node_grid=node_grid)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
