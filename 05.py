from time import time

with open("05.txt", "r") as f:
    input = f.read()

start = time()

temp1, temp2 = input.split("\n\n")
temp1 = temp1.splitlines()[-2::-1]
temp2 = temp2.splitlines()
crates = [list() for _ in range((len(temp1[0]) + 1) // 4)]
for line in temp1:
    for i in range(1, len(line), 4):
        if line[i] == " ":
            continue
        crates[i // 4].append(line[i])
for line in temp2:
    c, f, t = map(int, line.split(" ")[1::2])
    crates[t - 1].extend(crates[f - 1][-c:])
    crates[f - 1] = crates[f - 1][:-c]
print("".join(map(lambda x: x[-1], crates)))
print(f"Time taken: {time() - start}s")
