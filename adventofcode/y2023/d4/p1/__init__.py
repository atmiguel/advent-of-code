import parsy
from typing import Sequence

from adventofcode.helpers import executor


MULTIPLE_DIGITS = parsy.decimal_digit.at_least(1).concat().map(int)
NUMBER_LIST = parsy.whitespace.then(
    MULTIPLE_DIGITS.skip(parsy.whitespace).at_least(1)
)

COLON = parsy.string(':')
PIPE = parsy.string('|')
CARD = parsy.string('Card')

LINE = CARD.then(parsy.whitespace).then(
    parsy.seq(
        MULTIPLE_DIGITS.skip(COLON),
        NUMBER_LIST.skip(PIPE),
        NUMBER_LIST
    )
)


def solution(lines: Sequence[str], /) -> None:
    id_, magic_numbers, actual_numbers = LINE.parse('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53')
    print(id_)
    print(magic_numbers)
    print(actual_numbers)
    # grid = parse_grid(lines=lines)

    # return sum(
    #     part_number.value
    #     for part_number in grid.part_numbers
    #     if is_part_number_near_a_symbol(
    #         part_number=part_number,
    #         symbol_locations=grid.symbol_locations,
    #     )
    # )


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
