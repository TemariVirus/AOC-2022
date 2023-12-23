from functools import reduce
import os
from time import time

start = time()

with open("14.txt", "r") as f:
    input = f.read()


def get_bounding_box(vertices: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    left = min(map(lambda r: r[0], vertices))
    right = max(map(lambda r: r[0], vertices))
    top = min(map(lambda r: r[1], vertices))
    bottom = max(map(lambda r: r[1], vertices))
    return left, right, top, bottom


rocks = [
    [tuple(map(int, v.split(","))) for v in line.split(" -> ")]
    for line in input.splitlines()
]
LEFT, RIGHT, TOP, BOTTOM = get_bounding_box(reduce(list.__add__, rocks))
LEFT, RIGHT = LEFT - 200, RIGHT + 200
WIDTH = RIGHT - LEFT + 1
TOP, BOTTOM = 0, BOTTOM + 2
HEIGHT = BOTTOM - TOP + 1
grid = [["."] * WIDTH for _ in range(HEIGHT)]
grid[-1] = ["#"] * WIDTH
for rock in rocks:
    for i in range(1, len(rock)):
        start_x, start_y = rock[i - 1]
        end_x, end_y = rock[i]
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                grid[y - TOP][x - LEFT] = "#"


SOURCE_X, SOURCE_Y = 500 - LEFT, 0


def print_grid():
    os.system("cls" if os.name == "nt" else "clear")
    print("\n".join("".join(row) for row in grid))


def spawn_sand(x: int, y: int) -> bool:
    global grid

    while True:
        if grid[y + 1][x] == ".":
            y += 1
        elif grid[y + 1][x - 1] == ".":
            y += 1
            x -= 1
        elif grid[y + 1][x + 1] == ".":
            y += 1
            x += 1
        else:
            grid[y][x] = "o"
            return x != SOURCE_X or y != SOURCE_Y


count = 0
while True:
    count += 1
    if not spawn_sand(SOURCE_X, SOURCE_Y):
        break

    # if count % 300 == 0:
    #     print_grid()

print(count)
print(f"Time taken: {time() - start}s")
