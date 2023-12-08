from pathlib import Path

from adventofcode.helpers import file, paths


RESOURCES_DIRECTORY_PATH = paths.PROJECT_DIRECTORY_PATH / 'resources'


def _find_resources_directory_path(*, code_path: Path) -> Path:
    path_relative_to_source = code_path.relative_to(paths.SOURCE_DIRECTORY_PATH)
    return RESOURCES_DIRECTORY_PATH / path_relative_to_source.parent


def _find_input_directory_path(*, code_path: Path) -> Path:
    return _find_resources_directory_path(code_path=code_path) / 'in'


def _find_output_directory_path(*, code_path: Path) -> Path:
    return _find_resources_directory_path(code_path=code_path) / 'out'


def _read_input_file(*, code_path: Path, filename: str) -> str:
    while True:
        path = _find_input_directory_path(code_path=code_path) / filename
        if paths.is_root(path=path):
            raise Exception('failed to find input file')

        if path.is_file():
            break

        code_path = code_path.parent

    return file.read_content(path=path)


# returns output file path
def _write_output_file(*, code_path: Path, content: str, filename: str) -> Path:
    path = _find_output_directory_path(code_path=code_path) / filename
    file.write(content=content, path=path)

    return path


def read_example(*, code_path: str) -> str:
    return _read_input_file(
        code_path=Path(code_path),
        filename='example.txt',
    )


def read_actual(*, code_path: str) -> str:
    return _read_input_file(
        code_path=Path(code_path),
        filename='actual.txt',
    )


# returns output file path
def write_example(*, code_path: str, content: str) -> Path:
    return _write_output_file(
        code_path=Path(code_path),
        content=content,
        filename='example.txt',
    )


# returns output file path
def write_actual(*, code_path: str, content: str) -> Path:
    return _write_output_file(
        code_path=Path(code_path),
        content=content,
        filename='actual.txt',
    )
