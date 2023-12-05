from dataclasses import dataclass
import parsy
from typing import Sequence, Set

from adventofcode.helpers import executor


NUMBER = parsy.decimal_digit.at_least(1).concat().map(int)
NUMBER_LIST = NUMBER.skip(parsy.whitespace.many()).at_least(1)

COLON = parsy.string(':')
PIPE = parsy.string('|')
CARD = parsy.string('Card')

LINE = (
    CARD
    .then(parsy.whitespace)
    .then(NUMBER)
    .then(COLON)
    .then(parsy.whitespace)
    .then(
        parsy.seq(
            NUMBER_LIST
            .skip(PIPE)
            .skip(parsy.whitespace),
            NUMBER_LIST
        )
    )
)


@dataclass(frozen=True, kw_only=True)
class ScratchCard:
    scratched_numbers: Sequence[int]
    winning_numbers: Set[int]


def parse_scratch_card(*, line: str) -> ScratchCard:
    raw_winning_numbers, scratched_numbers = LINE.parse(line)

    winning_numbers = set(raw_winning_numbers)
    assert len(raw_winning_numbers) == len(winning_numbers)

    return ScratchCard(
        scratched_numbers=scratched_numbers,
        winning_numbers=winning_numbers
    )


def calculate_points(*, scratch_card: ScratchCard) -> int:
    count = sum(
        1
        for number in scratch_card.scratched_numbers
        if number in scratch_card.winning_numbers
    )

    return 0 if count == 0 else 2 ** (count - 1)


def solution(lines: Sequence[str], /) -> None:
    return sum(
        calculate_points(
            scratch_card=parse_scratch_card(line=line)
        )
        for line in lines
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
