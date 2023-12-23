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
DirectedDistance = Tuple[Optional[Direction], int]
Grid = Sequence[Sequence[int]]
DistanceGrid = Sequence[Sequence[DirectedDistance]]


def find_closest_unvisited_location(
        *,
        distance_grid: DistanceGrid,
        unvisited_locations: Set[Location],
) -> Location:
    min_distance: int = math.inf
    min_location: Optional[Location] = None
    for location in unvisited_locations:
        _, distance = distance_grid[location[0]][location[1]]
        if distance < min_distance:
            min_distance = distance
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


def is_location_in_grid(*, location: Location, grid: Grid) -> bool:
    if location[0] < 0:
        return False
    if location[0] >= len(grid):
        return False
    if location[1] < 0:
        return False
    if location[1] >= len(grid[0]):
        return False
    return True


def calculate_distance_grid(*, grid: Grid) -> DistanceGrid:
    distance_grid: DistanceGrid = []
    for row_index, row in enumerate(grid):
        distance_row = []
        for column_index in range(len(row)):
            distance_row.append(
                (
                    None,
                    0 if row_index == 0 and column_index == 0 else math.inf,
                )
            )

        distance_grid.append(distance_row)

    unvisited_locations = set([
        (row_index, column_index)
        for row_index, row in enumerate(grid)
        for column_index in range(len(row))
    ])

    while len(unvisited_locations) > 0:
        current_location = find_closest_unvisited_location(
            distance_grid=distance_grid,
            unvisited_locations=unvisited_locations,
        )
        _, current_distance = distance_grid[current_location[0]][current_location[1]]
        cell_weight = grid[current_location[0]][current_location[1]]

        for direction in ('up', 'down', 'left', 'right'):
            neighbor_location = get_next_location(
                location=current_location,
                direction=direction,
            )
            if not is_location_in_grid(location=neighbor_location, grid=grid):
                continue

            if neighbor_location not in unvisited_locations:
                continue

            inverted_direction = invert_direction(direction=direction)
            check_location = current_location
            for _ in range(3):
                check_location = get_next_location(
                    location=check_location,
                    direction=inverted_direction,
                )
                if not is_location_in_grid(location=check_location, grid=grid):
                    break

                check_direction, _ = distance_grid[check_location[0]][check_location[1]]
                if check_direction != direction:
                    break
            else:
                # all 3 check directions were in a row
                continue

            _, neighbor_distance = distance_grid[neighbor_location[0]][neighbor_location[1]]
            new_distance = current_distance + cell_weight
            if new_distance < neighbor_distance:
                distance_grid[neighbor_location[0]][neighbor_location[1]] = (direction, new_distance)

        unvisited_locations.remove(current_location)

    return distance_grid


def solution(content: str, /) -> int:
    grid = CONTENT.parse(content)
    distance_grid = calculate_distance_grid(grid=grid)
    print(distance_grid)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
