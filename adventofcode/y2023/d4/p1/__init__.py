from dataclasses import dataclass
import parsy
from typing import Sequence, Set

from adventofcode.helpers import executor, parsers


LINE = (
    parsy.string('Card')
    .then(parsers.SPACES)
    .then(
        parsy.seq(
            parsers.NUMBER
            .skip(parsy.string(':'))
            .skip(parsers.SPACES),
            parsers.NUMBER_LIST
            .skip(parsers.SPACES)
            .skip(parsy.string('|'))
            .skip(parsers.SPACES),
            parsers.NUMBER_LIST
        )
    )
)


@dataclass(frozen=True, kw_only=True)
class ScratchCard:
    scratched_numbers: Sequence[int]
    winning_numbers: Set[int]


def parse_scratch_card(*, line: str) -> ScratchCard:
    _, raw_winning_numbers, scratched_numbers = LINE.parse(line)

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


def solution(content: str, /) -> int:
    return sum(
        calculate_points(
            scratch_card=parse_scratch_card(line=line)
        )
        for line in content.split('\n')
        if len(line) > 0
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
