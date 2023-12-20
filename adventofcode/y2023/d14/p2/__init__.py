import parsy
from typing import Sequence

from adventofcode.helpers import executor, parsers

ROCK = parsy.regex(r'[\.#O]')
ROW = ROCK.at_least(1)

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)

Grid = Sequence[Sequence[str]]


def find_left(values: Sequence[str], /, *, char: str, start: int, stop: int) -> int:
    try:
        return values.index(char, start, stop)
    except ValueError:
        return -1


def find_right(values: Sequence[str], /, *, char: str, start: int, stop: int) -> int:
    for index in range(stop - 1, start - 1, -1):
        if values[index] == char:
            return index

    return -1


def roll_rocks_west(*, grid: Grid) -> None:
    for row in grid:
        solid_rocks = [index for index, char in enumerate(row) if char == '#'] + [len(row)]

        for index, solid_rock in enumerate(solid_rocks):
            start_index = 0 if index == 0 else solid_rocks[index - 1]
            stop_index = solid_rock

            while True:
                leftmost_empty = find_left(row, char='.', start=start_index, stop=stop_index)
                rightmost_rock = find_right(row, char='O', start=start_index, stop=stop_index)

                if leftmost_empty == -1 or rightmost_rock == -1:
                    break

                if leftmost_empty > rightmost_rock:
                    break

                row[leftmost_empty], row[rightmost_rock] = row[rightmost_rock], row[leftmost_empty]


def roll_rocks_east(*, grid: Grid) -> None:
    for row in grid:
        solid_rocks = [index for index, char in enumerate(row) if char == '#'] + [len(row)]

        for index, solid_rock in enumerate(solid_rocks):
            start_index = 0 if index == 0 else solid_rocks[index - 1]
            stop_index = solid_rock

            while True:
                rightmost_empty = find_right(row, char='.', start=start_index, stop=stop_index)
                leftmost_rock = find_left(row, char='O', start=start_index, stop=stop_index)

                if rightmost_empty == -1 or leftmost_rock == -1:
                    break

                if rightmost_empty < leftmost_rock:
                    break

                row[rightmost_empty], row[leftmost_rock] = row[leftmost_rock], row[rightmost_empty]


def roll_rocks_north(*, grid: Grid) -> None:
    for column_index in range(len(grid[0])):
        column = [grid[i][column_index] for i in range(len(grid))]
        solid_rocks = [index for index, char in enumerate(column) if char == '#'] + [len(column)]

        for solid_rock_index, solid_rock in enumerate(solid_rocks):
            start_index = 0 if solid_rock_index == 0 else solid_rocks[solid_rock_index - 1]
            stop_index = solid_rock

            while True:
                topmost_empty = find_left(column, char='.', start=start_index, stop=stop_index)
                bottommost_rock = find_right(column, char='O', start=start_index, stop=stop_index)

                if topmost_empty == -1 or bottommost_rock == -1:
                    break

                if topmost_empty > bottommost_rock:
                    break

                column[topmost_empty], column[bottommost_rock] = column[bottommost_rock], column[topmost_empty]

        for i, cell in enumerate(column):
            grid[i][column_index] = cell


def roll_rocks_south(*, grid: Grid) -> None:
    for column_index in range(len(grid[0])):
        column = [grid[i][column_index] for i in range(len(grid))]
        solid_rocks = [index for index, char in enumerate(column) if char == '#'] + [len(column)]

        for solid_rock_index, solid_rock in enumerate(solid_rocks):
            start_index = 0 if solid_rock_index == 0 else solid_rocks[solid_rock_index - 1]
            stop_index = solid_rock

            while True:
                bottommost_empty = find_right(column, char='.', start=start_index, stop=stop_index)
                topmost_rock = find_left(column, char='O', start=start_index, stop=stop_index)

                if bottommost_empty == -1 or topmost_rock == -1:
                    break

                if bottommost_empty < topmost_rock:
                    break

                column[bottommost_empty], column[topmost_rock] = column[topmost_rock], column[bottommost_empty]

        for i, cell in enumerate(column):
            grid[i][column_index] = cell


def cycle_rocks(*, grid: Grid) -> None:
    roll_rocks_north(grid=grid)
    roll_rocks_west(grid=grid)
    roll_rocks_south(grid=grid)
    roll_rocks_east(grid=grid)


def count_rocks(*, grid: Grid) -> int:
    return sum(
        row.count('O') * (len(grid) - index)
        for index, row in enumerate(grid)
    )


def print_grid(grid: Grid, /) -> None:
    for row in grid:
        print(''.join(row))
    print()


def determine_pattern_length(*, values: Sequence[int]) -> int:
    for pattern_length in range(1, 1_000):
        for i in range(pattern_length, len(values), pattern_length):
            if values[i] != values[i - pattern_length]:
                break
        else:
            return pattern_length

    raise Exception('failed to find pattern length')


def solution(content: str, /) -> int:
    grid = CONTENT.parse(content)

    for _ in range(1_000):
        cycle_rocks(grid=grid)

    weights = []
    for _ in range(1_000):
        cycle_rocks(grid=grid)
        weights.append(count_rocks(grid=grid))

    pattern_length = determine_pattern_length(values=weights)
    weight_index = (1_000_000_000 - 1_000 - 1) % pattern_length

    return weights[weight_index]


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
