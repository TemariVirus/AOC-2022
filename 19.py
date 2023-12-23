from re import match
from time import time

with open("19.txt", "r") as f:
    input = f.read()

start = time()


class BluePrint:
    def __init__(self, str: str) -> None:
        (
            self.id,
            self.ore_ore,
            self.clay_ore,
            self.obsidian_ore,
            self.obsidian_clay,
            self.geode_ore,
            self.geode_obsidian,
        ) = tuple(
            map(
                int,
                match(
                    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
                    str,
                ).groups(),
            )
        )
        self.max_ore = max(
            self.ore_ore, self.clay_ore, self.obsidian_ore, self.geode_ore
        )
        self.max_clay = self.obsidian_clay
        self.max_obsidian = self.geode_obsidian

    def max_geodes(
        self,
        time_left: int,
        robots: tuple[int, int, int, int] = (1, 0, 0, 0),
        res: tuple[int, int, int, int] = (0, 0, 0, 0),
        seen: dict[
            tuple[tuple[int, int, int, int], tuple[int, int, int, int]], int
        ] = {},
        can_make: tuple[bool, bool, bool, bool] = (False, False, False, False),
        max_found: int = 0,
    ) -> int:
        if time_left == 1:
            max_found = max(max_found, res[3] + robots[3])
            return res[3] + robots[3]

        estimate = res[3]
        estimate += (robots[3] * 2 + time_left - 1) * time_left // 2
        if estimate <= max_found:
            return 0

        result = seen.get((robots, res))
        if result is not None:
            if result >= time_left:
                return 0

        result = 0
        (can_make_ore, can_make_clay, can_make_obsidian, can_make_geode) = (
            False,
            False,
            False,
            False,
        )
        # Geode robot
        if (
            not can_make[3]
            and res[0] >= self.geode_ore
            and res[2] >= self.geode_obsidian
        ):
            can_make_geode = True
            new_res = (
                res[0] - self.geode_ore,
                res[1],
                res[2] - self.geode_obsidian,
                res[3],
            )
            new_res = tuple(map(sum, zip(new_res, robots)))
            new_robots = (robots[0], robots[1], robots[2], robots[3] + 1)
            result = max(
                result,
                self.max_geodes(
                    time_left - 1, new_robots, new_res, seen, max_found=max_found
                ),
            )
        # Obsidian robot
        if (
            not can_make[2]
            and res[0] >= self.obsidian_ore
            and res[1] >= self.obsidian_clay
        ):
            can_make_obsidian = True
            if self.max_obsidian > robots[2]:
                new_res = (
                    res[0] - self.obsidian_ore,
                    res[1] - self.obsidian_clay,
                    res[2],
                    res[3],
                )
                new_res = tuple(map(sum, zip(new_res, robots)))
                new_robots = (robots[0], robots[1], robots[2] + 1, robots[3])
                result = max(
                    result,
                    self.max_geodes(
                        time_left - 1, new_robots, new_res, seen, max_found=max_found
                    ),
                )
        # Clay robot
        if not can_make[1] and res[0] >= self.clay_ore:
            can_make_clay = True
            if self.max_clay > robots[1]:
                new_res = (res[0] - self.clay_ore, res[1], res[2], res[3])
                new_res = tuple(map(sum, zip(new_res, robots)))
                new_robots = (robots[0], robots[1] + 1, robots[2], robots[3])
                result = max(
                    result,
                    self.max_geodes(
                        time_left - 1, new_robots, new_res, seen, max_found=max_found
                    ),
                )
        # Ore robot
        if not can_make[0] and res[0] >= self.ore_ore:
            can_make_ore = True
            if self.max_ore > robots[0]:
                new_res = (res[0] - self.ore_ore, res[1], res[2], res[3])
                new_res = tuple(map(sum, zip(new_res, robots)))
                new_robots = (robots[0] + 1, robots[1], robots[2], robots[3])
                result = max(
                    result,
                    self.max_geodes(
                        time_left - 1, new_robots, new_res, seen, max_found=max_found
                    ),
                )
        # No robot
        new_res = tuple(map(sum, zip(res, robots)))
        result = max(
            result,
            self.max_geodes(
                time_left - 1,
                robots,
                new_res,
                seen,
                (can_make_ore, can_make_clay, can_make_obsidian, can_make_geode),
                max_found=max_found,
            ),
        )

        seen[(robots, res)] = time_left
        max_found = max(max_found, result)
        return result


blueprints = [BluePrint(str) for str in input.splitlines()]
answer = [b.max_geodes(32, seen={}) for b in blueprints]
print(answer)
print(answer[0] * answer[1] * answer[2])
print(f"Time taken: {time() - start}s")
