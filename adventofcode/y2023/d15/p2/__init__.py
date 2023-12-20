import parsy

from adventofcode.helpers import executor, parsers
from typing import Sequence, Union, Tuple

LABEL = parsy.letter.at_least(1).concat()
SET_VALUE = parsy.seq(
    LABEL.skip(parsy.string('=')),
    parsers.NUMBER
)
REMOVE_VALUE = LABEL.skip(parsy.string('-'))

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


def calculate_hashmap(*, sequence: Sequence[Union[str, Tuple[str, int]]]) -> Sequence[Sequence[Tuple[str, int]]]:
    hashmap = [[] for _ in range(256)]
    for step in sequence:
        if isinstance(step, str):
            index = calculate_hash(step)
            values = hashmap[index]

            index_to_replace = -1
            for i, (label, _) in enumerate(values):
                if label == step:
                    index_to_replace = i
                    break

            if index_to_replace >= 0:
                del values[index_to_replace]
        else:
            label, value = step
            index = calculate_hash(label)
            values = hashmap[index]

            index_to_replace = -1
            for i, (inner_label, _) in enumerate(values):
                if inner_label == label:
                    index_to_replace = i
                    break

            if index_to_replace >= 0:
                values[index_to_replace] = (label, value)
            else:
                values.append((label, value))

    return hashmap


def calculate_hashmap_value(*, hashmap: Sequence[Sequence[Tuple[str, int]]]) -> int:
    total = 0
    for box_index, values in enumerate(hashmap):
        for slot_index, (_, value) in enumerate(values):
            total += (box_index + 1) * (slot_index + 1) * value

    return total


def solution(content: str, /) -> int:
    sequence = CONTENT.parse(content)
    hashmap = calculate_hashmap(sequence=sequence)

    return calculate_hashmap_value(hashmap=hashmap)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
