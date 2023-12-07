from dataclasses import dataclass
import parsy

from adventofcode.helpers import executor, parsers


CONCATENATED_NUMBER_LIST = (
    parsy.regex(r'\d+')
    .sep_by(parsers.SPACES)
    .concat()
    .map(int)
)

TIMES_LINE = (
    parsy.string('Time:')
    .then(parsers.SPACES)
    .then(CONCATENATED_NUMBER_LIST)
)
DISTANCES_LINE = (
    parsy.string('Distance:')
    .then(parsers.SPACES)
    .then(CONCATENATED_NUMBER_LIST)
)

CONTENT = parsy.seq(
    TIMES_LINE.skip(parsers.NEWLINE),
    DISTANCES_LINE.skip(parsers.NEWLINE.many())
)


@dataclass(frozen=True, kw_only=True)
class Race:
    distance: int
    time: int


def parse_race(*, content: str) -> Race:
    time, distance = CONTENT.parse(content)
    return Race(distance=distance, time=time)


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
    race = parse_race(content=content)
    return calculate_win_count(race=race)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
