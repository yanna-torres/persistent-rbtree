from copy import deepcopy

from tree.red_black_tree import RedBlackTree


class PersistentRedBlackTree:
    def __init__(self):
        self.versions = [None] * 100
        self.current_version = 0
        self.tree = RedBlackTree()
        self.versions[0] = None

    def insert(self, value):
        # Deep copy the tree from current root
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

        print(f"SUC {x} {version}")
        print(succ.value if succ else float("inf"))
        print("")
        return succ.value if succ else float("inf")

    def print_version(self, version):
        if version > self.current_version:
            version = self.current_version

        root = self.versions[version]
        lines = []

        def _display(node, prefix="", is_left=True):
            if node is not None:
                color = "R" if node.color == "red" else "N"
                lines.append(
                    f"{prefix}{'└── ' if is_left else '┌── '}{node.value}({color})"
                )
                if node.left or node.right:
                    if node.right:
                        _display(
                            node.right, prefix + ("    " if is_left else "│   "), False
                        )
                    if node.left:
                        _display(
                            node.left, prefix + ("    " if is_left else "│   "), True
                        )
            else:
                lines.append(f"{prefix}{'└── ' if is_left else '┌── '}None")

        _display(root)
        return "\n".join(lines)
