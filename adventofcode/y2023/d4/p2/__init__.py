from dataclasses import dataclass
from typing import Sequence, Set, Dict
import parsy

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
    id_: int
    scratched_numbers: Sequence[int]
    winning_numbers: Set[int]


def parse_scratch_card(*, line: str) -> ScratchCard:
    id_, raw_winning_numbers, scratched_numbers = LINE.parse(line)

    winning_numbers = set(raw_winning_numbers)
    assert len(raw_winning_numbers) == len(winning_numbers)

    return ScratchCard(
        id_=id_,
        scratched_numbers=scratched_numbers,
        winning_numbers=winning_numbers
    )


def count_winning_numbers(*, scratch_card: ScratchCard) -> int:
    return sum(
        1
        for number in scratch_card.scratched_numbers
        if number in scratch_card.winning_numbers
    )


def calculate_points(*, scratch_cards: Sequence[ScratchCard]) -> int:
    copies_by_id: Dict[int, int] = {
        scratch_card.id_: 1
        for scratch_card in scratch_cards
    }

    for scratch_card in scratch_cards:
        count = count_winning_numbers(scratch_card=scratch_card)
        copy_count = copies_by_id[scratch_card.id_]

        for i in range(count):
            card_id = scratch_card.id_ + i + 1
            if card_id not in copies_by_id:
                continue

            copies_by_id[card_id] += copy_count

    return sum(copies_by_id.values())


def solution(content: str, /) -> int:
    scratch_cards = tuple(
        parse_scratch_card(line=line)
        for line in content.split('\n')
        if len(line) > 0
    )

    return calculate_points(scratch_cards=scratch_cards)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
