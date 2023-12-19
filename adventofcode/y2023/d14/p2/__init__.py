import parsy
from typing import Sequence, Tuple

from adventofcode.helpers import executor, parsers

ROCK = parsy.regex(r'[\.#O]')
ROW = ROCK.at_least(1)

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)

Location = Tuple[int, int]
Grid = Sequence[Sequence[str]]


# def roll_rock_north(*, rows: Sequence[Sequence[str]], rock_location: Location) -> Sequence[Sequence[str]]:
#     north_rock_row_location = (rock_location[0] - 1, rock_location[1])
#     if north_rock_row_location[0] < 0:
#         return rows

#     north_rock = rows[north_rock_row_location[0]][north_rock_row_location[1]]
#     match north_rock:
#         case '.':
#             new_rows = copy.deepcopy(rows)
#             new_rows[rock_location[0]][rock_location[1]] = '.'
#             new_rows[north_rock_row_location[0]][north_rock_row_location[1]] = 'O'

#             return roll_rock_north(rows=new_rows, rock_location=north_rock_row_location)
#         case '#' | 'O':
#             return rows
#         case _:
#             raise Exception('unexpected rock')


# def roll_rocks_north(*, rows: Sequence[Sequence[str]]) -> Sequence[Sequence[str]]:
#     new_rows = rows
#     for row_index, row in enumerate(rows):
#         for column_index, cell in enumerate(row):
#             match cell:
#                 case '.' | '#':
#                     pass
#                 case 'O':
#                     new_rows = roll_rock_north(rows=new_rows, rock_location=(row_index, column_index))
#                 case _:
#                     raise Exception('unexpected cell')

#     return new_rows


# def count_rocks(*, rows: Sequence[Sequence[str]]) -> int:
#     return sum(
#         row.count('O') * (len(rows) - index)
#         for index, row in enumerate(rows)
#     )


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
    for row_index, row in enumerate(grid):
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
    for row_index, row in enumerate(grid):
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


def print_grid(grid: Grid, /) -> None:
    for row in grid:
        print(''.join(row))
    print()


def solution(content: str, /) -> int:
    grid = CONTENT.parse(content)
    print_grid(grid)
    roll_rocks_east(grid=grid)
    print_grid(grid)
    # new_rows = roll_rocks_north(rows=rows)

    # return count_rocks(rows=new_rows)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
