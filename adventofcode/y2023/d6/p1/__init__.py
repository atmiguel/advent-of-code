from dataclasses import dataclass
import parsy
from typing import Sequence

from adventofcode.helpers import executor, parsers


TIMES_LINE = (
    parsy.string('Time:')
    .then(parsers.SPACES)
    .then(parsers.NUMBER_LIST)
)
DISTANCES_LINE = (
    parsy.string('Distance:')
    .then(parsers.SPACES)
    .then(parsers.NUMBER_LIST)
)

CONTENT = parsy.seq(
    TIMES_LINE.skip(parsers.NEWLINE),
    DISTANCES_LINE.skip(parsers.NEWLINE.many())
)


@dataclass(frozen=True, kw_only=True)
class Race:
    distance: int
    time: int


def parse_races(*, content: str) -> Sequence[Race]:
    times, distances = CONTENT.parse(content)
    assert len(times) == len(distances)

    return tuple(
        Race(distance=distance, time=time)
        for time, distance in zip(times, distances)
    )


def solution(content: str, /) -> int:
    races = parse_races(content=content)
    print(races)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
