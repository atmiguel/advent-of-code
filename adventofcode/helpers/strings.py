from typing import Sequence


def split(value: str, /, *, delimiter: str, expected_count: int) -> Sequence[str]:
    parts = value.split(delimiter)
    assert len(parts) == expected_count, \
        f'expected {expected_count} parts splitting {value} by {delimiter}'

    return parts
