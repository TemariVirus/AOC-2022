from re import match
from time import time

with open("04.txt", "r") as f:
    input = f.read()

start = time()


def check_overlap(a: int, b: int, c: int, d: int) -> bool:
    return (a <= c <= b) or (a <= d <= b) or (c <= a <= d) or (c <= b <= d)


input = [
    tuple(map(int, match(r"(\d+)-(\d+),(\d+)-(\d+)", line).groups()))
    for line in input.splitlines()
]
print(sum(check_overlap(*x) for x in input))
print(f"Time taken: {time() - start}s")
