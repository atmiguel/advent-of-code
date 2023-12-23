import parsy
from typing import Sequence, Literal, Union, Tuple, Set

from adventofcode.helpers import executor, parsers
import sys
sys.setrecursionlimit(8_000)

CELL = parsy.regex(r'[\.\|\-\\\/]')
ROW = CELL.at_least(1).concat()

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
Step = Tuple[Location, Direction]
Grid = Sequence[str]


def walk_path(*, grid: Grid, step: Step, visited_steps: Set[Step]) -> None:
    if step in visited_steps:
        return

    visited_steps.add(step)
    location, direction = step
    cell = grid[location[0]][location[1]]

    next_directions: Sequence[Direction]
    match cell:
        case '.':
            next_directions = [direction]
        case '|':
            match direction:
                case 'up' | 'down':
                    next_directions = [direction]
                case 'left' | 'right':
                    next_directions = ['up', 'down']
                case _:
                    raise Exception('unexpected direction')
        case '-':
            match direction:
                case 'up' | 'down':
                    next_directions = ['left', 'right']
                case 'left' | 'right':
                    next_directions = [direction]
                case _:
                    raise Exception('unexpected direction')
        case '/':
            match direction:
                case 'up':
                    next_directions = ['right']
                case 'down':
                    next_directions = ['left']
                case 'left':
                    next_directions = ['down']
                case 'right':
                    next_directions = ['up']
                case _:
                    raise Exception('unexpected direction')
        case '\\':
            match direction:
                case 'up':
                    next_directions = ['left']
                case 'down':
                    next_directions = ['right']
                case 'left':
                    next_directions = ['up']
                case 'right':
                    next_directions = ['down']
                case _:
                    raise Exception('unexpected direction')
        case _:
            raise Exception('unexpected cell')

    for next_direction in next_directions:
        next_location: Location
        match next_direction:
            case 'up':
                next_location = (location[0] - 1, location[1])
            case 'down':
                next_location = (location[0] + 1, location[1])
            case 'left':
                next_location = (location[0], location[1] - 1)
            case 'right':
                next_location = (location[0], location[1] + 1)
            case _:
                raise Exception('unexpected direction')

        if next_location[0] < 0 or next_location[0] >= len(grid):
            continue
        if next_location[1] < 0 or next_location[1] >= len(grid[0]):
            continue

        walk_path(
            grid=grid,
            step=(next_location, next_direction),
            visited_steps=visited_steps,
        )


def calculate_energized_tiles(*, grid: Grid, initial_step: Step) -> int:
    visited_steps: Set[Step] = set()
    walk_path(
        grid=grid,
        step=initial_step,
        visited_steps=visited_steps,
    )

    visited_locations = set(
        step[0]
        for step in visited_steps
    )

    return len(visited_locations)


def solution(content: str, /) -> int:
    grid = CONTENT.parse(content)

    values: Sequence[int] = []
    for row_index, row in enumerate(grid):
        for column_index in range(len(row)):
            location = (row_index, column_index)
            directions: Sequence[Direction] = []
            if row_index == 0:
                directions.append('down')
            elif row_index == len(grid) - 1:
                directions.append('up')

            if column_index == 0:
                directions.append('right')
            elif column_index == len(row) - 1:
                directions.append('left')

            for direction in directions:
                values.append(
                    calculate_energized_tiles(
                        grid=grid,
                        initial_step=(location, direction),
                    )
                )

    return max(values)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
