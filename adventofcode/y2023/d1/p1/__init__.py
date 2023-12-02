from typing import Sequence

from adventofcode.helpers import executor


def find_first_digit(*, line: str) -> int:
    for char in line:
        if char.isdigit():
            return int(char)

    raise Exception('expected to find a digit')


def find_last_digit(*, line: str) -> int:
    for i in range(len(line) - 1, -1, -1):
        char = line[i]
        if char.isdigit():
            return int(char)

    raise Exception('expected to find a digit')


def calculate_value(*, line: str) -> int:
    first_digit = find_first_digit(line=line)
    last_digit = find_last_digit(line=line)

    return (10 * first_digit) + last_digit


def solution(lines: Sequence[str], /) -> str:
    return sum(
        calculate_value(line=line)
        for line in lines
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
