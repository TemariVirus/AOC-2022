from time import time
from typing import Callable

start = time()

with open("11.txt", "r") as f:
    input = f.read()


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: Callable[[int], int],
        test: Callable[[int], bool],
        true_monkey: int,
        false_monkey: int,
    ):
        self.items = items
        self.operation = operation
        self.test = test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspect_count = 0

    def process_turn(self, monkeys: list["Monkey"]) -> None:
        for item in self.items:
            # item = self.operation(item) // 3
            item = self.operation(item) % 9_699_690
            self.inspect_count += 1
            monkeys[
                self.true_monkey if self.test(item) else self.false_monkey
            ].items.append(item)
        self.items = []

    def __repr__(self) -> str:
        return f"Monkey(items={self.items}, operation={self.operation}, test={self.test}, true_monkey={self.true_monkey}, false_monkey={self.false_monkey}, inspect_count={self.inspect_count})"


def str_to_monkey(str: str) -> Monkey:
    lines = str.splitlines()
    items = [int(i) for i in lines[1].split(": ")[1].split(", ")]
    operation = eval("lambda old: " + lines[2].split("new = ")[1])
    test = eval("lambda old: old % " + lines[3].split("divisible by ")[1] + " == 0")
    true_monkey = int(lines[4].split("throw to monkey ")[1])
    false_monkey = int(lines[5].split("throw to monkey ")[1])
    return Monkey(items, operation, test, true_monkey, false_monkey)


monkeys = [str_to_monkey(x) for x in input.split("\n\n")]
for _ in range(10000):
    for monkey in monkeys:
        monkey.process_turn(monkeys)
print([x.inspect_count for x in monkeys])
print(f"Time taken: {time() - start}s")
