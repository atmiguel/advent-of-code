from typing import Optional, Tuple

DIGITS_BY_WORD = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


# returns (index, digit)
def find_first_digit_char(*, line: str) -> Optional[Tuple[int, int]]:
    for index, char in enumerate(line):
        if char.isdigit():
            return (index, int(char))

    return None


# returns (index, digit)
def find_first_digit_word(*, line: str) -> Optional[Tuple[int, int]]:
    if len(line) == 0:
        return None

    for word, digit in DIGITS_BY_WORD.items():
        if line.startswith(word):
            return (0, digit)

    result = find_first_digit_word(line=line[1:])
    if result is None:
        return None

    index, digit = result
    return (index + 1, digit)


# returns (index, digit)
def find_last_digit_char(*, line: str) -> Optional[Tuple[int, int]]:
    for index in range(len(line) - 1, -1, -1):
        char = line[index]
        if char.isdigit():
            return (index, int(char))

    return None


# returns (index, digit)
def find_last_digit_word(*, line: str) -> Optional[Tuple[int, int]]:
    if len(line) == 0:
        return None

    for word, digit in DIGITS_BY_WORD.items():
        if line.endswith(word):
            return (len(line) - 1, digit)

    return find_last_digit_word(line=line[:-1])


def find_first_digit(*, line: str) -> int:
    word_result = find_first_digit_word(line=line)
    char_result = find_first_digit_char(line=line)

    if word_result is None:
        if char_result is None:
            raise Exception('expected to find a digit')

        _, digit = char_result
    else:
        if char_result is None:
            _, digit = word_result
        else:
            word_index, word_digit = word_result
            char_index, char_digit = char_result

            if word_index == char_index:
                raise Exception('indexes unexpectedly equal')

            if word_index < char_index:
                digit = word_digit
            else:
                digit = char_digit

    return digit


def find_last_digit(*, line: str) -> int:
    word_result = find_last_digit_word(line=line)
    char_result = find_last_digit_char(line=line)

    if word_result is None:
        if char_result is None:
            raise Exception('expected to find a digit')

        _, digit = char_result
    else:
        if char_result is None:
            _, digit = word_result
        else:
            word_index, word_digit = word_result
            char_index, char_digit = char_result

            if word_index == char_index:
                raise Exception('indexes unexpectedly equal')

            if word_index > char_index:
                digit = word_digit
            else:
                digit = char_digit

    return digit


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


def main():
    # lines = read_file_as_lines(file_path='example2.txt')
    lines = read_file_as_lines(file_path='actual.txt')
    value = extract_value_from_lines(lines=lines)
    print(value)
