import copy
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


def print_rows(rows: Sequence[Sequence[str]], /) -> None:
    for row in rows:
        print(''.join(row))
    print()


def roll_rock_north(*, rows: Sequence[Sequence[str]], rock_location: Location) -> Sequence[Sequence[str]]:
    north_rock_row_location = (rock_location[0] - 1, rock_location[1])
    if north_rock_row_location[0] < 0:
        return rows

    north_rock = rows[north_rock_row_location[0]][north_rock_row_location[1]]
    match north_rock:
        case '.':
            new_rows = copy.deepcopy(rows)
            new_rows[rock_location[0]][rock_location[1]] = '.'
            new_rows[north_rock_row_location[0]][north_rock_row_location[1]] = 'O'

            return roll_rock_north(rows=new_rows, rock_location=north_rock_row_location)
        case '#' | 'O':
            return rows
        case _:
            raise Exception('unexpected rock')


def roll_rocks_north(*, rows: Sequence[Sequence[str]]) -> Sequence[Sequence[str]]:
    new_rows = rows
    for row_index, row in enumerate(rows):
        for column_index, cell in enumerate(row):
            match cell:
                case '.' | '#':
                    pass
                case 'O':
                    new_rows = roll_rock_north(rows=new_rows, rock_location=(row_index, column_index))
                case _:
                    raise Exception('unexpected cell')

    return new_rows


def count_rocks(*, rows: Sequence[Sequence[str]]) -> int:
    return sum(
        row.count('O') * (len(rows) - index)
        for index, row in enumerate(rows)
    )


def solution(content: str, /) -> int:
    rows = CONTENT.parse(content)
    new_rows = roll_rocks_north(rows=rows)

    return count_rocks(rows=new_rows)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
