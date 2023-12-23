from re import finditer
from time import time

with open("22.txt", "r") as f:
    input = f.read()

start = time()

# region Parse input
input = input.split("\n\n")

maze = input[0]
maze = [line.rstrip() for line in maze.split("\n")]
WIDTH = max(map(len, maze))
HEIGHT = len(maze)
maze = (
    ["".ljust(WIDTH + 2)]
    + [" " + line.ljust(WIDTH) + " " for line in maze]
    + ["".ljust(WIDTH + 2)]
)

instructions = []
for match in finditer(r"\d+|[RL]", input[1]):
    match = match.group()
    if match.isnumeric():
        instructions.append(int(match))
    else:
        instructions.append(match)

faces = (
    ["".ljust(WIDTH + 2)]
    + [" " + (" " * 50) + ("1" * 50) + ("2" * 50) + " " for _ in maze[0:50]]
    + [" " + (" " * 50) + ("3" * 50) + (" " * 50) + " " for _ in maze[50:100]]
    + [" " + ("4" * 50) + ("5" * 50) + (" " * 50) + " " for _ in maze[100:150]]
    + [" " + ("6" * 50) + (" " * 50) + (" " * 50) + " " for _ in maze[150:200]]
    + ["".ljust(WIDTH + 2)]
)
# endregion

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
turn_left = {DOWN: RIGHT, RIGHT: UP, UP: LEFT, LEFT: DOWN}
turn_right = {DOWN: LEFT, LEFT: UP, UP: RIGHT, RIGHT: DOWN}
idx_to_facing = [RIGHT, DOWN, LEFT, UP]
facing_to_idx = {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}
facing_to_arrow = {RIGHT: ">", DOWN: "v", LEFT: "<", UP: "^"}

pos = (maze[1].index("."), 1)
facing = RIGHT
for instruction in instructions:
    if isinstance(instruction, str):
        facing = idx_to_facing[
            (facing_to_idx[facing] + (1 if instruction == "R" else -1)) % 4
        ]
        continue

    for _ in range(instruction):
        x = pos[0] + facing[0]
        y = pos[1] + facing[1]
        new_facing = facing
        if maze[y][x] == " ":
            face = faces[y - facing[1]][x - facing[0]]
            if face == "1" and facing == LEFT:
                x, y = 1, 151 - y
                new_facing = RIGHT
            elif face == "1" and facing == UP:
                x, y = 1, 100 + x
                new_facing = RIGHT
            elif face == "2" and facing == DOWN:
                x, y = 100, x - 50
                new_facing = LEFT
            elif face == "2" and facing == RIGHT:
                x, y = 100, 151 - y
                new_facing = LEFT
            elif face == "2" and facing == UP:
                x, y = x - 100, 200
                new_facing = UP
            elif face == "3" and facing == RIGHT:
                x, y = 50 + y, 50
                new_facing = UP
            elif face == "3" and facing == LEFT:
                x, y = y - 50, 101
                new_facing = DOWN
            elif face == "4" and facing == LEFT:
                x, y = 51, 151 - y
                new_facing = RIGHT
            elif face == "4" and facing == UP:
                x, y = 51, x + 50
                new_facing = RIGHT
            elif face == "5" and facing == RIGHT:
                x, y = 150, 151 - y
                new_facing = LEFT
            elif face == "5" and facing == DOWN:
                x, y = 50, x + 100
                new_facing = LEFT
            elif face == "6" and facing == LEFT:
                x, y = y - 100, 1
                new_facing = DOWN
            elif face == "6" and facing == DOWN:
                x, y = x + 100, 1
                new_facing = DOWN
            elif face == "6" and facing == RIGHT:
                x, y = y - 100, 150
                new_facing = UP

        if maze[y][x] == "#":
            break
        pos = (x, y)
        facing = new_facing

        # maze2 = [list(line) for line in maze]
        # maze2[pos[1]][pos[0]] = facing_to_arrow[facing]
        # print(instruction)
        # for line in maze2:
        #     print("".join(line))
        # print("\n\n\n")
        # input()

print(1000 * pos[1] + 4 * pos[0] + facing_to_idx[facing])
print(f"Time taken: {time() - start}s")
