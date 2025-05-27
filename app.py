from tree.persistent import PersistentRedBlackTree

if __name__ == "__main__":
    tree = PersistentRedBlackTree()

    tree.insert(10)   # versão 1
    tree.insert(20)   # versão 2
    tree.delete(10)   # versão 3 (deletando 10)
    tree.insert(30)   # versão 3
    tree.insert(40)   # versão 4
    tree.insert(50)   # versão 5
    tree.insert(25)   # versão 6
    
    print("Versão 1 (após incluir 10):")
    print(" ".join(tree.print_version(1)))
    
    print("Versão 2 (após incluir 20):")
    print(" ".join(tree.print_version(2)))
    
    print("Versão 3 (após deletar 10 e incluir 30):")
    print(" ".join(tree.print_version(3)))

    print("Versão 6:")
    print(" ".join(tree.print_version(6)))

    tree.delete(20)   # versão 7

    print("\nVersão 7 (após deletar 20):")
    print(" ".join(tree.print_version(7)))

    print("\nVersão 2 (antes de deletar 20):")
    print(" ".join(tree.print_version(2)))

    print("\nSucessor de 25 na versão 6:")
    print(tree.successor(25, 6))

    print("\nSucessor de 50 na versão 7 (não existe):")
    print(tree.successor(50, 7))
