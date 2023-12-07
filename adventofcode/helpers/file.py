from pathlib import Path


def read_content(*, path: Path) -> str:
    with open(path, 'r') as f:
        return f.read()


def write(*, content: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as f:
        f.write(content)
        f.write('\n')
