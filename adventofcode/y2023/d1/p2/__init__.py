from typing import Sequence

from adventofcode.helpers import executor


DIGITS_BY_WORD = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def find_first_digit(*, line: str) -> int:
    if len(line) == 0:
        raise Exception('expected to find digit')

    char = line[0]
    if char.isdigit():
        return int(char)

    for word, digit in DIGITS_BY_WORD.items():
        if line.startswith(word):
            return digit

    return find_first_digit(line=line[1:])


def find_last_digit(*, line: str) -> int:
    if len(line) == 0:
        raise Exception('expected to find digit')

    char = line[-1]
    if char.isdigit():
        return int(char)

    for word, digit in DIGITS_BY_WORD.items():
        if line.endswith(word):
            return digit

    return find_last_digit(line=line[:-1])


def calculate_value(*, line: str) -> int:
    first_digit = find_first_digit(line=line)
    last_digit = find_last_digit(line=line)

    return (10 * first_digit) + last_digit


def solution(lines: Sequence[str], /) -> int:
    return sum(
        calculate_value(line=line)
        for line in lines
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
