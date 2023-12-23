from time import time

start = time()

with open("10.txt", "r") as f:
    input = f.read()


def print_pixel():
    global counter

    print(
        "#" if abs(x - (counter % 40)) <= 1 else ".",
        end="\n" if counter % 40 == 0 else "",
    )
    counter += 1


input = input.splitlines()
counter = 1
x = 1
for line in input:
    if line == "noop":
        print_pixel()

    else:
        print_pixel()
        x += int(line[4:])
        print_pixel()

print(f"Time taken: {time() - start}s")
