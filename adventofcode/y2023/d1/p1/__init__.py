from pathlib import Path
from adventofcode.helpers import resources


def find_first_digit(*, line: str) -> int:
    for char in line:
        if char.isdigit():
            return int(char)

    raise Exception('expected to find a digit')


def find_last_digit(*, line: str) -> int:
    for i in range(len(line) - 1, -1, -1):
        char = line[i]
        if char.isdigit():
            return int(char)

    raise Exception('expected to find a digit')


def extract_value_from_line(*, line: str) -> int:
    first_digit = find_first_digit(line=line)
    last_digit = find_last_digit(line=line)

    return (10 * first_digit) + last_digit


def extract_value_from_lines(*, lines: list[str]) -> int:
    return sum(
        extract_value_from_line(line=line)
        for line in lines
    )


# TODO move this to a shared place
# TODO add type to lines_consumer
def execute(*, lines_consumer, file_path: str) -> None:
    lines = file.read_lines(path=file_path)
    value = lines_consumer(lines)
    print(f'Result for {file_path}:')
    print(value)

    filename = get_filename_without_extension(file_path=file_path)
    write_to_file(content=str(value), file_path=f'{filename}_output.txt')


def main():
    print(resources.read_actual(__file__))

    # print(__file__)
    # print(file.read_lines(path='resources/y2023/d1/p1/in/example.txt'))
    # execute(
    #     lines_consumer=lambda lines: extract_value_from_lines(lines=lines),
    #     file_path='example.txt',
    # )
    # execute(
    #     lines_consumer=lambda lines: extract_value_from_lines(lines=lines),
    #     file_path='../input.txt',
    # )
