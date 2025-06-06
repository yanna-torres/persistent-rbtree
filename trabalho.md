Árvore Rubro negra (red_black_tree):
Essa parte do código Implementa a árvore rubro negra e suas operações (busca, inserção, remoção, balanceamento, mínimo e print)

Implementa árvore rubro negra:
-Cria classe RedBlackTree
-Cria raiz da árvore que começa vazia

Código:
class RedBlackTree:
    def __init__(self):
        self.root = None


Operação de busca:
-Define busca "search" que recebe valor "value".
-Busca a partir da raiz da árvore.
-Enquanto o nó atual não for nulo: 
    -se o valor for igual ao valor do nó atual, retornar nó atual
    -se o valor não for igual e se for menor que o valor do nó atual, continuar busca para esquerda
    -senão, continuar para direita
-Retorna nulo caso não encontre o valor

Código:
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
    

Operação de inserção:
-Define função "insert" que insere valor "value".
-Cria novo nó.
-Se a árvore estiver vazia, o novo nó se torna a raiz da árvore
-Senão, percorrer árvore a partir da raiz com o laço "while true", até encontrar o lugar do novo nó
    -se o valor for menor que o valor do nó atual, nó tem que ir para a esquerda
        -se o filho esquerdo estiver vazio, o novo nó é inserido ali e define o pai
        -senão, continuar descendo para esquerda
    -senão (se o valor for igual ou maior que o valor do nó atual), vai para a direita
        -se filho direito estiver vazio, o novo nó é inserido ali e define o pai 
        -senão, continua descendo para a direita
-Chama função para corrigir a árvore

Código:
def insert(self, value):
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


Corrigir a árvore depois da inserção:
-Define função "insert_fix" que corrige nó "new_node"
-Percorre o laço enquanto nó pai e novo nó forem vermelhos (filhos de nós vermelhos têm que ser pretos)
    -Se pai do novo nó estiver a esquerda de nó avô, filho direito do nó avô é tio do novo nó
        -Se tio existir e for vermelho, pai e tio do novo nó passarão a ser pretos, avô será vermelho (para manter o número de nós pretos) e a verificação passa para o avô.
        -Senão (tio é nulo ou preto)
            -se novo nó estiver à direita de nó pai, fazer rotação para ficar à esquerda do pai (para ficar em linha reta)
            -com tudo alinhado, pai vira preto, avô vira vermelho e faz rotação para a direita
    -Senão (um espelho do caso anterior: pai à direira e tio à esquerda)
        -Se tio for vermelho, pai e tio viram pretos, avô vira vermelho e a verificação sobe para o avô
        -Senão
            -se novo nó estiver à esquerda, fazer rotação para direita
            =pai vira preto, avô vira vermelho e faz rotação para a esquerda
-Sai do laço e garante a raiz preta

Código:
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


Operação de Remoção:
-Define função "delete" que remove valor "value"
-Usa fução de busca para encontrar o valor do nó que será removido
    -Se não encontrar nada, retornar
-y é o nó que será removido
-Guarda a cor original de y (para não violar as regras da árvore)
-Se o nó que será removido não tiver filho a sua esquerda, armazenar filho direito e substuir nó por filho direito
-Senão, se o nó que será removido não tiver filho a sua direita, armazenar filho esquerdo e substituir nó por filho direito
-Senão (nó com filho direito e esquero), encontar sucessor y de nó que será removido (o menor nó da subárvore direita)
-Guarda cor original do sucessor 
-Torna x o filho direito do sucessor e vai assumir a antiga posição do y 
    -se pai de y for o nó que será removido, ele já está na posição correta
        -se x existir, tornar x filho de y
    -senão (y está mais em baixo na árvore), filho de y sobe para o lugar de y e ponteiro de y é ajustado
    -y substitui nó a ser removido e pai de nó a ser removido passa a apontar para y
    -y herda filho esquerdo de nó a ser removido
    -se filho esquerdo existe, ponteiro "parent" de filho esquerdo aponta para y
    -y herda cor de nó a ser removido
-Se o nó removido era preto, chamar função para corrigir a árvore

Código:
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


