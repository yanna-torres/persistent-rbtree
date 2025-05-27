from tree.red_black_tree import RedBlackTree


if __name__ == "__main__":
    tree = RedBlackTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    tree.insert(50)
    tree.insert(25)

    print("Inorder traversal of the Red-Black Tree:")
    tree._inorder_traversal(tree.root)
    print()

    tree.delete(20)

    print("Inorder traversal of the Red-Black Tree after deleting 20")
    tree._inorder_traversal(tree.root)
    print()
