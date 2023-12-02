import inspect
from pathlib import Path
from typing import Callable, Sequence, Any

from adventofcode.helpers import resources


def _print_result(*, is_example: bool, path: Path, result: str) -> None:
    descriptor = 'example' if is_example else 'actual'

    print(f'Wrote {descriptor} result to {path}')
    print('----')
    print(result)
    print()


def _execute(*, is_example: bool, lines_consumer: Callable[[Sequence[str]], Any]) -> None:
    # Copied from https://stackoverflow.com/a/60297932
    # Changed to [2] because it's in a helper function
    code_path = inspect.stack()[2].filename

    file_reader = resources.read_example if is_example else resources.read_actual
    file_writer = resources.write_example if is_example else resources.write_actual

    lines = file_reader(code_path=code_path)
    result = str(lines_consumer(lines))

    output_path = file_writer(code_path=code_path, content=result)
    _print_result(is_example=is_example, path=output_path, result=result)


def execute_example(lines_consumer: Callable[[Sequence[str]], Any], /) -> None:
    _execute(is_example=True, lines_consumer=lines_consumer)


def execute_actual(lines_consumer: Callable[[Sequence[str]], Any], /) -> None:
    _execute(is_example=False, lines_consumer=lines_consumer)
