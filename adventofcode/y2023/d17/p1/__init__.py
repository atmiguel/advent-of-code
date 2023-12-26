from dataclasses import dataclass
import math
from typing import Sequence, Union, Literal, Tuple, Optional, Set, Dict

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
    source: Optional[Source]
    visited: bool
    weight: int


@dataclass(frozen=True, kw_only=True)
class Input:
    end_location: Location
    nodes_by_location: Dict[Location, Node]
    start_location: Location


# def calculate_node_grid(*, weight_grid: WeightGrid) -> NodeGrid:
#     node_grid: NodeGrid = []
#     for row_index, row in enumerate(weight_grid):
#         nodes = []
#         for column_index in range(len(row)):
#             nodes.append(
#                 Node(
#                     distance=0 if row_index == 0 and column_index == 0 else math.inf,
#                     source_direction=None,
#                     source_location=None,
#                 )
#             )

#         node_grid.append(nodes)

#     unvisited_locations = set([
#         (row_index, column_index)
#         for row_index, row in enumerate(weight_grid)
#         for column_index in range(len(row))
#     ])

#     while len(unvisited_locations) > 0:
#         current_location = find_closest_unvisited_location(
#             node_grid=node_grid,
#             unvisited_locations=unvisited_locations,
#         )
#         current_node = node_grid[current_location[0]][current_location[1]]
#         cell_weight = weight_grid[current_location[0]][current_location[1]]

#         for direction in ('up', 'down', 'left', 'right'):
#             neighbor_location = get_next_location(
#                 location=current_location,
#                 direction=direction,
#             )
#             if not is_location_in_grid(location=neighbor_location, weight_grid=weight_grid):
#                 continue

#             if neighbor_location not in unvisited_locations:
#                 continue

#             inverted_direction = invert_direction(direction=direction)
#             check_location = current_location
#             for _ in range(2):
#                 check_location = get_next_location(
#                     location=check_location,
#                     direction=inverted_direction,
#                 )
#                 if not is_location_in_grid(location=check_location, weight_grid=weight_grid):
#                     break

#                 check_node = node_grid[check_location[0]][check_location[1]]
#                 if check_node.source_direction != direction:
#                     break
#             else:
#                 # all 3 check directions were in a row
#                 continue

#             neighbor_node = node_grid[neighbor_location[0]][neighbor_location[1]]
#             new_distance = current_node.distance + cell_weight
#             if new_distance < neighbor_node.distance:
#                 node_grid[neighbor_location[0]][neighbor_location[1]] = Node(
#                     distance=new_distance,
#                     source_direction=direction,
#                     source_location=current_location,
#                 )

#         unvisited_locations.remove(current_location)

#         if current_location == (len(weight_grid) - 1, len(weight_grid[0]) - 1):
#             break

#     return node_grid


# def print_node_grid(*, node_grid: NodeGrid) -> None:
#     path: Set[Location] = set()
#     current_location = (len(node_grid) - 1, len(node_grid[0]) - 1)
#     while current_location != (0, 0):
#         path.add(current_location)
#         node = node_grid[current_location[0]][current_location[1]]
#         current_location = node.source_location

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
                source=None,
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


def find_shortest_routes(*, current_location: Optional[Location], input: Input) -> Dict[Location, Node]:
    if current_location is None:
        current_location = input.start_location

    # while end location node has not been visited
    while not input.nodes_by_location[input.end_location].visited and current_location is not None:
        current_node = input.nodes_by_location[current_location]

        # update all neighbors
        neighbor_locations_by_direction = get_all_neighbor_locations(location=current_location)
        for neighbor_direction, neighbor_location in neighbor_locations_by_direction.items():
            neighbor_node = input.nodes_by_location.get(neighbor_location)
            # skip if non-existent
            if neighbor_node is None:
                continue
            # skip if visited
            if neighbor_node.visited:
                continue

            # skip if direction of last two steps are the same direction
            if current_node.source is not None:
                if current_node.source.direction == neighbor_direction:
                    source_node = input.nodes_by_location[current_node.source.location]
                    if source_node.source is not None:
                        if source_node.source.direction == neighbor_direction:
                            continue

            new_distance = current_node.distance_from_start + neighbor_node.weight
            if new_distance == neighbor_node.distance_from_start:
                # TODO: if calculated distance is the same from two directions, gotta calculate both possibilities
                print('gotta split here')
            elif new_distance < neighbor_node.distance_from_start:
                neighbor_node.distance_from_start = new_distance
                neighbor_node.source = Source(
                    direction=neighbor_direction,
                    location=current_location,
                )

        current_node.visited = True
        current_location = find_closest_unvisited_location(nodes_by_location=input.nodes_by_location)

    return input.nodes_by_location


def solution(content: str, /) -> int:
    input = parse_input(content=content)
    nodes_by_location = find_shortest_routes(current_location=None, input=input)

    return nodes_by_location[input.end_location].distance_from_start


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
