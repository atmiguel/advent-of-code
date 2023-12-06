import parsy
from typing import Sequence

from adventofcode.helpers import executor


NEWLINE = parsy.string('\n')
NEWLINES = parsy.regex(r'\n+')
MAYBE_NEWLINES = parsy.regex(r'\n*')

SPACE = parsy.string(' ')
SPACES = parsy.regex(r' +')

NUMBER = parsy.decimal_digit.at_least(1).concat().map(int)
NUMBER_LIST = NUMBER.sep_by(SPACES)

SEEDS_LINE = parsy.string('seeds: ').then(NUMBER_LIST)
MAPS_LINE = NUMBER.sep_by(SPACES, min=3, max=3)


def create_maps_parser(name: str) -> parsy.Parser:
    return (
        parsy.string(f'{name} map:')
        .then(NEWLINE)
        .then(MAPS_LINE.sep_by(NEWLINE, min=1))
        .skip(MAYBE_NEWLINES)
    )


FILE = parsy.seq(
    SEEDS_LINE.skip(NEWLINES),
    create_maps_parser('seed-to-soil'),
    create_maps_parser('soil-to-fertilizer'),
    create_maps_parser('fertilizer-to-water'),
    create_maps_parser('water-to-light'),
    create_maps_parser('light-to-temperature'),
    create_maps_parser('temperature-to-humidity'),
    create_maps_parser('humidity-to-location'),
)


def parse_lines(*, lines: Sequence[str]) -> None:
    # TODO(adrian@gradient.ai, 12/05/2023): consider getting full file instead of lines
    file_content = '\n'.join(lines)

    (
        seeds,
        seed_to_soil_maps,
        soil_to_fertilizer_maps,
        fertizlier_to_water_maps,
        water_to_light_maps,
        light_to_temperature_maps,
        temperature_to_humidity_maps,
        humidity_to_location_maps,
    ) = FILE.parse(file_content)
    print(seeds)
    print(seed_to_soil_maps)
    pass


def solution(lines: Sequence[str], /) -> int:
    parse_lines(lines=lines)
    # return sum(
    #     calculate_points(
    #         scratch_card=parse_scratch_card(line=line)
    #     )
    #     for line in lines
    # )


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
