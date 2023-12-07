from dataclasses import dataclass
import functools
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


def calculate_win_count(*, race: Race) -> int:
    half_time = race.time // 2
    for index in range(half_time):
        speed = index + 1
        remaining_time = race.time - speed

        if remaining_time * speed > race.distance:
            result = (half_time - index) * 2
            if race.time % 2 == 0:
                result -= 1

            return result

    raise Exception('expected to find result')


def solution(content: str, /) -> int:
    races = parse_races(content=content)
    win_counts = tuple(
        calculate_win_count(race=race)
        for race in races
    )

    return functools.reduce(lambda x, y: x * y, win_counts)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
