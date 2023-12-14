from dataclasses import dataclass
import parsy
from typing import Sequence, Tuple, Optional, Literal, Union

from adventofcode.helpers import executor, parsers

PIPE = parsy.regex(r'[\|\-LJ7F\.S]')

CONTENT = (
    PIPE.at_least(1).concat()
    .sep_by(parsers.NEWLINE)
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
class Pipe:
    directions: Tuple[Direction, Direction]


@dataclass(frozen=True, kw_only=True)
class Grid:
    pipes: Sequence[Sequence[Optional[Pipe]]]
    start: Location


@dataclass(frozen=True, kw_only=True)
class Step:
    direction: Direction
    location: Location


@dataclass(frozen=True, kw_only=True)
class Path:
    steps: Sequence[Step]


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
            raise Exception(f'unexpected direction: {direction}')


def calculate_next_location(*, step: Step) -> Location:
    difference: Tuple[int, int]
    match step.direction:
        case 'up':
            difference = (-1, 0)
        case 'down':
            difference = (1, 0)
        case 'left':
            difference = (0, -1)
        case 'right':
            difference = (0, 1)
        case _:
            raise Exception(f'unexpected direction: {step.direction}')

    return (
        step.location[0] + difference[0],
        step.location[1] + difference[1],
    )


def is_location_in_grid(*, grid: Grid, location: Location) -> bool:
    row_index, column_index = location
    if row_index < 0:
        return False
    if row_index > len(grid.pipes):
        return False

    if column_index < 0:
        return False
    if column_index > len(grid.pipes[0]):
        return False

    return True


def calculate_next_direction(*, pipe: Pipe, previous_direction: Direction) -> Optional[Direction]:
    direction = invert_direction(direction=previous_direction)
    try:
        index = pipe.directions.index(direction)
    except ValueError:
        return None

    return pipe.directions[(index + 1) % 2]


def calculate_next_step(*, grid: Grid, previous_step: Step) -> Optional[Step]:
    next_location = calculate_next_location(step=previous_step)
    if not is_location_in_grid(grid=grid, location=next_location):
        return None

    if next_location == grid.start:
        return Step(
            direction='down',  # doesn't matter because we're back at the start
            location=next_location,
        )

    pipe = grid.pipes[next_location[0]][next_location[1]]
    if pipe is None:
        return None

    next_direction = calculate_next_direction(pipe=pipe, previous_direction=previous_step.direction)
    if next_direction is None:
        return None

    return Step(
        direction=next_direction,
        location=next_location,
    )


def calculate_path(*, direction: Direction, grid: Grid) -> Optional[Path]:
    steps: Sequence[Step] = [Step(direction=direction, location=grid.start)]
    while True:
        next_step = calculate_next_step(grid=grid, previous_step=steps[-1])
        if next_step is None:
            return None
        if next_step.location == grid.start:
            break

        steps.append(next_step)

    return Path(steps=steps)


def find_top_left_step(*, path: Path) -> Step:
    result = path.steps[0]
    for step in path.steps:
        if step.location[0] > result.location[0]:
            pass
        elif step.location[0] < result.location[0]:
            result = step
        else:  # equal row
            if step.location[1] < result.location[1]:
                result = step

    return result


def solution(content: str, /) -> int:
    grid = parse_grid(content=content)

    for direction in ('up', 'down', 'left', 'right'):
        path = calculate_path(
            direction=direction,
            grid=grid,
        )

        if path is None:
            continue

        top_left_step = find_top_left_step(path=path)
        if top_left_step.direction != 'right':
            continue

        print(top_left_step)
        # TODO: also get step index
        # then follow steps
        # always looking "right" and recording all the locations up till hitting a path cell
        # by using sets


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
