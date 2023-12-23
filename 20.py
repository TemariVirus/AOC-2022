from time import time

with open("20.txt", "r") as f:
    input = f.read()

start = time()


class LinkedList:
    def __init__(self, values):
        self.head = LinkedListNode(values[0])
        self.head.next = self.head
        self.head.prev = self.head
        for value in values[1:]:
            node = LinkedListNode(value, self.head, self.head.prev)
            self.head.prev.next = node
            self.head.prev = node

    def to_list(self):
        node = self.head
        values = [node.value]
        while node.next != self.head:
            node = node.next
            values.append(node.value)
        return values

    def find(self, value):
        node = self.head
        while node.value != value and node.next != self.head:
            node = node.next
        return None if node.value != value else node

    def mix(self, count):
        node = self.head
        nodes = [node]
        while node.next != self.head:
            node = node.next
            nodes.append(node)

        length = len(nodes) - 1
        for _ in range(count):
            for node in nodes:
                if node.value == 0:
                    continue

                value = node.value % length
                node.remove(self)
                n = node
                for _ in range(value):
                    n = n.next
                n.insert_after(node)

    def __getitem__(self, index):
        node = self.head
        for _ in range(index):
            node = node.next
        return node.value

    def __repr__(self):
        return str(self.to_list())


class LinkedListNode:
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev

    def remove(self, list):
        self.prev.next = self.next
        self.next.prev = self.prev
        if self == list.head:
            list.head = self.next

    def insert_after(self, node):
        node.next = self.next
        node.prev = self
        self.next.prev = node
        self.next = node

    def __getitem__(self, index):
        node = self
        for _ in range(index):
            node = node.next
        return node.value

    def __repr__(self):
        return f"{self.prev.value} <- {self.value} -> {self.next.value}"


input = LinkedList(list(map(lambda x: int(x) * 811589153, input.splitlines())))
input.mix(10)
head = input.find(0)
print(head[1000] + head[2000] + head[3000])
print(f"Time taken: {time() - start}s")
