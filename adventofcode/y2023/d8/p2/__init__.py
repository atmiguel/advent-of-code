from dataclasses import dataclass
import parsy
from typing import Sequence, Dict

from adventofcode.helpers import executor, parsers


DIRECTION = parsy.regex(r'[RL]')
DIRECTIONS = DIRECTION.at_least(1)

NODE_NAME = parsy.any_char.times(3).concat()

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


def are_all_end_nodes(*, node_names: Sequence[str]) -> bool:
    return all((
        name.endswith('Z')
        for name in node_names
    ))


def count_steps(*, destination_nodes_by_name: Dict[str, str]) -> int:
    current_node_names = list(
        name
        for name in destination_nodes_by_name.keys()
        if name.endswith('A')
    )
    step_count = 0
    while not are_all_end_nodes(node_names=current_node_names):
        for i, node_name in enumerate(current_node_names):
            current_node_names[i] = destination_nodes_by_name[node_name]

        step_count += 1

    return step_count


def calculate_destination_nodes_by_name(*, network: Network) -> Dict[str, str]:
    destination_nodes_by_name = {}
    for node_name in network.nodes_by_name.keys():
        next_node_name = follow_directions(
            current_node_name=node_name,
            directions=network.directions,
            nodes_by_name=network.nodes_by_name,
        )
        destination_nodes_by_name[node_name] = next_node_name

    return destination_nodes_by_name


def solution(content: str, /) -> int:
    network = parse_network(content=content)
    destination_nodes_by_name = calculate_destination_nodes_by_name(network=network)
    steps = count_steps(destination_nodes_by_name=destination_nodes_by_name)

    return steps * len(network.directions)


def main():
    executor.execute_example(solution)
    executor.execute_actual(solution)