Corrigir a árvore após remoção:
-Definir função "delete_x" que corrige nó x
-Se x for nulo, retornar
-Percorre o laço enquanto x não for a raiz e a cor de x for preta
    -Se x for filho esquerdo de seu pai, o filho direito será irmão de x
        -se irmão de x for vermelho, colorir irmão de preto e pai de vermelho e fazer rotação de pai para a esquerda
        -se filho esquerdo do irmão for nulo ou preto e filho direito do irmão for nulo ou preto, colorir irmão de vermelho e subir a verificação para o pai
        -se não
            -se filho direito do irmão for nulo ou preto, filho esquerdo do irmão vira preto, irmão de x vira vermelho, ele também faz uma rotação para a direita e ajusta os ponteiros
            -irmão recebe a cor de pai de x
            -pai de x vira preto
            -se filho direito do irmão existir, colorir filho direito do irmão de preto
            -faz rotação à esquerda do pai de x 
            -x vira a raiz da árvore (sai do laço)
-Colore x de preto

Código:
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


Função de rotação para a esquerda:
-Define função "rotate_left" que faz a rotação de nó "node" para a esquerda
-Transforma filho direito de nó atual (right_child) em pai
-Filho esquerdo de right_child vira filho direito de nó atual
-Se filho esquerdo de right_child existir, seu ponteiro "parent" passa a apontar para nó atual
-Pai de nó atual vira pai de right_child também
-Se pai de nó atual for nulo (nó é a raiz), righ_child vira a raiz da árvore
-Senão, se o nó atual for filho esquerdo do seu pai, right_child vira filho esquerdo do pai do nó atual
-Senão (nó atual é filho direito), right_child vira filho direito do pai de nó atual
-Nó atual vira filho esquerdo de right_child
-Ponteiro "parent" de nó atual passa a apontat para right_child

Código:
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



Função de rotação para a direita (espelho da função anterior):
-Define função "rotate_right" que faz a rotação de nó "node" para a direita
-Transforma filho esquerdo de nó atual (left_child) em pai
-Filho direito de left_child vira filho esquerdo de nó atual
-Se filho direito de left_child existir, seu ponteiro "parent" passa a apontar para nó atual
-Pai de nó atual vira pai de left_child também
-Se pai de nó atual for nulo (ou seja, nó atual é a raiz), left_child vira a raiz da árvore
-Senão, se nó atual for filho direito de seu pai, left_child vira filho direito do pai de nó atual
-Senão (nó atual é filho esquerdo), left_child vira filho esquerdo do pai de nó atual
-Nó atual vira filho direito de left_child
-Ponteiro "parent" de nó atual passa a apontar para left child.

Código:
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

Função de substituição:
-Define a função "replace_node" que substitui um antigo nó "old_node" por um novo nó "new_node"
-Se pai do antigo nó for nulo (antigo nó é a raiz), novo nó vira a raiz da árvore
-Senão
    -Se antigo nó era filho esqerdo de seu pai, novo nó vira o filho esquerdo do pai do antigo nó
    -Senão (antigo nó era filho direito), novo nó vira filho direito do pai do antigo nó
-Se novo nó existir, ponteiro "parent" de novo nó passa a apontar para pai do antigo nó

Código:
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


Função para encontrar valor mínimo em uma subárvore:
-Define função "_find_min" que busca o menor valor da subárvore de nó "node"
-Enquanto filho esquerdo de nó existir, descer a busca para esse filho, até encontrar o menor valor (nó que está mais a esquerda e não tem filho)
-Sai do laço e retorna o menor valor

Código:
def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node


Funão que percorre os nós:
-Define função "_inorder_traversal" que percorre os nós em ordem crescente (de valor) a partir de nó "node"
-Se o nó atual existir, percorrer subárvore esquerda, imprime valor do nó e percorre a subárvore direita

Código:
def _inorder_traversal(self, node):
        if node is not None:
            self._inorder_traversal(node.left)
            print(node.value, end=" ")
            self._inorder_traversal(node.right)


-


Persistência (persistent): 
Essa parte do código implementa percistência parcial na árvore rubro negra

Implementa percistência:
-Cria classe "PersistentRedBlackTree"
-Cria um array de 100 versões da árvore
-Define versão atual como 0
-Cria a nova instância da árvore RB
-Define versão 0 como vazia

Código:
class PersistentRedBlackTree:
    def __init__(self):
        self.versions = [None] * 100
        self.current_version = 0
        self.tree = RedBlackTree()
        self.versions[0] = None


Inserção: 
-Define função "insert" que insere valor "value" na árvore 
-Colona árvore atual (a nova raiz recebe uma cópia de todos os nós da versão atual)
-Insere valor na nova árvore
-Atualiza a contagem da versão atual
-Grava versão modificada que, agora, é a versão atual

Código:
def insert(self, value):
        self.tree.root = deepcopy(self.versions[self.current_version])
        self.tree.insert(value)
        self.current_version += 1
        self.versions[self.current_version] = self.tree.root


