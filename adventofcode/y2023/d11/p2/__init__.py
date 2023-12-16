from dataclasses import dataclass
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


def insert_space_between_galaxies(*, image: Image, space: int) -> Image:
    empty_row_indices = find_empty_indices(image=image, galaxy_index=0)
    empty_column_indices = find_empty_indices(image=image, galaxy_index=1)

    new_galaxies: Set[Location] = set()
    for galaxy in image.galaxies:
        row_index, column_index = galaxy

        row_index_diff = sum(
            space - 1
            for index in empty_row_indices
            if row_index > index
        )
        column_index_diff = sum(
            space - 1
            for index in empty_column_indices
            if column_index > index
        )

        new_galaxies.add((
            row_index + row_index_diff,
            column_index + column_index_diff,
        ))

    return Image(galaxies=new_galaxies)


def calculate_distance_between_galaxies(*, image: Image) -> int:
    return sum(
        abs(galaxy_a[0] - galaxy_b[0]) + abs(galaxy_a[1] - galaxy_b[1])
        for galaxy_a in image.galaxies
        for galaxy_b in image.galaxies
    ) // 2


def solution(content: str, /) -> int:
    image = parse_image(content=content)
    spaced_image = insert_space_between_galaxies(image=image, space=1_000_000)

    return calculate_distance_between_galaxies(image=spaced_image)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
