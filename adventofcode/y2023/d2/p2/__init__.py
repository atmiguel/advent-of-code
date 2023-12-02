from dataclasses import dataclass
from typing import Sequence, Dict, Tuple

from adventofcode.helpers import executor


COLORS = {'red', 'green', 'blue'}

# 12 red cubes, 13 green cubes, and 14 blue cubes
MAX_COUNTS_BY_COLOR = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


@dataclass(frozen=True, kw_only=True)
class CubeSet:
    counts_by_color: Dict[str, int]


@dataclass(frozen=True, kw_only=True)
class Game:
    id_: int
    cube_sets: Sequence[CubeSet]


# TODO: Move this to shared location
def split(value: str, /, *, delimiter: str, expected_count: int) -> Sequence[str]:
    parts = value.split(delimiter)
    assert len(parts) == expected_count, \
        f'expected {expected_count} parts splitting {value} by {delimiter}'

    return parts


class Deserializer:
    # line = <game_part>: <cubes_part>
    # game_part = Game <game_id>
    # cubes_part = <cube_set>; <cube_set>; ...
    # cube_set = <cube_spec>, <cube_spec>, ...
    # cube_spec = <cube_count> <cube_color>

    @staticmethod
    def to_game_id(*, game_part: str) -> int:
        game_word, id_ = split(game_part, delimiter=' ', expected_count=2)
        assert game_word == 'Game'

        return int(id_)

    @staticmethod
    def to_cube_spec(*, cube_spec: str) -> Tuple[str, int]:
        # returns (cube_color, cube_count)

        cube_count, cube_color = split(cube_spec, delimiter=' ', expected_count=2)
        assert cube_color in COLORS

        return (cube_color, int(cube_count))

    @staticmethod
    def to_cube_set(*, cube_set: str) -> CubeSet:
        counts_by_color = dict(
            Deserializer.to_cube_spec(cube_spec=cube_spec)
            for cube_spec in cube_set.split(', ')
        )

        return CubeSet(counts_by_color=counts_by_color)

    @staticmethod
    def to_cube_sets(*, cubes_part: str) -> Sequence[CubeSet]:
        return tuple(
            Deserializer.to_cube_set(cube_set=cube_set)
            for cube_set in cubes_part.split('; ')
        )

    @staticmethod
    def to_game(*, line: str) -> Game:
        game_part, cubes_part = split(line, delimiter=': ', expected_count=2)
        id_ = Deserializer.to_game_id(game_part=game_part)
        cube_sets = Deserializer.to_cube_sets(cubes_part=cubes_part)

        return Game(id_=id_, cube_sets=cube_sets)


def is_cube_set_valid(*, cube_set: CubeSet) -> bool:
    for color, count in cube_set.counts_by_color.items():
        max_count = MAX_COUNTS_BY_COLOR[color]
        if count > max_count:
            return False

    return True


def is_game_valid(*, game: Game) -> bool:
    return all(
        is_cube_set_valid(cube_set=cube_set)
        for cube_set in game.cube_sets
    )


def solution(lines: Sequence[str], /) -> None:
    games = (
        Deserializer.to_game(line=line)
        for line in lines
    )

    return sum(
        game.id_
        for game in games
        if is_game_valid(game=game)
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