Remoção:
-Define função "delete" que remove valor "value"
-Colona árvore atual (a nova raiz recebe uma cópia de todos os nós da versão atual)
-Remove o valor da nova árvore
-Atualiza a contagem da versão atual
-Grava versão modificada que, agora, é a versão atual

Código:
def delete(self, value):
        self.tree.root = deepcopy(self.versions[self.current_version])
        self.tree.delete(value)
        self.current_version += 1
        self.versions[self.current_version] = self.tree.root


Sucessão:
-Define função "successor" que encontra sucessor de x na versão "version" da árvore
-Se o número da versão da busca for maior que o número da versão atual, a busca passa a ser na versão atual
-Node recebe a raiz dessa versão da árvore
-Sucessor começa vazio
-Entra no laço que faz a busca enquanto existir um nó
    -Se valor de nó atual for maior que x, nó atual se torna o melhor candidato a sucessor e a busca desce para o filho esquerdo (pode existir um nó com valor menor que nó atual, porém menor que x)
    -Senão (o valor de nó atual não é maior que x), descer a busca para a direita
-Imprime valor de x, a versão da árvore e o valor sucessor (se existir, senão imprime infinito)
-Retorna valor do sucessor, se ele existir, senão retorna infinito

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


Imprimir versão:
-Define função "print_version" que imprime versão "version"
-Se o número da versão escolhida for maior que o número da versão atual, versão atual passa a ser a versão escolhida
-Acessa raiz da versão escolhida
-Cria um array para impressão
-Define função interna "display"
    -Se nó existir, mostrar "R" para nós vermelhos e "N" para nós pretos
    -Cria formatação da árvore
        Filho direito será mostrado com prefixo "┌──" assim: ┌──20 (R)
        Filho esquerdo será mostrado com prefixo "└──" assim:└──10 (N)
    -Senão (nó não existe), imprime folha vazia
-Chama função display para mostrar a partir da raiz
-Retorna árvore formatada

Código:
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






Nó (node):
Essa parte do código cria as classes de nó de acordo com as regras da árvore RB

Implementa nó:
-Cria classe "RBNode"
-Define função para nós vermelhos que constrói nó de valor "value" e cor vermelha
    -Armazena valor do nó
    -Armazena cor do nó
    -Cria ponteiro de filho esquerdo, que começa vazio
    -Cria ponteiro de filho direito, que começa vazio
    -Cria ponteiro de pai, que começa vazio

Código
class RBNode:
    def __init__(self, value, color="red"):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

Avô:
-Define função "grandparent"
-Se não existir pai, retornar nada
-Se existir pai, retornar o pai do pai (avô)
Código
def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

Irmão:
-Define função "sibling"
-Se não existir pai, retornar nada
-Se nó for filho esquerdo, retornar filho direito
-Senão (nó é filho direito), retornar filho esquerdo
Código
def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

Tio
-Define função "uncle"
-Se não existir pai, retornar nada
--Se existir pai, retornar irmão do pai (tio)
def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()




Valores da árvore e impressão de versões:
Nessa parte do código colocamos os valores para inserir e remover e imprimimos suas respectivas versões

Importa a árvore:
-Inicializa a árvore persistente
-Insere 10, 20, 30, 40, 50 e 25
-Remove 10 e 20
-Cada operação cria uma nova versão
-Imprime versão 1 a 7

Código:
from tree.persistent import PersistentRedBlackTree

if __name__ == "__main__":
    tree = PersistentRedBlackTree()

    tree.insert(10)  # versão 1
    tree.insert(20)  # versão 2
    tree.delete(10)  # versão 3 (deletando 10)
    tree.insert(30)  # versão 3
    tree.insert(40)  # versão 4
    tree.insert(50)  # versão 5
    tree.insert(25)  # versão 6

    print("Versão 1 (após incluir 10):")
    print(" ".join(tree.print_version(1)))

    print("Versão 2 (após incluir 20):")
    print(" ".join(tree.print_version(2)))

    print("Versão 3 (após deletar 10 e incluir 30):")
    print(" ".join(tree.print_version(3)))

    print("Versão 6:")
    print(" ".join(tree.print_version(6)))

    tree.delete(20)  # versão 7

    print("\nVersão 7 (após deletar 20):")
    print(" ".join(tree.print_version(7)))

    print("\nVersão 2 (antes de deletar 20):")
    print(" ".join(tree.print_version(2)))

    tree.successor(25, 6)

    tree.successor(50, 7)
