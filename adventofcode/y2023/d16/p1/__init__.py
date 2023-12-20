import parsy
from typing import Sequence, Literal, Union, Tuple, Set

from adventofcode.helpers import executor, parsers

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

    match direction:
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
        return
    if next_location[1] < 0 or next_location[1] >= len(grid[0]):
        return

    match cell:
        case '.':
            walk_path(
                grid=grid,
                step=Step((next_location, direction)),
                visited_steps=visited_steps,
            )
        case '|':
            pass
        case '-':
            pass
        case '/':
            pass
        case '\\':
            pass
        case _:
            raise Exception('unexpected cell')
    pass


def solution(content: str, /) -> int:
    grid = CONTENT.parse(content)

    visited_steps: Set[Step] = set()
    print(grid)

    # return sum(
    #     calculate_hash(step)
    #     for step in sequence
    # )


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
