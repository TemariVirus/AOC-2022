from time import time

with open("08.txt", "r") as f:
    input = f.read()

start = time()


def scenic_score(x: int, y: int, trees: list[list[int]]) -> int:
    height = trees[y][x]
    # Left
    left = x - 1
    while left > 0:
        if trees[y][left] >= height:
            break
        left -= 1
    else:
        left = 0
    left = x - left
    # Right
    right = x + 1
    while right < len(trees[y]) - 1:
        if trees[y][right] >= height:
            break
        right += 1
    else:
        right = len(trees[y]) - 1
    right -= x
    # Up
    up = y - 1
    while up > 0:
        if trees[up][x] >= height:
            break
        up -= 1
    else:
        up = 0
    up = y - up
    # Down
    down = y + 1
    while down < len(trees) - 1:
        if trees[down][x] >= height:
            break
        down += 1
    else:
        down = len(trees) - 1
    down -= y
    return left * right * up * down


input = [[int(c) for c in line] for line in input.split("\n")]
print(
    max(
        scenic_score(x, y, input)
        for x in range(len(input[0]))
        for y in range(len(input))
    )
)
print(f"Time taken: {time() - start}s")
