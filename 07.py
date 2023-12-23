from time import time

with open("07.txt", "r") as f:
    input = f.read()

start = time()


def get_size(dir: str, dirs: dict) -> int:
    size = 0
    for item in dirs[dir]:
        if isinstance(item, tuple):
            size += int(item[1])
        else:
            size += get_size(dir + "/" + item, dirs)
    return size


dirs = {}
current_dir = "/"
for line in input.splitlines():
    if line.startswith("$ cd "):
        line = line[5:]
        if line == "..":
            current_dir = "/".join(current_dir.split("/")[:-1])
        elif line == "/":
            current_dir = "/"
        else:
            current_dir += "/" + line
        if current_dir not in dirs:
            dirs[current_dir] = set()
    elif line.startswith("$ ls"):
        continue
    elif line.startswith("dir "):
        dirs[current_dir].add(line[4:])
    else:
        size, name = line.split(" ", 1)
        dirs[current_dir].add((name, size))
SPACE_USED = get_size("/", dirs)
SPACE_NEEDED = 30000000 - (70000000 - SPACE_USED)
sizes = [get_size(dir, dirs) for dir in dirs]
sizes.sort()
print(filter(lambda x: x >= SPACE_NEEDED, sizes).__next__())
print(f"Time taken: {time() - start}s")
