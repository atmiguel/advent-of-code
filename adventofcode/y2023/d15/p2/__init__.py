import parsy

from adventofcode.helpers import executor, parsers

LABEL = parsy.letter.at_least(1).concat()
SET_VALUE = parsy.seq(
    LABEL.skip(parsy.string('=')),
    parsy.decimal_digit
)
REMOVE_VALUE = LABEL.skip(parsy.string('-')),

LABEL_VALUE = SET_VALUE | REMOVE_VALUE

CONTENT = (
    LABEL_VALUE.sep_by(parsy.string(','))
    .skip(parsers.NEWLINE.many())
)


def calculate_hash(string: str, /) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256

    return value


def solution(content: str, /) -> int:
    sequence = CONTENT.parse(content)

    return sum(
        calculate_hash(step)
        for step in sequence
    )


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
