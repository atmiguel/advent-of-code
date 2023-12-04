from dataclasses import dataclass
from typing import Sequence, Tuple, Set

from adventofcode.helpers import executor


Location = Tuple[int, int] # (row_index, column_index)


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

    part_number_locations: Sequence[Location] = []
    part_number_value: int = 0
    for row_index, line in enumerate(lines):
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

                # todo: check if ending number
                match char:
                    case '.':
                        continue
                    case '*' | '#' | '+' | '$':
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


def solution(lines: Sequence[str], /) -> None:
    grid = parse_grid(lines=lines)
    print(grid.symbol_locations)
    print(grid.part_numbers)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
