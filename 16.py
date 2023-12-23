from functools import cache
from queue import Queue
import re
from time import time
from typing import TypeVar, Hashable, Iterator


T = TypeVar("T", bound=Hashable)

with open("16.txt", "r") as f:
    input = f.read()


def calculate_distances(node: T, graph: dict[T, tuple[T, ...]]) -> dict[T, int]:
    distances = {key: -1 for key in graph.keys()}
    distances[node] = 0
    queue = Queue()
    queue.put(node)
    while not queue.empty():
        node = queue.get()
        for neighbour in graph[node]:
            if distances[neighbour] < 0:
                distances[neighbour] = distances[node] + 1
                queue.put(neighbour)

    return distances


def compress_graph(
    graph: dict[str, tuple[int, tuple[str, ...]]]
) -> tuple[dict[int, tuple[int, dict[int, int]]], dict[str, int]]:
    name_to_index = {name: i + 1 for i, name in enumerate(graph.keys())}
    graph = {
        name_to_index[k]: (v1, tuple(map(lambda x: name_to_index[x], v2)))
        for k, (v1, v2) in graph.items()
    }
    clean_graph = {node: neighbours for node, (_, neighbours) in graph.items()}
    start_node = name_to_index["AA"]

    useful_nodes = [node for node, (flow, _) in graph.items() if flow > 0]
    new_graph = dict()
    distances = calculate_distances(start_node, clean_graph)
    new_graph[start_node] = (
        graph[start_node][0],
        {n: distances[n] for n in useful_nodes},
    )

    for node in useful_nodes:
        distances = calculate_distances(node, clean_graph)
        new_graph[node] = (graph[node][0], {n: distances[n] for n in useful_nodes})

    return new_graph, name_to_index


def unique_product(*tuples: list[tuple[T, ...]]) -> tuple[tuple[T, ...], ...]:
    seen = set()

    def unique_product_inner(tuples: list[tuple[T, ...]]) -> Iterator[tuple[T, ...]]:
        if len(tuples) == 0:
            yield ()
            return

        yielded = False
        for item in tuples[-1]:
            if item in seen:
                continue

            seen.add(item)
            for result in unique_product_inner(tuples[:-1]):
                yield result + (item,)
            seen.remove(item)
            yielded = True

        if not yielded:
            for result in unique_product_inner(tuples[:-1]):
                yield result + (None,)

    return tuple(unique_product_inner(tuples))


@cache
def highest_pressure_release(
    open: tuple[int, ...], from_rooms: tuple[int, ...], time_lefts: tuple[int, ...]
) -> int:
    global valves, max_depth

    if not any(from_rooms):
        return 0

    open = set(open)
    time_lefts = tuple(x - 1 for x in time_lefts)
    choices = list(
        unique_product(
            *[
                [
                    node
                    for node, dist in valves[from_rooms[i]][1].items()
                    if node not in open and dist < time_lefts[i]
                ]
                for i in range(len(from_rooms))
                if from_rooms[i]
            ]
        )
    )

    highest = 0
    for rooms in choices:
        rooms_set = set(rooms).difference((None,))
        open = open.union(rooms_set)
        t_left = tuple(
            time_lefts[i] - valves[from_rooms[i]][1][rooms[i]]
            if from_rooms[i] and rooms[i]
            else 0
            for i in range(len(rooms))
        )
        highest = max(
            highest,
            sum(valves[rooms[i]][0] * t_left[i] for i in range(len(rooms)) if rooms[i])
            + highest_pressure_release(tuple(open), rooms, t_left),
        )
        open = open.difference(rooms_set)

    if max(time_lefts) + 1 > max_depth:
        max_depth = max(time_lefts) + 1
        print(
            f"Finished depth {max_depth} in {(time() - start).__round__(5)}s, highest: {highest}"
        )

    return highest


groups = [
    re.match(
        r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]+(, ?[A-Z]+)*)",
        line,
    ).groups()
    for line in input.splitlines()
]
valves, name_to_index = compress_graph(
    {g[0]: (int(g[1]), g[2].split(", ")) for g in groups}
)

max_depth = 0
start = time()

start_node = name_to_index["AA"]
# print(highest_pressure(tuple(), (start_node,), (30,)))
print(highest_pressure_release(tuple(), tuple([start_node] * 2), tuple([26] * 2)))
