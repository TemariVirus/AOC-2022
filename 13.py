from functools import cmp_to_key
from time import time

start = time()

with open("13.txt", "r") as f:
    input = f.read()

input = [eval(line) for line in input.replace("\n\n", "\n").splitlines()]
input.append([[2]])
input.append([[6]])


def compare(l_packet, r_packet, default=0) -> int:
    for i in range(min(len(l_packet), len(r_packet))):
        left, right = l_packet[i], r_packet[i]
        if type(left) is list or type(right) is list:
            left = left if type(left) is list else [left]
            right = right if type(right) is list else [right]

            result = compare(left, right)
            if result != 0:
                return result
        else:
            if left < right:
                return -1
            elif left > right:
                return 1

    if len(l_packet) < len(r_packet):
        return -1
    elif len(l_packet) > len(r_packet):
        return 1

    return default


input.sort(key=cmp_to_key(lambda l, r: compare(l, r, default=-1)))
print(input.index([[2]]))
print(input.index([[6]]))
print(f"Time taken: {time() - start}s")
