from dataclasses import dataclass
import parsy
from typing import Sequence, Tuple

from adventofcode.helpers import executor, parsers

CARD_LETTERS = 'AKQJT98765432'
SCORES_BY_CARD_LETTER = {
    letter: len(CARD_LETTERS) - i
    for i, letter in enumerate(CARD_LETTERS)
}

HAND_TYPES = (
    (5,),             # Five of a kind
    (1, 4),           # Four of a kind
    (2, 3),           # Full house
    (1, 1, 3),        # Three of a kind
    (1, 2, 2),        # Two pair
    (1, 1, 1, 2),     # One pair
    (1, 1, 1, 1, 1),  # High card
)
SCORES_BY_HAND_TYPE = {
    hand_type: len(HAND_TYPES) - i
    for i, hand_type in enumerate(HAND_TYPES)
}

CARD = parsy.regex(rf'[{CARD_LETTERS}]')
HAND = CARD.times(5).concat()

HAND_LINE = parsy.seq(
    HAND.skip(parsers.SPACES),
    parsers.NUMBER
)

CONTENT = (
    HAND_LINE
    .sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINES)
)


@dataclass(frozen=True, kw_only=True)
class Hand:
    bid: int
    cards: str


def parse_hands(*, content: str) -> Sequence[Hand]:
    hands = CONTENT.parse(content)

    return tuple(
        Hand(bid=bid, cards=cards)
        for cards, bid in hands
    )


def determine_hand_type(*, cards: str) -> Tuple:
    counts_by_card = {}
    for card in cards:
        if card not in counts_by_card:
            counts_by_card[card] = 0

        counts_by_card[card] += 1

    return tuple(sorted(counts_by_card.values()))


def calculate_score(*, cards: str) -> int:
    hand_type = determine_hand_type(cards=cards)

    multiplier = 1
    score = 0
    for i in range(len(cards) - 1, -1, -1):
        card = cards[i]
        score += multiplier * SCORES_BY_CARD_LETTER[card]
        multiplier *= 100

    score += multiplier * SCORES_BY_HAND_TYPE[hand_type]
    return score


def calculate_total_winnings(*, hands: Sequence[Hand]) -> int:
    scores_and_hands = list(
        (calculate_score(cards=hand.cards), hand)
        for hand in hands
    )
    scores_and_hands.sort(key=lambda x: x[0])

    return sum(
        hand.bid * (i + 1)
        for i, (_, hand) in enumerate(scores_and_hands)
    )


def solution(content: str, /) -> int:
    hands = parse_hands(content=content)
    return calculate_total_winnings(hands=hands)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
