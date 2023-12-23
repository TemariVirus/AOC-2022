from time import time

with open("02.txt", "r") as f:
    input = f.read()

start = time()

dict1 = {"A": 1, "B": 2, "C": 3}
dict2 = {"X": -1, "Y": 0, "Z": 1}
input = [(dict1[line[0]], dict2[line[2]]) for line in input.splitlines()]
print(sum(((a + x - 1) % 3) + 1 + (x * 3) + 3 for a, x in input))
print(f"Time taken: {time() - start}s")
