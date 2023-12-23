from time import time

with open("23.txt", "r") as f:
    input = f.read()

start = time()


class CycleList:
    def __init__(self, list) -> None:
        node = CycleListNode(list[0])
        self.head = node
        curr = self.head
        for item in list[1:]:
            node = CycleListNode(item)
            curr.next = node
            curr = node
        else:
            self.tail = node

    def cycle_next(self) -> None:
        self.tail.next = self.head
        self.tail = self.head

        next = self.head.next
        self.head.next = None
        self.head = next

    def __iter__(self):
        curr = self.head
        while curr is not None:
            yield curr.value
            curr = curr.next

    def __repr__(self) -> str:
        return "[" + ", ".join(map(str, self)) + "]"


class CycleListNode:
    def __init__(self, value) -> None:
        self.value = value
        self.next = None


def add(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return (a[0] + b[0], a[1] + b[1])


def play_round(elves: set[tuple[int]], directions: CycleList) -> bool:
    moves: dict[tuple[int], tuple[int] | None] = dict()
    for elf in elves:
        skip = True
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                point = add((x, y), elf)
                if point in elves:
                    skip = False
                    break
            if not skip:
                break
        if skip:
            continue

        for d, checks in directions:
            d = add(d, elf)
            for check in checks:
                if add(elf, check) in elves:
                    break
            else:
                if d in moves:
                    moves[d] = None
                else:
                    moves[d] = elf
                break

    moved = False
    for move, elf in moves.items():
        if elf is not None:
            elves.remove(elf)
            elves.add(move)
            moved = True
    directions.cycle_next()

    return moved


def print_board(elves: set[tuple[int]]) -> None:
    min_x, max_x = min(map(lambda x: x[0], elves)), max(map(lambda x: x[0], elves))
    min_y, max_y = min(map(lambda x: x[1], elves)), max(map(lambda x: x[1], elves))
    width, height = max_x - min_x + 1, max_y - min_y + 1
    board = [["." for _ in range(width)] for _1 in range(height)]
    for x, y in elves:
        board[y - min_y][x - min_x] = "#"

    for row in board:
        print("".join(row))


elves = set(
    (x, y)
    for y, line in enumerate(input.splitlines())
    for x, char in enumerate(line)
    if char == "#"
)
directions = CycleList(
    [
        ((0, -1), ((-1, -1), (0, -1), (1, -1))),
        ((0, 1), ((-1, 1), (0, 1), (1, 1))),
        ((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),
        ((1, 0), ((1, -1), (1, 0), (1, 1))),
    ]
)

round = 1
while play_round(elves, directions):
    round += 1
print(round)

print(f"Time taken: {time() - start}s")
