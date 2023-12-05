from dataclasses import dataclass
from typing import Sequence, Tuple, Set

from adventofcode.helpers import executor


Location = Tuple[int, int] # (row_index, column_index)


@dataclass(frozen=True, kw_only=True)
class PartNumber:
    locations: Set[Location]
    value: int


@dataclass(frozen=True, kw_only=True)
class Grid:
    gear_locations: Set[Location]
    part_numbers: Sequence[PartNumber]


def parse_grid(*, lines: Sequence[str]) -> Grid:
    gear_locations: Set[Location] = set()
    part_numbers: Sequence[PartNumber] = []

    for row_index, line in enumerate(lines):
        part_number_locations: Set[Location] = set()
        part_number_value: int = 0

        for column_index, char in enumerate(line):
            if char.isdigit():
                part_number_locations.add((row_index, column_index))
                if part_number_value == 0:
                    part_number_value = int(char)
                else:
                    part_number_value = (10 * part_number_value) + int(char)
            else:
                if part_number_value > 0:
                    part_numbers.append(
                        PartNumber(
                            locations=part_number_locations,
                            value=part_number_value
                        )
                    )
                    part_number_locations = set()
                    part_number_value = 0

                match char:
                    case '.' | '#' | '+' | '$' | '%' | '=' | '-' | '/' | '@' | '&':
                        continue
                    case '*':
                        gear_locations.add((row_index, column_index))
                    case _:
                        raise Exception(f'unexpected character: {char}')

        if part_number_value > 0:
            part_numbers.append(
                PartNumber(
                    locations=part_number_locations,
                    value=part_number_value
                )
            )
    
    return Grid(
        part_numbers=part_numbers,
        gear_locations=gear_locations,
    )


def get_adjacent_locations(*, location: Location) -> Set[Location]:
    adjacent_locations: Set[Location] = set()
    for row_adjustment in (-1, 0, 1):
        for column_adjustment in (-1, 0, 1):
            if row_adjustment == 0 and column_adjustment == 0:
                continue

            adjacent_locations.add(
                (location[0] + row_adjustment, location[1] + column_adjustment)
            )
    
    return adjacent_locations


def is_location_near_part_number(*, location: Location, part_number: PartNumber) -> bool:
    return any(
        adjacent_location in part_number.locations
        for adjacent_location in get_adjacent_locations(location=location)
    )


def get_adjacent_part_numbers(*, location: Location, part_numbers: Sequence[PartNumber]) -> Sequence[PartNumber]:
    return tuple(
        part_number
        for part_number in part_numbers
        if is_location_near_part_number(location=location, part_number=part_number)
    )


def calculate_gear_ratio(*, gear_location: Location, part_numbers: Sequence[PartNumber]) -> int:
    adjacent_part_numbers = get_adjacent_part_numbers(location=gear_location, part_numbers=part_numbers)
    if len(adjacent_part_numbers) != 2:
        return 0
    
    return adjacent_part_numbers[0].value * adjacent_part_numbers[1].value


def solution(lines: Sequence[str], /) -> int:
    grid = parse_grid(lines=lines)

    return sum(
        calculate_gear_ratio(gear_location=gear_location, part_numbers=grid.part_numbers)
        for gear_location in grid.gear_locations
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
