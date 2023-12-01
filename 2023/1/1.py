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


def read_file_as_lines(*, file_path: str) -> list[str]:
    with open(file_path, 'r') as fin:
        content = fin.read()

    return [
        line
        for line in content.split('\n')
        if len(line) > 0
    ]


if __name__ == '__main__':
    # lines = read_file_as_lines(file_path='example.txt')
    lines = read_file_as_lines(file_path='actual.txt')
    value = extract_value_from_lines(lines=lines)
    print(value)

