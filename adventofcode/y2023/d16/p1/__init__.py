import parsy

from adventofcode.helpers import executor, parsers

CELL = parsy.regex(r'[\.\|\-\\\/]')
ROW = CELL.at_least(1).concat()

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)


def solution(content: str, /) -> int:
    grid = CONTENT.parse(content)
    print(grid)

    # return sum(
    #     calculate_hash(step)
    #     for step in sequence
    # )


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
