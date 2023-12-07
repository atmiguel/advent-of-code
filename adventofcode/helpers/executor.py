import inspect
from pathlib import Path
from typing import Any, Callable 

from adventofcode.helpers import resources


def _print_result(*, is_example: bool, path: Path, result: str) -> None:
    descriptor = 'example' if is_example else 'actual'

    print(f'Wrote {descriptor} result to {path}')
    print('----')
    print(result)
    print()


def _execute(*, is_example: bool, consumer: Callable[[str], Any]) -> None:
    # Copied from https://stackoverflow.com/a/60297932
    # Changed to [2] because it's in a helper function
    code_path = inspect.stack()[2].filename

    file_reader = resources.read_example if is_example else resources.read_actual
    file_writer = resources.write_example if is_example else resources.write_actual

    content = file_reader(code_path=code_path)
    result = str(consumer(content))

    output_path = file_writer(code_path=code_path, content=result)
    _print_result(is_example=is_example, path=output_path, result=result)


def execute_example(consumer: Callable[[str], Any], /) -> None:
    _execute(is_example=True, consumer=consumer)


def execute_actual(consumer: Callable[[str], Any], /) -> None:
    _execute(is_example=False, consumer=consumer)
