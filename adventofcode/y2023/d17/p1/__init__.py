from typing import Sequence

from adventofcode.helpers import executor, parsers

ROW = parsers.DIGIT.at_least(1)

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)

Grid = Sequence[Sequence[int]]


def solution(content: str, /) -> int:
    grid = CONTENT.parse(content)
    print(grid)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
