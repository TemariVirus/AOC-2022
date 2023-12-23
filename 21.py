from time import time
from queue import Queue

with open("21.txt", "r") as f:
    input = f.read()

start = time()


class Monkey:
    def __init__(self, line: str) -> None:
        (self.name, value) = line.split(": ")
        if value.isnumeric():
            self.value = int(value)
            return

        (self.left, op, self.right) = value.split(" ")
        self.op = {
            "+": int.__add__,
            "-": int.__sub__,
            "*": int.__mul__,
            "/": int.__floordiv__,
        }[op]

    def get_value(self, monkeys: dict[str, "Monkey"]) -> int:
        if hasattr(self, "value"):
            return self.value

        self.value = self.op(
            monkeys[self.left].get_value(monkeys),
            monkeys[self.right].get_value(monkeys),
        )
        return self.value

    def is_on_left(self, target: str, monkeys: dict[str, "Monkey"]) -> bool:
        queue = Queue()
        queue.put((self.left, True))
        queue.put((self.right, False))
        while not queue.empty():
            (name, is_left) = queue.get()
            if name == target:
                return is_left

            monkey = monkeys[name]
            if hasattr(monkey, "value"):
                continue

            queue.put((monkey.left, is_left))
            queue.put((monkey.right, is_left))

        raise ValueError(f"Could not find {target} in {self.name}")

    def get_required_value(self, monkeys: dict[str, "Monkey"]) -> int:
        root = monkeys["root"]
        is_left = root.is_on_left(self.name, monkeys)
        target = monkeys[root.right if is_left else root.left].get_value(monkeys)
        pivot = monkeys[root.left if is_left else root.right]
        while True:
            is_left = pivot.is_on_left(self.name, monkeys)
            other = monkeys[pivot.right if is_left else pivot.left].get_value(monkeys)
            match pivot.op:
                case int.__add__:
                    target -= other
                case int.__sub__:
                    if is_left:
                        target += other
                    else:
                        target = other - target
                case int.__mul__:
                    target //= other
                case int.__floordiv__:
                    if is_left:
                        target *= other
                    else:
                        target = other // target

            pivot = monkeys[pivot.left if is_left else pivot.right]
            if pivot.name == self.name:
                return target

    def __repr__(self) -> str:
        if hasattr(self, "value"):
            return f"{self.name}: {self.value}"

        return f"{self.name}: {self.left} {self.op.__name__} {self.right}"


# Part 1
monkeys = {line[:4]: Monkey(line) for line in input.splitlines()}
print(monkeys["root"].get_value(monkeys))

# Part 2
monkeys = {line[:4]: Monkey(line) for line in input.splitlines()}
print(monkeys["humn"].get_required_value(monkeys))

print(f"Time taken: {time() - start}s")
