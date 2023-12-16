from dataclasses import dataclass
import parsy
from typing import Sequence, Tuple, Optional, Literal, Union, Set

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


def find_top_left_step(*, path: Path) -> Tuple[int, Step]:
    result_index = 0
    result = path.steps[result_index]
    for index, step in enumerate(path.steps):
        if step.location[0] > result.location[0]:
            pass
        elif step.location[0] < result.location[0]:
            result_index = index
            result = step
        else:  # equal row
            if step.location[1] < result.location[1]:
                result_index = index
                result = step

    return result_index, result


def check_right(
    *,
    direction: Direction,
    grid: Grid,
    location: Location,
    path_locations: Set[Location],
) -> Set[Location]:
    match direction:
        case 'up':
            check_direction = 'right'
        case 'down':
            check_direction = 'left'
        case 'left':
            check_direction = 'up'
        case 'right':
            check_direction = 'down'
        case _:
            raise Exception(f'unexpected direction {direction}')

    inner_locations: Set[Location] = set()
    next_location = location
    while True:
        next_location = calculate_next_location(
            step=Step(
                direction=check_direction,
                location=next_location,
            )
        )
        if not is_location_in_grid(grid=grid, location=next_location):
            break
        if next_location in path_locations:
            break

        inner_locations.add(next_location)

    return inner_locations


def follow_steps(*, grid: Grid, path: Path, top_left_step_index: int) -> Set[Location]:
    path_locations = set([
        step.location
        for step in path.steps
    ])
    indexes = [i for i in range(top_left_step_index, len(path.steps))] + \
        [i for i in range(top_left_step_index)]

    inner_locations: Set[Location] = set()
    last_direction = 'up'
    for index in indexes:
        step = path.steps[index]
        inner_locations.update(
            check_right(
                direction=last_direction,
                grid=grid,
                location=step.location,
                path_locations=path_locations,
            )
        )
        last_direction = step.direction

    return inner_locations


def solution(content: str, /) -> int:
    grid = parse_grid(content=content)

    for direction in ('up', 'down', 'left', 'right'):
        path = calculate_path(
            direction=direction,
            grid=grid,
        )

        if path is None:
            continue

        top_left_step_index, top_left_step = find_top_left_step(path=path)
        if top_left_step.direction != 'right':
            continue

        inner_locations = follow_steps(grid=grid, path=path, top_left_step_index=top_left_step_index)
        return len(inner_locations)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
