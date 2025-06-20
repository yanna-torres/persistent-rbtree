from tree.node import RBNode


class RedBlackTree:
    # constructor to initialize the RB tree
    def __init__(self):
        self.root = None

    # function to search a value in RB Tree
    def search(self, value):
        curr_node = self.root
        while curr_node is not None:
            if value == curr_node.value:
                return curr_node
            elif value < curr_node.value:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None

    # function to insert a node in RB Tree, similar to BST insertion
    def insert(self, value):
        # Regular insertion
        new_node = RBNode(value)
        if self.root is None:
            self.root = new_node
        else:
            curr_node = self.root
            while True:
                if value < curr_node.value:
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left
                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        self.insert_fix(new_node)

    # Function to fix RB tree properties after insertion
    def insert_fix(self, new_node):
        while new_node.parent and new_node.parent.color == "red":
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == "red":
                    new_node.parent.color = "black"
                    uncle.color = "black"
                    new_node.grandparent().color = "red"
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = "black"
                    new_node.grandparent().color = "red"
                    self.rotate_right(new_node.grandparent())
            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == "red":
                    new_node.parent.color = "black"
                    uncle.color = "black"
                    new_node.grandparent().color = "red"
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = "black"
                    new_node.grandparent().color = "red"
                    self.rotate_left(new_node.grandparent())
        self.root.color = "black"

    # function to delete a value from RB Tree
    def delete(self, value):
        node_to_remove = self.search(value)
        if node_to_remove is None:
            return

        y = node_to_remove
        y_original_color = y.color

        if node_to_remove.left is None:
            x = node_to_remove.right
            self._replace_node(node_to_remove, node_to_remove.right)
        elif node_to_remove.right is None:
            x = node_to_remove.left
            self._replace_node(node_to_remove, node_to_remove.left)
        else:
            y = self._find_min(node_to_remove.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node_to_remove:
                if x:
                    x.parent = y
            else:
                self._replace_node(y, y.right)
                y.right = node_to_remove.right
                if y.right:
                    y.right.parent = y
            self._replace_node(node_to_remove, y)
            y.left = node_to_remove.left
            if y.left:
                y.left.parent = y
            y.color = node_to_remove.color

        if y_original_color == "black":
            self.delete_fix(x)


    # function to fix RB Tree properties after deletion
    def delete_fix(self, x):
        if x is None:
            return
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                sibling = x.sibling()
                if sibling.color == "red":
                    sibling.color = "black"
                    x.parent.color = "red"
                    self.rotate_left(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == "black") and (
                    sibling.right is None or sibling.right.color == "black"
                ):
                    sibling.color = "red"
                    x = x.parent
                else:
                    if sibling.right is None or sibling.right.color == "black":
                        sibling.left.color = "black"
                        sibling.color = "red"
                        self.rotate_right(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = "black"
                    if sibling.right:
                        sibling.right.color = "black"
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                sibling = x.sibling()
                if sibling.color == "red":
                    sibling.color = "black"
                    x.parent.color = "red"
                    self.rotate_right(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == "black") and (
                    sibling.right is None or sibling.right.color == "black"
                ):
                    sibling.color = "red"
                    x = x.parent
                else:
                    if sibling.left is None or sibling.left.color == "black":
                        sibling.right.color = "black"
                        sibling.color = "red"
                        self.rotate_left(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = "black"
                    if sibling.left:
                        sibling.left.color = "black"
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = "black"

    # Function for left rotation of RB Tree
    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    # function for right rotation of RB Tree
    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    # function to replace an old node with a new node
    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    # function to find node with minimum value in a subtree
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node
