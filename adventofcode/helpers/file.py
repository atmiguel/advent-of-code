from pathlib import Path
from typing import Sequence


def read_lines(*, path: Path) -> Sequence[str]:
    with open(path, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    if len(lines[-1]) == 0:
        lines = lines[:-1]

    return tuple(lines)


def write(*, content: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as f:
        f.write(content)
        f.write('\n')
