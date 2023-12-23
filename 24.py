from time import time

with open("24.txt", "r") as f:
    input = f.read()

start = time()

input = [line[1:-1] for line in input.splitlines()[1:-1]]
WIDTH, HEIGHT = len(input[0]), len(input)


horizontals: dict[int, list[tuple[int, int]]] = {i: [] for i in range(-1, HEIGHT + 1)}
verticals: dict[int, list[tuple[int, int]]] = {i: [] for i in range(WIDTH)}
for y, line in enumerate(input):
    for x, char in enumerate(line):
        if char in "<>":
            horizontals[y].append((x, 1 if char == ">" else -1))
        if char in "^v":
            verticals[x].append((y, 1 if char == "v" else -1))


def shortest_path_length(
    start_pos: tuple[int, int], target: tuple[int, int], start_time: int
) -> int:
    global horizontals, verticals, WIDTH, HEIGHT

    i = start_time + 1

    nodes = {start_pos}
    while True:
        new_nodes = set()
        for node in nodes:
            for neighbour in (
                (node[0] + 1, node[1]),
                (node[0] - 1, node[1]),
                (node[0], node[1] + 1),
                (node[0], node[1] - 1),
                node,
            ):
                if neighbour == target:
                    return i - start_time
                # Special case for starting node
                if neighbour == start_pos:
                    new_nodes.add(neighbour)
                    continue
                # Check if out of bounds
                if (
                    neighbour[0] < 0
                    or neighbour[1] < 0
                    or neighbour[0] >= WIDTH
                    or neighbour[1] >= HEIGHT
                ):
                    continue
                # Check if inside blizzard
                if neighbour[0] in tuple(
                    map(
                        lambda b: (b[0] + i * b[1]) % WIDTH,
                        horizontals[neighbour[1]],
                    )
                ) or neighbour[1] in tuple(
                    map(
                        lambda b: (b[0] + i * b[1]) % HEIGHT,
                        verticals[neighbour[0]],
                    )
                ):
                    continue

                new_nodes.add(neighbour)

        nodes = new_nodes
        if not nodes:
            break
        i += 1

    raise Exception("No path found")


length = shortest_path_length((0, -1), (WIDTH - 1, HEIGHT), 0)
print(length)
length += shortest_path_length((WIDTH, HEIGHT - 1), (0, -1), length)
print(length)
length += shortest_path_length((0, -1), (WIDTH - 1, HEIGHT), length)
print(length)
print(f"Time taken: {time() - start}s")
