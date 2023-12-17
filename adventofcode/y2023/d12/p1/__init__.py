from dataclasses import dataclass
import parsy
from typing import Sequence

from adventofcode.helpers import executor, parsers

SPRING = parsy.regex(r'[\?\.#]')
ROW = parsy.seq(
    SPRING.at_least(1).concat()
    .skip(parsers.SPACE),
    parsers.NUMBER.sep_by(parsy.string(','))
)

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)


@dataclass(frozen=True, kw_only=True)
class SpringRow:
    damaged_groups: Sequence[int]
    springs: str


def parse_spring_rows(*, content: str) -> Sequence[SpringRow]:
    rows = CONTENT.parse(content)

    return [
        SpringRow(damaged_groups=damaged_groups, springs=springs)
        for springs, damaged_groups in rows
    ]


def solution(content: str, /) -> int:
    spring_rows = parse_spring_rows(content=content)
    # image = parse_image(content=content)
    # spaced_image = insert_space_between_galaxies(image=image)

    # return calculate_distance_between_galaxies(image=spaced_image)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
