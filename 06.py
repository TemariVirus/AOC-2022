from time import time

with open("06.txt", "r") as f:
    input = f.read()

start = time()

distinct = dict()
for i in range(len(input)):
    if input[i] in distinct:
        distinct = {k: v for k, v in distinct.items() if v >= distinct[input[i]]}
    distinct[input[i]] = i
    if len(distinct) == 14:
        print(i + 1)
        break
print(f"Time taken: {time() - start}s")
