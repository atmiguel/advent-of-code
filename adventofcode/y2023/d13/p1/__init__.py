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


def find_reflection_row(*, field: Field) -> int:
    for index in range(len(field.rows) - 1):
        top_index = index
        bottom_index = index + 1

        while field.rows[top_index] == field.rows[bottom_index]:
            top_index -= 1
            bottom_index += 1

            if top_index < 0:
                return index + 1

            if bottom_index >= len(field.rows):
                return index + 1

    return 0


def get_column(*, field: Field, index: int) -> str:
    return ''.join([
        row[index]
        for row in field.rows
    ])


def find_reflection_column(*, field: Field) -> int:
    for index in range(len(field.rows[0]) - 1):
        left_index = index
        right_index = index + 1

        while get_column(field=field, index=left_index) == get_column(field=field, index=right_index):
            left_index -= 1
            right_index += 1

            if left_index < 0:
                return index + 1

            if right_index >= len(field.rows[0]):
                return index + 1

    return 0


def solution(content: str, /) -> int:
    fields = parse_fields(content=content)

    total = 0
    for field in fields:
        reflection_row = find_reflection_row(field=field)
        reflection_column = find_reflection_column(field=field)

        total += 100 * reflection_row + reflection_column

    return total


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
