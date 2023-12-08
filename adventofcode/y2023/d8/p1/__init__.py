from dataclasses import dataclass
import parsy
from typing import Sequence, Dict

from adventofcode.helpers import executor, parsers


DIRECTION = parsy.regex(r'[RL]')
DIRECTIONS = DIRECTION.at_least(1)

NODE_NAME = parsy.letter.times(3).concat()

NODE_LINE = parsy.seq(
    NODE_NAME
    .skip(parsers.SPACES)
    .skip(parsy.string('='))
    .skip(parsers.SPACES)
    .skip(parsy.string('(')),
    NODE_NAME
    .skip(parsy.string(','))
    .skip(parsers.SPACES),
    NODE_NAME
    .skip(parsy.string(')')),
)

CONTENT = parsy.seq(
    DIRECTIONS
    .skip(parsers.NEWLINES),
    NODE_LINE
    .sep_by(parsers.NEWLINE)
    .skip(parsers.NEWLINE.many())
)


@dataclass(frozen=True, kw_only=True)
class Node:
    left: str
    right: str


@dataclass(frozen=True, kw_only=True)
class Network:
    directions: str
    nodes_by_name: Dict[str, Node]


def parse_network(*, content: str) -> Network:
    directions, nodes = CONTENT.parse(content)

    nodes_by_name = {}
    for (node_name, left, right) in nodes:
        nodes_by_name[node_name] = Node(
            left=left,
            right=right,
        )

    return Network(
        directions=directions,
        nodes_by_name=nodes_by_name,
    )


def follow_direction(*, current_node_name: str, direction: str, nodes_by_name: Dict[str, Node]) -> str:
    current_node = nodes_by_name[current_node_name]

    match direction:
        case 'L':
            return current_node.left
        case 'R':
            return current_node.right
        case _:
            raise Exception(f'unexpected direction: {direction}')


def follow_directions(*, current_node_name: str, directions: Sequence[str], nodes_by_name: Dict[str, Node]) -> str:
    current = current_node_name
    for direction in directions:
        current = follow_direction(
            current_node_name=current,
            direction=direction,
            nodes_by_name=nodes_by_name,
        )

    return current


def count_steps(*, network: Network) -> int:
    current = 'AAA'  # start node name
    step_count = 0
    while current != 'ZZZ':  # end node name
        current = follow_directions(
            current_node_name=current,
            directions=network.directions,
            nodes_by_name=network.nodes_by_name,
        )
        step_count += len(network.directions)

    return step_count


def solution(content: str, /) -> int:
    network = parse_network(content=content)
    return count_steps(network=network)


def main():
    executor.execute_example(solution)
    # executor.execute_actual(solution)
