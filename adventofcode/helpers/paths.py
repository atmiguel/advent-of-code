from pathlib import Path


def is_root(*, path: Path) -> bool:
    return path == path.parent


def _find_source_directory_path() -> Path:
    source_directory_name = 'adventofcode'

    path = Path(__file__)
    while path.name != source_directory_name:
        path = path.parent

        if is_root(path=path):
            raise Exception(f'expected to find {source_directory_name} in {__file__}')

    return path


SOURCE_DIRECTORY_PATH = _find_source_directory_path()
PROJECT_DIRECTORY_PATH = SOURCE_DIRECTORY_PATH.parent
