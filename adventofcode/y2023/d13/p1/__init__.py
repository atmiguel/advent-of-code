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


def solution(content: str, /) -> int:
    fields = parse_fields(content=content)

    print(fields)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
