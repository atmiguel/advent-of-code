import parsy

from adventofcode.helpers import executor, parsers

CHAR = parsy.regex(r'[a-z0-9\=\-]')
STEP = CHAR.at_least(1).concat()

CONTENT = (
    STEP.sep_by(parsy.string(','))
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
    executor.execute_actual(solution)
