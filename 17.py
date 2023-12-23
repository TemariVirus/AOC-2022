from copy import deepcopy
from functools import reduce
from time import time
from typing import TypeVar, Iterable, Iterator

T = TypeVar("T")

rocks = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""
with open("17.txt", "r") as f:
    jets = f.read()


def index_or_default(array: list[T], obj: T, default: T = None) -> int:
    try:
        return array.index(obj)
    except ValueError:
        return default


class Chamber:
    def __init__(self, width: int) -> None:
        self.width = width
        self.mask = 0
        self.heights = [0] * width
        self.height_offset = 0

    def height(self) -> int:
        return self.height_offset + max(self.heights)

    def __repr__(self) -> str:
        result = bin(self.mask)[2:][::-1]
        split = len(result) // self.width * self.width
        truncated = [result[i : i + self.width] for i in range(0, split, self.width)][
            ::-1
        ]
        if len(result) > split:
            truncated = [
                "".join(
                    [
                        "0" if i >= len(result) else result[i]
                        for i in range(split, split + self.width)
                    ]
                )
            ] + truncated
        return (
            "\n".join(map(lambda x: x[::-1], truncated))
            .replace("0", ".")
            .replace("1", "#")
        )


class Rock:
    # Min x is always 0
    def __init__(self, mask: int, max_x: int, heights: tuple[int]) -> None:
        self.mask = mask
        self.max_x = max_x
        self.heights = heights

        self.x = 0
        self.y = 0

    def spawn(self, chamber: Chamber) -> None:
        self.x = self.max_x - 2
        self.y = max(chamber.heights) + 3

    def blow(self, chamber: Chamber, direction: str) -> None:
        mask = self.get_mask(chamber)
        if direction == ">":
            if chamber.mask & (mask >> 1) != 0:
                return
            self.x = max(0, self.x - 1)
        else:
            if chamber.mask & (mask << 1) != 0:
                return
            self.x = min(self.max_x, self.x + 1)

    def move_down(self, chamber: Chamber) -> bool:
        mask = self.get_mask(chamber)
        if (mask >> chamber.width) & chamber.mask or self.y <= 0:
            chamber.mask |= mask

            for i in range(self.x, self.x + len(self.heights)):
                chamber.heights[i] = max(
                    chamber.heights[i], self.y + self.heights[i - self.x]
                )

            floor = min(chamber.heights)
            if floor > 0:
                chamber.height_offset += floor
                chamber.heights = list(map(lambda h: h - floor, chamber.heights))
                chamber.mask >>= floor * chamber.width

            return True

        self.y -= 1
        return False

    def get_mask(self, chamber: Chamber) -> int:
        pos = self.y * chamber.width + self.x
        return self.mask << pos

    def __repr__(self) -> str:
        return f"Rock(x: {self.x}, y: {self.y}, mask: {bin(self.mask)[2:]}, max_x: {self.max_x}, height: {self.heights})"


class RockBag:
    def __init__(self, rocks: list[list[str]], chamber: Chamber) -> None:
        self.bag: list[Rock] = []
        for rock in rocks:
            # Convert to binary and parse each layer
            mask = [int(layer.replace(".", "0").replace("#", "1"), 2) for layer in rock]
            rock_width = max(m.bit_length() for m in mask)
            max_x = chamber.width - rock_width
            heights = tuple(
                map(
                    lambda column: len(mask)
                    - index_or_default(
                        [(m & column) == 0 for m in mask], False, default=-1
                    ),
                    [1 << i for i in range(rock_width)],
                )
            )
            mask = reduce(lambda cur, next: (cur << chamber.width) | next, mask)
            self.bag.append(Rock(mask, max_x, heights))

    def __iter__(self):
        return self.bag.__iter__()


def loop_forever(obj: Iterable[T]) -> Iterator[T]:
    while True:
        for item in deepcopy(obj):
            yield deepcopy(item)


start = time()

GAME_LENGTH = 1_000_000_000_000
# GAME_LENGTH = 2022
chamber = Chamber(7)
rocks = rocks.split("\n\n")
rocks = RockBag([r.splitlines() for r in rocks], chamber)
jets = loop_forever(enumerate(jets))

count = 0
seen: dict[tuple[int, int, int], tuple[int, int]] = dict()
for i, rock in loop_forever(enumerate(rocks)):
    if count >= GAME_LENGTH:
        print(f"{chamber.height()} units tall")
        break

    # prev = str(chamber)
    old_offset = chamber.height_offset

    rock.spawn(chamber)
    for j, jet in jets:
        rock.blow(chamber, jet)
        if rock.move_down(chamber):
            break
    count += 1

    key = (chamber.mask, i, j)
    if key not in seen:
        seen[key] = (chamber.height(), count)
    else:
        prev_height, prev_count = seen[key]
        cycle_length = count - prev_count
        cycles = (GAME_LENGTH - count) // cycle_length
        if cycles <= 0:
            continue
        # Jump ahead cycle times
        chamber.height_offset += cycles * (chamber.height() - prev_height)
        count += cycles * cycle_length

    # region Debug
    # curr = str(chamber)
    # if chamber.height_offset > old_offset:
    #     prev = prev[: (old_offset - chamber.height_offset) * (chamber.width + 1)]
    # prev = (
    #     "".join(
    #         ["." * chamber.width + "\n"]
    #         * ((len(curr) - len(prev) + 1) // (chamber.width + 1))
    #     )
    #     + prev
    # )
    # curr, prev = list(curr), list(prev)
    # for i in range(len(curr)):
    #     if curr[i] != prev[i]:
    #         curr[i] = "@"
    # print(count, chamber.height())
    # print("".join(curr)[: 8 * 35])
    # input()
    # endregion

print(f"Time taken: {time() - start}s")
