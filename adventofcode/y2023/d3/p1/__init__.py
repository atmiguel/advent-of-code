from dataclasses import dataclass
from typing import Sequence, Tuple, Set

from adventofcode.helpers import executor


Location = Tuple[int, int]  # (row_index, column_index)


@dataclass(frozen=True, kw_only=True)
class PartNumber:
    locations: Sequence[Location]
    value: int


@dataclass(frozen=True, kw_only=True)
class Grid:
    symbol_locations: Set[Location]
    part_numbers: Sequence[PartNumber]


def parse_grid(*, lines: Sequence[str]) -> Grid:
    symbol_locations: Set[Location] = set()
    part_numbers: Sequence[PartNumber] = []

    for row_index, line in enumerate(lines):
        part_number_locations: Sequence[Location] = []
        part_number_value: int = 0

        for column_index, char in enumerate(line):
            if char.isdigit():
                part_number_locations.append((row_index, column_index))
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
                    part_number_locations = []
                    part_number_value = 0

                match char:
                    case '.':
                        continue
                    case '*' | '#' | '+' | '$' | '%' | '=' | '-' | '/' | '@' | '&':
                        symbol_locations.add((row_index, column_index))
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
        symbol_locations=symbol_locations,
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


def is_location_near_a_symbol(*, location: Location, symbol_locations: Set[Location]) -> bool:
    return any(
        adjacent_location in symbol_locations
        for adjacent_location in get_adjacent_locations(location=location)
    )


def is_part_number_near_a_symbol(*, part_number: PartNumber, symbol_locations: Set[Location]) -> bool:
    return any(
        is_location_near_a_symbol(location=location, symbol_locations=symbol_locations)
        for location in part_number.locations
    )


def solution(content: str, /) -> int:
    grid = parse_grid(lines=content.split('\n'))

    return sum(
        part_number.value
        for part_number in grid.part_numbers
        if is_part_number_near_a_symbol(
            part_number=part_number,
            symbol_locations=grid.symbol_locations,
        )
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
