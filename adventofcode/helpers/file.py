from pathlib import Path
from typing import Sequence


def read_lines(*, path: Path) -> Sequence[str]:
    with open(path, 'r') as f:
        content = f.read()

    return tuple(
        line
        for line in content.split('\n')
        if len(line) > 0
    )


def write(*, content: str, path: Path) -> None:
    with open(path, 'w') as f:
        f.write(content)
        f.write('\n')
