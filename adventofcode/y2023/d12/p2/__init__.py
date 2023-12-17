from dataclasses import dataclass
import parsy
from typing import Sequence, Optional

from adventofcode.helpers import executor, parsers

SPRING = parsy.regex(r'[\?\.#]')
ROW = parsy.seq(
    SPRING.at_least(1).concat()
    .skip(parsers.SPACE),
    parsers.NUMBER.sep_by(parsy.string(','))
)

CONTENT = (
    ROW.sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)


@dataclass(frozen=True, kw_only=True)
class SpringRow:
    damaged_groups: Sequence[int]
    springs: str


def parse_spring_rows(*, content: str) -> Sequence[SpringRow]:
    rows = CONTENT.parse(content)

    return [
        SpringRow(
            damaged_groups=tuple(damaged_groups * 5),
            springs='?'.join([springs] * 5),
        )
        for springs, damaged_groups in rows
    ]


class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(
            self,
            *,
            springs: str,
            damaged_groups: Sequence[int],
            damage_count: Optional[int] = 0,
    ) -> int:
        key = (springs, damaged_groups, damage_count)
        if key not in self.memo:
            self.memo[key] = self.fn(
                springs=springs,
                damaged_groups=damaged_groups,
                damage_count=damage_count,
            )

        return self.memo[key]


@Memoize
def calculate_arrangements(
        *,
        springs: str,
        damaged_groups: Sequence[int],
        damage_count: Optional[int] = 0,
) -> int:
    for index, spring in enumerate(springs):
        match spring:
            case '#':
                damage_count += 1

                if len(damaged_groups) == 0:
                    # invalid configuration
                    return 0

                if damage_count > damaged_groups[0]:
                    # invalid configuration
                    return 0
            case '.':
                if damage_count == 0:
                    continue

                if len(damaged_groups) == 0:
                    continue

                if damage_count != damaged_groups[0]:
                    # invalid configuration
                    return 0

                # good, recurse down
                return calculate_arrangements(
                    damaged_groups=damaged_groups[1:],
                    springs=springs[index + 1:],
                )
            case '?':
                if len(damaged_groups) == 0:
                    return calculate_arrangements(
                        damage_count=damage_count,
                        damaged_groups=damaged_groups,
                        springs=f'.{springs[index + 1:]}',
                    )

                if damage_count == damaged_groups[0]:
                    return calculate_arrangements(
                        damage_count=0,
                        damaged_groups=damaged_groups[1:],
                        springs=f'.{springs[index + 1:]}',
                    )

                value_if_damaged = calculate_arrangements(
                    damage_count=damage_count,
                    damaged_groups=damaged_groups,
                    springs=f'#{springs[index + 1:]}',
                )
                value_if_not_damaged = calculate_arrangements(
                    damage_count=damage_count,
                    damaged_groups=damaged_groups,
                    springs=f'.{springs[index + 1:]}',
                )

                return value_if_damaged + value_if_not_damaged
            case _:
                raise Exception(f'unexpected spring: {spring}')

    if len(damaged_groups) == 0:
        return 1

    if len(damaged_groups) > 1:
        # invalid
        return 0

    if damage_count != damaged_groups[0]:
        # invalid
        return 0

    return 1


def solution(content: str, /) -> int:
    spring_rows = parse_spring_rows(content=content)

    return sum(
        calculate_arrangements(
            springs=spring_row.springs,
            damaged_groups=spring_row.damaged_groups,
        )
        for spring_row in spring_rows
    )


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
