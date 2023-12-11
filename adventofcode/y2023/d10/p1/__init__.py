from dataclasses import dataclass
import parsy
from typing import Sequence, Tuple, Optional

from adventofcode.helpers import executor, parsers


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
                    raise Exception('unexpected character')

            pipe_row.append(value)

        pipes.append(pipe_row)

    if start is None:
        raise Exception('expected a single start character')

    return Grid(pipes=pipes, start=start)


def solution(content: str, /) -> int:
    grid = parse_grid(content=content)
    print(grid)

    # return sum(
    #     calculate_next_value(history=history)
    #     for history in histories
    # )


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
