from time import time
import re

start = time()

with open("15.txt", "r") as f:
    input = f.read()
MIN_X = 0
MAX_X = 4_000_000


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_exclude_x_range(
    sensor: tuple[int, int], beacon_dist: int, y: int
) -> tuple[int, int] | None:
    x_radius = beacon_dist - abs(sensor[1] - y)
    return (sensor[0] - x_radius, sensor[0] + x_radius) if x_radius >= 0 else None


sensors = []
beacons = set()
distances = []
line_pattern = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)
for line in input.splitlines():
    sx, sy, bx, by = line_pattern.match(line).groups()
    sensors.append((int(sx), int(sy)))
    beacons.add((int(bx), int(by)))
    distances.append(manhattan_distance((int(sx), int(sy)), (int(bx), int(by))))
beacons = list(beacons)


def search_row(y: int) -> int | None:
    # Get ranges of x values where there cannot be a beacon
    ranges = [get_exclude_x_range(s, d, y) for s, d in zip(sensors, distances)]
    ranges = list(filter(lambda r: r, ranges))
    # Add ranges for beacons
    ranges.extend([(pos[0], pos[0]) for pos in beacons if pos[1] == y])
    # Combine overlapping or adjacent ranges
    ranges.sort(key=lambda r: r[0])
    i = 0
    while i < len(ranges) - 1:
        left, right = ranges[i], ranges[i + 1]
        if left[1] + 1 >= right[0]:
            ranges[i] = (left[0], max(left[1], right[1]))
            del ranges[i + 1]
        else:
            i += 1

    if len(ranges) > 1:
        return ranges[0][1] + 1
    if len(ranges) == 1:
        if ranges[0][0] > MIN_X:
            return ranges[0][0] - 1
        elif ranges[0][1] < MAX_X:
            return ranges[0][1] + 1
        else:
            return None
    raise ValueError("No ranges found")


MIN_Y = 0
MAX_Y = 4000000
for y in range(MIN_Y, MAX_Y + 1):
    x = search_row(y)
    if x:
        print(x * 4000000 + y)
        break

print(f"Time taken: {time() - start}s")
