from dataclasses import dataclass
import parsy
from typing import Sequence, Optional

from adventofcode.helpers import executor, parsers

ASH_OR_ROCK = parsy.regex(r'[\.#]')
ROW = ASH_OR_ROCK.at_least(1).concat()
FIELD = ROW.sep_by(parsers.NEWLINE)

CONTENT = (
    FIELD.sep_by(parsers.NEWLINE.times(2))
    .skip(parsers.NEWLINE.many())
)


@dataclass(frozen=True, kw_only=True)
class Field:
    rows: Sequence[str]


def parse_fields(*, content: str) -> Sequence[Field]:
    fields = CONTENT.parse(content)

    return [
        Field(rows=field)
        for field in fields
    ]


def find_reflection_rows(*, field: Field) -> Sequence[int]:
    results = []
    for index in range(len(field.rows) - 1):
        top_index = index
        bottom_index = index + 1

        while field.rows[top_index] == field.rows[bottom_index]:
            top_index -= 1
            bottom_index += 1

            if top_index < 0 or bottom_index >= len(field.rows):
                results.append(index + 1)
                break

    return results


def get_column(*, field: Field, index: int) -> str:
    return ''.join([
        row[index]
        for row in field.rows
    ])


def find_reflection_columns(*, field: Field) -> Sequence[int]:
    results = []
    for index in range(len(field.rows[0]) - 1):
        left_index = index
        right_index = index + 1

        while get_column(field=field, index=left_index) == get_column(field=field, index=right_index):
            left_index -= 1
            right_index += 1

            if left_index < 0 or right_index >= len(field.rows[0]):
                results.append(index + 1)
                break

    return results


def generate_field(*, field: Field):
    for row_index, row in enumerate(field.rows):
        for column_index, cell in enumerate(row):
            match cell:
                case '#':
                    new_cell = '.'
                case '.':
                    new_cell = '#'
                case _:
                    raise Exception('unexpected cell')

            new_row = f'{row[:column_index]}{new_cell}{row[column_index + 1:]}'
            new_rows = field.rows[:row_index] + [new_row] + field.rows[row_index + 1:]

            yield Field(rows=new_rows)


def solution(content: str, /) -> int:
    fields = parse_fields(content=content)

    total = 0
    for field in fields:
        original_reflection_rows = set(find_reflection_rows(field=field))
        original_reflection_columns = set(find_reflection_columns(field=field))

        for generated_field in generate_field(field=field):
            reflection_rows = find_reflection_rows(field=generated_field)
            reflection_columns = find_reflection_columns(field=generated_field)

            should_break = False
            for reflection_row in reflection_rows:
                if reflection_row > 0 and reflection_row not in original_reflection_rows:
                    total += 100 * reflection_row
                    should_break = True
                    break

            for reflection_column in reflection_columns:
                if reflection_column > 0 and reflection_column not in original_reflection_columns:
                    total += reflection_column
                    should_break = True
                    break

            if should_break:
                break
        else:
            raise Exception('failed to find new reflection')

    return total


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
