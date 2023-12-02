from typing import Sequence

from adventofcode.helpers import executor
from adventofcode.y2023.d2 import p1


def calculate_max(*, color: str, cube_sets: Sequence[p1.CubeSet]) -> int:
    return max(
        cube_set.counts_by_color.get(color, 0)
        for cube_set in cube_sets
    )


def calculate_power(*, game: p1.Game) -> int:
    max_red = calculate_max(color='red', cube_sets=game.cube_sets)
    max_green = calculate_max(color='green', cube_sets=game.cube_sets)
    max_blue = calculate_max(color='blue', cube_sets=game.cube_sets)

    return max_red * max_green * max_blue


def solution(lines: Sequence[str], /) -> None:
    return sum(
        calculate_power(game=game)
        for game in p1.Deserializer.to_games(lines=lines)
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
