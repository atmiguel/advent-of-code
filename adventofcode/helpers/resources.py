from pathlib import Path
from typing import Sequence

from adventofcode.helpers.paths import PROJECT_DIRECTORY_PATH, SOURCE_DIRECTORY_PATH
from adventofcode.helpers import file


RESOURCES_DIRECTORY_PATH = PROJECT_DIRECTORY_PATH / 'resources'


def _find_resources_directory_path(*, code_path: str) -> Path:
    path_relative_to_source = Path(code_path).relative_to(SOURCE_DIRECTORY_PATH)
    return RESOURCES_DIRECTORY_PATH / path_relative_to_source.parent


def _find_input_directory_path(*, code_path: str) -> Path:
    return _find_resources_directory_path(code_path=code_path) / 'in'


def _find_output_directory_path(*, code_path: str) -> Path:
    return _find_resources_directory_path(code_path=code_path) / 'out'


def _read_input_file(*, code_path: str, filename: str) -> Sequence[str]:
    path = _find_input_directory_path(code_path=code_path) / filename
    return file.read_lines(path=path)


# returns output file path
def _write_output_file(*, code_path: str, content: str, filename: str) -> Path:
    path = _find_output_directory_path(code_path=code_path) / filename
    file.write(content=content, path=path)

    return path


def read_example(*, code_path: str) -> Sequence[str]:
    return _read_input_file(code_path=code_path, filename='example.txt')


def read_actual(*, code_path: str) -> Sequence[str]:
    return _read_input_file(code_path=code_path, filename='actual.txt')


# returns output file path
def write_example(*, code_path: str, content: str) -> Path:
    return _write_output_file(
        code_path=code_path,
        content=content,
        filename='example.txt',
    )


# returns output file path
def write_actual(*, code_path: str, content: str) -> Path:
    return _write_output_file(
        code_path=code_path,
        content=content,
        filename='actual.txt',
    )
