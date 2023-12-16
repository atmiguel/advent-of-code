from dataclasses import dataclass
import math
import parsy
from typing import Sequence, Tuple, Optional

from adventofcode.helpers import executor, parsers

import sys
print(sys.setrecursionlimit(16_000))

PIPE = parsy.regex(r'[\|\-LJ7F\.S]')

CONTENT = (
    PIPE.at_least(1).concat()
    .sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)


@dataclass(frozen=True, kw_only=True)
class Pipe:
    directions: Tuple[str, str]


@dataclass(frozen=True, kw_only=True)
class Grid:
    pipes: Sequence[Sequence[Optional[Pipe]]]
    start: Tuple[int, int]


def parse_grid(*, content: str) -> Grid:
    grid = CONTENT.parse(content)

    pipes = []
    start = None
    for row_index, line in enumerate(grid):
        pipe_row = []

        for column_index, pipe in enumerate(line):
            value: Optional[Pipe]
            match pipe:
                case '|':
                    value = Pipe(directions=('up', 'down'))
                case '-':
                    value = Pipe(directions=('left', 'right'))
                case 'L':
                    value = Pipe(directions=('up', 'right'))
                case 'J':
                    value = Pipe(directions=('up', 'left'))
                case '7':
                    value = Pipe(directions=('down', 'left'))
                case 'F':
                    value = Pipe(directions=('down', 'right'))
                case '.':
                    value = None
                case 'S':
                    value = None
                    if start is not None:
                        raise Exception('expected a single start character')

                    start = (row_index, column_index)
                case _:
                    raise Exception(f'unexpected character: {pipe}')

            pipe_row.append(value)

        pipes.append(pipe_row)

    if start is None:
        raise Exception('expected a single start character')

    return Grid(pipes=pipes, start=start)


def get_next_location(*, grid: Grid, location: Tuple[int, int], direction: str) -> Optional[Tuple[int, int]]:
    current_row_index, current_column_index = location
    match direction:
        case 'up':
            next_location = (current_row_index - 1, current_column_index)
        case 'down':
            next_location = (current_row_index + 1, current_column_index)
        case 'left':
            next_location = (current_row_index, current_column_index - 1)
        case 'right':
            next_location = (current_row_index, current_column_index + 1)
        case _:
            raise Exception(f'unexpected direction: {direction}')

    next_row_index, next_column_index = next_location
    if next_row_index < 0:
        return None
    if next_row_index > len(grid.pipes):
        return None

    if next_column_index < 0:
        return None
    if next_column_index > len(grid.pipes[0]):
        return None

    return next_location


def find_distance_to_start(*, current_location: Tuple[int, int], grid: Grid, last_direction: str) -> Optional[int]:
    if current_location == grid.start:
        return 0

    current_row_index, current_column_index = current_location
    pipe = grid.pipes[current_row_index][current_column_index]

    if pipe is None:
        return None

    match last_direction:
        case 'up':
            expected_direction = 'down'
        case 'down':
            expected_direction = 'up'
        case 'left':
            expected_direction = 'right'
        case 'right':
            expected_direction = 'left'
        case _:
            raise Exception(f'unexpected direction: {last_direction}')

    try:
        index = pipe.directions.index(expected_direction)
    except ValueError:
        return None

    next_direction = pipe.directions[(index + 1) % 2]
    next_location = get_next_location(
        grid=grid,
        location=current_location,
        direction=next_direction,
    )

    distance_to_start = find_distance_to_start(
        current_location=next_location,
        grid=grid,
        last_direction=next_direction,
    )
    if distance_to_start is None:
        return None

    return distance_to_start + 1


def solution(content: str, /) -> int:
    grid = parse_grid(content=content)

    for direction in ['up', 'down', 'left', 'right']:
        location = get_next_location(
            grid=grid,
            location=grid.start,
            direction=direction,
        )

        if location is None:
            continue

        distance_to_start = find_distance_to_start(
            current_location=location,
            grid=grid,
            last_direction=direction,
        )

        if distance_to_start is not None:
            return math.ceil(distance_to_start / 2)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
