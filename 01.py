from time import time

with open("01.txt", "r") as f:
    input = f.read()

start = time()


input = input.split("\n\n")
input = [sum(map(int, i.splitlines())) for i in input]
input.sort(reverse=True)
print(input[0] + input[1] + input[2])
print(f"Time taken: {time() - start}s")
