from functools import reduce
from time import time

with open("03.txt", "r") as f:
    input = f.read()

start = time()


def get_priority(s: str) -> int:
    return (
        ord(s) - ord("a") + 1
        if ord("a") <= ord(s) <= ord("z")
        else ord(s) - ord("A") + 27
    )


input = [set(line) for line in input.splitlines()]
print(
    sum(
        map(
            get_priority,
            (
                reduce(set.intersection, input[i : i + 3]).pop()
                for i in range(0, len(input), 3)
            ),
        )
    )
)
print(f"Time taken: {time() - start}s")
