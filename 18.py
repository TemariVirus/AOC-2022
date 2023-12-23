from queue import Queue
from time import time

start = time()

with open("18.txt", "r") as f:
    input = f.read()

cubes = set(tuple(map(int, line.split(","))) for line in input.splitlines())
min_x, max_x = min(x for x, y, z in cubes), max(x for x, y, z in cubes)
min_y, max_y = min(y for x, y, z in cubes), max(y for x, y, z in cubes)
min_z, max_z = min(z for x, y, z in cubes), max(z for x, y, z in cubes)

filled: set[tuple[int, int, int]] = set()


def fill_from(cube: tuple[int, int, int]) -> None:
    global filled

    new_cubes = Queue()
    new_cubes.put(cube)
    while not new_cubes.empty():
        cube = new_cubes.get()
        if cube in filled or cube in cubes:
            continue
        filled.add(cube)

        x, y, z = cube
        if x > min_x:
            new_cubes.put((x - 1, y, z))
        if x < max_x:
            new_cubes.put((x + 1, y, z))
        if y > min_y:
            new_cubes.put((x, y - 1, z))
        if y < max_y:
            new_cubes.put((x, y + 1, z))
        if z > min_z:
            new_cubes.put((x, y, z - 1))
        if z < max_z:
            new_cubes.put((x, y, z + 1))


for y in range(min_y, max_y + 1):
    for z in range(min_z, max_z + 1):
        fill_from((min_x, y, z))
        fill_from((max_x, y, z))
for x in range(min_x, max_x + 1):
    for z in range(min_z, max_z + 1):
        fill_from((x, min_y, z))
        fill_from((x, max_y, z))
for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        fill_from((x, y, min_z))
        fill_from((x, y, max_z))

surface_area = 0
for a in cubes:
    if a[0] == min_x:
        surface_area += 1
    if a[0] == max_x:
        surface_area += 1
    if a[1] == min_y:
        surface_area += 1
    if a[1] == max_y:
        surface_area += 1
    if a[2] == min_z:
        surface_area += 1
    if a[2] == max_z:
        surface_area += 1
    for b in filled:
        equal_count = sum(a_pos == b_pos for a_pos, b_pos in zip(a, b))
        adjacent_count = sum(abs(a_pos - b_pos) == 1 for a_pos, b_pos in zip(a, b))
        if equal_count == 2 and adjacent_count == 1:
            surface_area += 1

print(f"Answer: {surface_area}")
print(f"Time taken: {time() - start}s")


# Part 1 (10 lines)
# from itertools import combinations
# input = open("18_input.txt").readlines()
# cubes = tuple(tuple(map(int, line.split(","))) for line in input)
# surface_area = 6 * len(cubes)
# for a, b in combinations(cubes, 2):
#     equal_count = sum(a_pos == b_pos for a_pos, b_pos in zip(a, b))
#     adjacent_count = sum(abs(a_pos - b_pos) == 1 for a_pos, b_pos in zip(a, b))
#     if equal_count == 2 and adjacent_count == 1:
#         surface_area -= 2
# print(f"Answer: {surface_area}")
