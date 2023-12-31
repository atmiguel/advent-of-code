from dataclasses import dataclass
import parsy
from typing import Sequence

from adventofcode.helpers import executor, parsers


SEEDS_LINE = parsy.string('seeds: ').then(parsers.NUMBER_LIST)
CATEGORY_MAPS_LINE = parsers.NUMBER.sep_by(parsers.SPACES, min=3, max=3)


def create_maps_parser(name: str) -> parsy.Parser:
    return (
        parsy.string(f'{name} map:')
        .then(parsers.NEWLINE)
        .then(CATEGORY_MAPS_LINE.sep_by(parsers.NEWLINE, min=1))
        .skip(parsers.NEWLINE.many())
    )


FILE = parsy.seq(
    SEEDS_LINE.skip(parsers.NEWLINES),
    create_maps_parser('seed-to-soil'),
    create_maps_parser('soil-to-fertilizer'),
    create_maps_parser('fertilizer-to-water'),
    create_maps_parser('water-to-light'),
    create_maps_parser('light-to-temperature'),
    create_maps_parser('temperature-to-humidity'),
    create_maps_parser('humidity-to-location'),
)


@dataclass(frozen=True, kw_only=True)
class CategoryMap:
    destination_start: int
    length: int
    source_start: int


@dataclass(frozen=True, kw_only=True)
class Almanac:
    seeds: Sequence[int]
    seed_to_soil: Sequence[CategoryMap]
    soil_to_fertilizer: Sequence[CategoryMap]
    fertilizer_to_water: Sequence[CategoryMap]
    water_to_light: Sequence[CategoryMap]
    light_to_temperature: Sequence[CategoryMap]
    temperature_to_humidity: Sequence[CategoryMap]
    humidity_to_location: Sequence[CategoryMap]


def parse_category_map(*, map: Sequence[int]) -> CategoryMap:
    destination_start, source_start, length = map

    return CategoryMap(
        destination_start=destination_start,
        length=length,
        source_start=source_start,
    )


def parse_category_maps(*, maps: Sequence[Sequence[int]]) -> Sequence[CategoryMap]:
    return tuple(
        parse_category_map(map=map)
        for map in maps
    )


def parse_almanac(*, content: str) -> Almanac:
    (
        seeds,
        seed_to_soil_maps,
        soil_to_fertilizer_maps,
        fertizlier_to_water_maps,
        water_to_light_maps,
        light_to_temperature_maps,
        temperature_to_humidity_maps,
        humidity_to_location_maps,
    ) = FILE.parse(content)

    return Almanac(
        seeds=seeds,
        seed_to_soil=parse_category_maps(maps=seed_to_soil_maps),
        soil_to_fertilizer=parse_category_maps(maps=soil_to_fertilizer_maps),
        fertilizer_to_water=parse_category_maps(maps=fertizlier_to_water_maps),
        water_to_light=parse_category_maps(maps=water_to_light_maps),
        light_to_temperature=parse_category_maps(maps=light_to_temperature_maps),
        temperature_to_humidity=parse_category_maps(maps=temperature_to_humidity_maps),
        humidity_to_location=parse_category_maps(maps=humidity_to_location_maps),
    )


def get_destination_value(*, category_maps: Sequence[CategoryMap], source: int) -> int:
    for category_map in category_maps:
        distance = source - category_map.source_start
        if distance >= 0 and distance < category_map.length:
            return category_map.destination_start + distance

    return source


def calculate_seed_location(*, almanac: Almanac, seed: int) -> int:
    soil = get_destination_value(category_maps=almanac.seed_to_soil, source=seed)
    fertilizer = get_destination_value(category_maps=almanac.soil_to_fertilizer, source=soil)
    water = get_destination_value(category_maps=almanac.fertilizer_to_water, source=fertilizer)
    light = get_destination_value(category_maps=almanac.water_to_light, source=water)
    temperature = get_destination_value(category_maps=almanac.light_to_temperature, source=light)
    humidity = get_destination_value(category_maps=almanac.temperature_to_humidity, source=temperature)
    location = get_destination_value(category_maps=almanac.humidity_to_location, source=humidity)

    return location


def solution(content: str, /) -> int:
    almanac = parse_almanac(content=content)

    return min(
        calculate_seed_location(almanac=almanac, seed=seed)
        for seed in almanac.seeds
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
