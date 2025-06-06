from copy import deepcopy
from tree.red_black_tree import RedBlackTree


class PersistentRedBlackTree:
    def __init__(self):
        self.versions = [None] * 100
        self.current_version = 0
        self.tree = RedBlackTree()
        self.versions[0] = None

    def insert(self, value):
        self.tree.root = deepcopy(self.versions[self.current_version])
        self.tree.insert(value)
        self.current_version += 1
        self.versions[self.current_version] = self.tree.root

    def delete(self, value):
        self.tree.root = deepcopy(self.versions[self.current_version])
        self.tree.delete(value)
        self.current_version += 1
        self.versions[self.current_version] = self.tree.root

    def successor(self, x, version):
        if version > self.current_version:
            version = self.current_version

        node = self.versions[version]
        succ = None

        while node:
            if node.value > x:
                succ = node
                node = node.left
            else:
                node = node.right

        return succ.value if succ else float("inf")

    def print_version(self, version):
        if version > self.current_version:
            version = self.current_version

        root = self.versions[version]
        result = []

        def in_order(node, depth=0):
            if node:
                in_order(node.left, depth + 1)
                color = "R" if node.color == "red" else "N"
                result.append(f"{node.value},{depth},{color}")
                in_order(node.right, depth + 1)

        in_order(root)
        return result
