from dataclasses import dataclass
import math
import parsy
from typing import Tuple, Set

from adventofcode.helpers import executor, parsers

CELL = parsy.regex(r'[\.#]')
ROW = CELL.at_least(1)

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)

Location = Tuple[int, int]


@dataclass(frozen=True, kw_only=True)
class Image:
    galaxies: set[Location]


def parse_image(*, content: str) -> Image:
    rows = CONTENT.parse(content)

    galaxies: Set[Location] = set()
    for row_index, row in enumerate(rows):
        for column_index, cell in enumerate(row):
            match cell:
                case '.':
                    continue
                case '#':
                    galaxies.add((row_index, column_index))
                case _:
                    raise Exception(f'unexpected character: {cell}')

    return Image(galaxies=galaxies)


def solution(content: str, /) -> int:
    image = parse_image(content=content)
    print(image)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
