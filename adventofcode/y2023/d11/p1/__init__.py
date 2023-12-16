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


def find_empty_indices(*, image: Image, galaxy_index: int) -> Set[int]:
    non_empty_indices = set([
        galaxy[galaxy_index]
        for galaxy in image.galaxies
    ])
    max_index = max(non_empty_indices)

    return set([
        index
        for index in range(max_index)
        if index not in non_empty_indices
    ])


def solution(content: str, /) -> int:
    image = parse_image(content=content)

    empty_row_indices = find_empty_indices(image=image, galaxy_index=0)
    empty_column_indices = find_empty_indices(image=image, galaxy_index=1)
    print(empty_row_indices)
    print(empty_column_indices)
    print(image)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
