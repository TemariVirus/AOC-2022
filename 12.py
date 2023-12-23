from time import time
from queue import Queue

with open("12.txt", "r") as f:
    input = f.read()

start_time = time()

start, end = input.index("S"), input.index("E")
input = input.replace("S", "a")
input = input.replace("E", "z")
map = [[ord(c) - ord("a") for c in line] for line in input.splitlines()]
width = len(map[0]) + 1
start = (start % width, start // width)
end = (end % width, end // width)


def a_star(
    map: list[list[int]], start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(
        came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path

    g_score = {start: heuristic(start, start)}
    f_score = {start: g_score[start] + heuristic(start, end)}
    came_from = dict()
    closed_set = set()
    open_set = {start}
    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if current == end:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)
        for neighbor in [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]:
            if (
                neighbor[0] < 0
                or neighbor[0] >= len(map[0])
                or neighbor[1] < 0
                or neighbor[1] >= len(map)
                or neighbor in closed_set
                or map[neighbor[1]][neighbor[0]] - map[current[1]][current[0]] > 1
            ):
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
            if neighbor not in open_set:
                open_set.add(neighbor)

    raise Exception("No path found")


def part_one():
    path = a_star(map, start, end)
    print(len(path) - 1)


def part_two():
    distances = [[0 for _ in range(len(map[0]))] for _ in range(len(map))]
    queue = Queue()
    queue.put(end)
    while queue.qsize():
        current = queue.get()
        for neighbor in [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]:
            if (
                neighbor[0] < 0
                or neighbor[0] >= len(map[0])
                or neighbor[1] < 0
                or neighbor[1] >= len(map)
                or distances[neighbor[1]][neighbor[0]] != 0
                or map[current[1]][current[0]] - map[neighbor[1]][neighbor[0]] > 1
            ):
                continue

            distances[neighbor[1]][neighbor[0]] = distances[current[1]][current[0]] + 1
            queue.put(neighbor)

            if map[neighbor[1]][neighbor[0]] == 0:
                print(distances[neighbor[1]][neighbor[0]])
                return


part_one()
print(f"Time taken: {time() - start_time}s")
