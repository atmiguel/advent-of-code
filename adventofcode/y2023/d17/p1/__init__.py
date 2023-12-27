from dataclasses import dataclass
import math
from typing import List, Union, Literal, Tuple, Optional, Dict

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
class Source:
    # direction from source's perspective
    direction: Direction
    location: Location


@dataclass(kw_only=True)
class Node:
    distance_from_start: int
    sources: List[Source]
    visited: bool
    weight: int


@dataclass(frozen=True, kw_only=True)
class Input:
    end_location: Location
    nodes_by_location: Dict[Location, Node]
    start_location: Location


def print_nodes(*, end_location: Location, nodes_by_location: Dict[Location, Node]) -> None:
    for row_index in range(end_location[0]):
        for column_index in range(end_location[1]):
            location = (row_index, column_index)
            node = nodes_by_location[location]
            if node.distance_from_start < 10:
                value = f' {node.distance_from_start} '
            elif node.distance_from_start < 100:
                value = f' {node.distance_from_start}'
            else:
                value = str(node.distance_from_start)

            print(value, end=" ")
        print()
        print()

# def print_node_grid(*, node_grid: NodeGrid) -> None:
#     for row_index, row in enumerate(node_grid):
#         for column_index, node in enumerate(row):
#             location = (row_index, column_index)
#             if location in path:
#                 match node.source_direction:
#                     case 'up':
#                         char = '^'
#                     case 'down':
#                         char = 'v'
#                     case 'left':
#                         char = '<'
#                     case 'right':
#                         char = '>'
#                     case _:
#                         raise Exception('unexpected direction')
#             else:
#                 # char = str(node.distance)
#                 char = '0'

#             print(char, end="")
#         print()


def parse_input(*, content: str) -> Input:
    grid = CONTENT.parse(content)
    start_location = (0, 0)

    nodes_by_location = {}
    for row_index, row in enumerate(grid):
        for column_index, cell in enumerate(row):
            location = (row_index, column_index)
            distance_from_start = cell if location == start_location else math.inf

            node = Node(
                distance_from_start=distance_from_start,
                sources=[],
                visited=False,
                weight=cell,
            )

            nodes_by_location[location] = node
            end_location = location

    return Input(
        end_location=end_location,
        nodes_by_location=nodes_by_location,
        start_location=start_location,
    )


def find_closest_unvisited_location(*, nodes_by_location: Dict[Location, Node]) -> Optional[Location]:
    min_distance: int = math.inf
    min_location: Optional[Location] = None
    for location, node in nodes_by_location.items():
        if node.visited:
            continue

        if node.distance_from_start < min_distance:
            min_distance = node.distance_from_start
            min_location = location

    return min_location


def get_all_neighbor_locations(*, location: Location) -> Dict[Direction, Location]:
    row, column = location
    return {
        'up': (row - 1, column),
        'down': (row + 1, column),
        'left': (row, column - 1),
        'right': (row, column + 1),
    }


def find_shortest_routes(*, current_location: Optional[Location], input_: Input) -> Dict[Location, Node]:
    if current_location is None:
        current_location = input_.start_location

    # while end location node has not been visited
    while not input_.nodes_by_location[input_.end_location].visited and current_location is not None:
        current_node = input_.nodes_by_location[current_location]

        print_nodes(
            end_location=input_.end_location,
            nodes_by_location=input_.nodes_by_location,
        )
        input()

        # update all neighbors
        neighbor_locations_by_direction = get_all_neighbor_locations(location=current_location)
        for neighbor_direction, neighbor_location in neighbor_locations_by_direction.items():
            neighbor_node = input_.nodes_by_location.get(neighbor_location)
            # skip if non-existent
            if neighbor_node is None:
                continue
            # skip if visited
            if neighbor_node.visited:
                continue

            # skip if direction of last two steps are the same direction
            if len(current_node.sources) == 1:
                source = current_node.sources[0]
                if source.direction == neighbor_direction:
                    source_node = input_.nodes_by_location[source.location]
                    if len(source_node.sources) == 1:
                        source_source = source_node.sources[0]
                        if source_source.direction == neighbor_direction:
                            continue

            new_distance = current_node.distance_from_start + neighbor_node.weight
            if new_distance == neighbor_node.distance_from_start:
                neighbor_node.sources.append(
                    Source(
                        direction=neighbor_direction,
                        location=current_location,
                    )
                )
            elif new_distance < neighbor_node.distance_from_start:
                neighbor_node.distance_from_start = new_distance
                neighbor_node.sources = [Source(
                    direction=neighbor_direction,
                    location=current_location,
                )]

        current_node.visited = True
        current_location = find_closest_unvisited_location(nodes_by_location=input_.nodes_by_location)

    return input_.nodes_by_location


def solution(content: str, /) -> int:
    input_ = parse_input(content=content)
    nodes_by_location = find_shortest_routes(current_location=None, input_=input_)

    return nodes_by_location[input_.end_location].distance_from_start


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
