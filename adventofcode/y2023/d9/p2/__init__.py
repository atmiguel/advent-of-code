from typing import Sequence

from adventofcode.helpers import executor, parsers


CONTENT = (
    parsers.NUMBER_LIST
    .sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)


def has_all_zeros(*, history: Sequence[int]) -> bool:
    return all(value == 0 for value in history)


def calculate_diff(*, history: Sequence[int]) -> Sequence[int]:
    return tuple(
        history[i + 1] - history[i]
        for i in range(len(history) - 1)
    )


def calculate_previous_value(*, history: Sequence[int]) -> int:
    if has_all_zeros(history=history):
        return 0

    diff = calculate_diff(history=history)
    previous_diff_value = calculate_previous_value(history=diff)

    return history[0] - previous_diff_value


def solution(content: str, /) -> int:
    histories = CONTENT.parse(content)

    return sum(
        calculate_previous_value(history=history)
        for history in histories
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
