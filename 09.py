from numpy import array
from time import time

with open("09.txt", "r") as f:
    input = f.read()

start = time()


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


directions = {
    "R": array([1, 0]),
    "L": array([-1, 0]),
    "U": array([0, 1]),
    "D": array([0, -1]),
}
input = [(directions[line[0]], int(line[2:])) for line in input.splitlines()]

knots = [array([0, 0]) for _ in range(10)]
visited = set()
visited.add(tuple(knots[-1]))

for d, n in input:
    for _ in range(n):
        knots[0] += d
        for i in range(1, len(knots)):
            if all(abs(knots[i - 1] - knots[i]) <= 1):
                break

            diff = knots[i - 1] - knots[i]
            diff = array(list(map(sign, diff)))
            knots[i] += diff
        visited.add(tuple(knots[-1]))

print(len(visited))
print(f"Time taken: {time() - start}s")
