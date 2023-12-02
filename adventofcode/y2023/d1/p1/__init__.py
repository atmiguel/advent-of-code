from pathlib import Path
from adventofcode.helpers import resources, executor
from typing import Sequence


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


def extract_value_from_line(*, line: str) -> int:
    first_digit = find_first_digit(line=line)
    last_digit = find_last_digit(line=line)

    return (10 * first_digit) + last_digit


def extract_value_from_lines(lines: Sequence[str]) -> str:
    return sum(
        extract_value_from_line(line=line)
        for line in lines
    )


def main():
    executor.execute_example(extract_value_from_lines)
    executor.execute_actual(extract_value_from_lines)
