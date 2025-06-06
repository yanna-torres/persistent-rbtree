# Documentação

- [Documentação](#documentação)
  - [Nó (node):](#nó-node)
    - [Estrutura do Nó](#estrutura-do-nó)
    - [Métodos auxiliares para navegação na árvore](#métodos-auxiliares-para-navegação-na-árvore)
      - [Avô (`grandparent`)](#avô-grandparent)
      - [Irmão (`sibling`)](#irmão-sibling)
      - [Tio (`uncle`)](#tio-uncle)
  - [Árvore Rubro negra (red\_black\_tree):](#árvore-rubro-negra-red_black_tree)
    - [Estrutura da Árvore](#estrutura-da-árvore)
    - [Busca (`search`)](#busca-search)
    - [Inserção (`insert`)](#inserção-insert)
    - [Correção após inserção (`insert_fix`)](#correção-após-inserção-insert_fix)
    - [Remoção (`delete`)](#remoção-delete)
    - [Correção após remoção (`delete_fix`)](#correção-após-remoção-delete_fix)
    - [Rotação à esquerda (`rotate_left`)](#rotação-à-esquerda-rotate_left)
    - [Rotação à direita (`rotate_right`)](#rotação-à-direita-rotate_right)
    - [Funções Auxiliares](#funções-auxiliares)
      - [Substituição de nó (`_replace_node`)](#substituição-de-nó-_replace_node)
      - [Busca do mínimo (`_find_min`)](#busca-do-mínimo-_find_min)
  - [Persistência (persistent):](#persistência-persistent)
    - [Estrutura da Árvore Persistente](#estrutura-da-árvore-persistente)
    - [Inserção (`insert`)](#inserção-insert-1)
    - [Remoção (`delete`)](#remoção-delete-1)
    - [Sucessor de um valor em uma versão (`successor`)](#sucessor-de-um-valor-em-uma-versão-successor)
    - [Impressão da Árvore em uma versão (`print_version`)](#impressão-da-árvore-em-uma-versão-print_version)
  - [Aplicação (`app.py`)](#aplicação-apppy)
    - [Função `decode_input`](#função-decode_input)
    - [Execução principal](#execução-principal)


## Nó (node):

> Arquivo: [tree/node.py](tree/node.py)

Este arquivo define a classe do nó para a árvore rubro-negra, implementando as regras e propriedades básicas dessa estrutura.

### Estrutura do Nó

A classe `RBNode` representa um nó da árvore rubro-negra, com os seguintes atributos:
- Armazena valor do nó (`value`)
- Armazena cor do nó (`color`), que por padrão é vermelha (`red`)
- Cria uma referência para o filho esquerdo, que começa como `None`
- Cria uma referência para o filho direito, que começa `None`
- Cria uma referência para o pai, que começa `None`

```python
class RBNode:
    def __init__(self, value, color="red"):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None
```

### Métodos auxiliares para navegação na árvore

#### Avô (`grandparent`)

Retorna o avô do nó, caso exista; caso contrário, retorna `None`.

```python
def grandparent(self):
    if self.parent is None:
        return None
    return self.parent.parent
```

#### Irmão (`sibling`)

Retorna o irmão do nó (outro filho do mesmo pai), caso exista; caso contrário, retorna `None`.

```python
def sibling(self):
    if self.parent is None:
        return None
    if self == self.parent.left:
        return self.parent.right
    return self.parent.left
```

#### Tio (`uncle`)

Retorna o tio do nó, ou seja, o irmão do pai, caso exista; caso contrário, retorna `None`.

```python
def uncle(self):
    if self.parent is None:
        return None
    return self.parent.sibling()
```

---


## Árvore Rubro negra (red_black_tree):

> Arquivo: [tree/red_black_tree.py](tree/red_black_tree.py)

Este arquivo implementa uma árvore rubro-negra com operações básicas: busca, inserção, remoção e rotações.

### Estrutura da Árvore

A classe `RedBlackTree` representa a árvore rubro-negra e possui apenas a referência da raiz (`root`), que inicialmente é `None`.

```python
class RedBlackTree:
    def __init__(self):
        self.root = None
```

### Busca (`search`)

Retorna o nó que contém o valor buscado, iniciando pela raiz da árvore. Caso o valor não seja encontrado, retorna `None`.

```python
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
```

### Inserção (`insert`)

Insere um novo nó com o valor dado na árvore.

- Se a árvore estiver vazia, o novo nó se torna a raiz.
- Caso contrário, percorre a árvore para encontrar a posição correta do novo nó, inserindo-o como filho esquerdo ou direito conforme o valor, e atualiza o pai do novo nó.
- Por fim, chama a função [`insert_fix`](#correção-após-inserção-insert_fix) para corrigir a árvore.

```python
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
```

### Correção após inserção (`insert_fix`)

Corrige possíveis violações das propriedades rubro-negras após inserir um nó vermelho.

- Enquanto o pai do nó for vermelho, há necessidade de ajustes.
- Usa casos baseados na cor do tio e na posição do nó para fazer rotações e mudanças de cor.
- No final, garante que a raiz seja preta.

```python
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
```

### Remoção (`delete`)

Remove um nó com um determinado valor da árvore. 

- Procura o nó com o valor a ser removido.
- Se não encontrado, retorna sem fazer nada.
- Remove o nó mantendo as propriedades da árvore.
- Se o nó removido for preto, chama [`delete_fix`](#correção-após-remoção-delete_fix) para correção.

```python
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
```

### Correção após remoção (`delete_fix`)

Corrige possíveis violações após remoção.

- Enquanto o nó `x` não for a raiz e estiver com cor preta, verifica as propriedades do seu irmão para detectar desequilíbrios.
- Realiza recoloração e rotações conforme o caso para restaurar o equilíbrio da árvore.
- Ao final, garante que o nó `x` esteja colorido de preto para manter as propriedades da árvore.

```python
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
```

### Rotação à esquerda (`rotate_left`)

Rotaciona para a esquerda a partir de um nó.

- Rotaciona o nó `node` para a esquerda, promovendo seu filho direito (`right_child`).
- O filho esquerdo de `right_child` vira filho direito de `node`.
- Atualiza ponteiros dos pais e filhos conforme necessário.
- Se `node` for raiz, `right_child` assume seu lugar.
- `node` torna-se filho esquerdo de `right_child`.

```python
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
```

### Rotação à direita (`rotate_right`)

Rotaciona para a direita a partir de um nó.

- Rotaciona o nó `node` para a direita, promovendo seu filho esquerdo (`left_child`).
- O filho direito de `left_child` vira filho esquerdo de `node`.
- Atualiza ponteiros dos pais e filhos conforme necessário.
- Se `node` for raiz, `left_child` assume seu lugar.
- `node` torna-se filho direito de `left_child`.

```python
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
```

### Funções Auxiliares

#### Substituição de nó (`_replace_node`)

Substitui um nó antigo por um novo, atualizando os ponteiros do pai e da raiz conforme necessário.

```python
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
```


#### Busca do mínimo (`_find_min`)

Encontra o nó com o menor valor em uma subárvore, indo sempre para o filho esquerdo até o final.

```python
def _find_min(self, node):
    while node.left is not None:
        node = node.left
    return node
```

---


## Persistência (persistent): 


> Arquivo: [tree/persistent.py](tree/persistent.py)


Este arquivo implementa uma árvore rubro-negra persistente parcialmente, que mantém versões imutáveis da árvore após operações de inserção e remoção. Utiliza cópias profundas para garantir que versões anteriores permaneçam intactas.

### Estrutura da Árvore Persistente

A classe `PersistentRedBlackTree` mantém um vetor fixo para armazenar até 100 versões da árvore, usando uma instância da `RedBlackTree` para manipular cada versão. A classe possui os seguintes atributos:
- Um vetor de versões (`versions`) de tamanho 100, para armazenar as referências de cada versão
- A versão atual (`current_version`), incialmente 0
- Instância atual da árvore (`tree`)

```python
class PersistentRedBlackTree:
    def __init__(self):
        self.versions = [None] * 100
        self.current_version = 0
        self.tree = RedBlackTree()
        self.versions[0] = None
```

### Inserção (`insert`)

Insere um valor criando uma nova versão da árvore.

- Faz uma cópia profunda da árvore da versão atual.
- Insere o valor na cópia.
- Incrementa a versão atual e salva a nova raiz.

```python
def insert(self, value):
    self.tree.root = deepcopy(self.versions[self.current_version])
    self.tree.insert(value)
    self.current_version += 1
    self.versions[self.current_version] = self.tree.root
```

### Remoção (`delete`)

Remove um valor criando uma nova versão da árvore.

- Faz uma cópia profunda da árvore da versão atual.
- Remove o valor na cópia.
- Incrementa a versão atual e salva a nova raiz.

```python
def delete(self, value):
    self.tree.root = deepcopy(self.versions[self.current_version])
    self.tree.delete(value)
    self.current_version += 1
    self.versions[self.current_version] = self.tree.root
```

### Sucessor de um valor em uma versão (`successor`)

Retorna o sucessor do valor `x` na versão especificada da árvore.

- Se a versão solicitada for maior que a atual, usa a última versão disponível.
- Percorre a árvore da versão para encontrar o menor valor maior que `x`.
- Retorna o valor do sucessor ou inf caso não exista.

```python
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
```

### Impressão da Árvore em uma versão (`print_version`)

Retorna uma lista com a travessia em ordem da árvore da versão especificada, com informações de valor, profundidade e cor do nó.

- Se a versão for maior que a atual, usa a última versão disponível.
- Atravessa a árvore em ordem, registrando para cada nó:
    - `valor, profundidade, cor` ("R" para vermelho e "N" para preto).
- Retorna a lista de strings com essas informações.

```python
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
```

---

## Aplicação (`app.py`)

> Arquivo: [app.py](app.py)

Este arquivo implementa o programa principal para manipular uma árvore rubro-negra persistente por meio de comandos de um arquivo de entrada, gerando resultados em um arquivo de saída.

### Função `decode_input`

Lê um arquivo de entrada com comandos e executa operações na árvore persistente, armazenando os resultados em um arquivo de saída.

**Parâmetros:**

- `input_filename` (str): nome do arquivo de entrada com os comandos.
- `output_filename` (str): nome do arquivo onde o resultado será salvo.
- `tree` (PersistentRedBlackTree): instância da árvore rubro-negra persistente.

**Operações suportadas:**

- `INC <valor>`: insere o valor na versão atual da árvore.
- `REM <valor>`: remove o valor na versão atual da árvore.
- `SUC <valor> <versao>`: busca o sucessor do valor na versão indicada da árvore, escreve o comando e o resultado no arquivo.
- `IMP <versao>`: imprime os valores da árvore na versão indicada em ordem crescente, junto com a profundidade e cor dos nós, separados por espaços.

Caso o comando seja inválido ou mal formatado, uma mensagem de erro é impressa no console.

```python
def decode_input(input_filename, output_filename, tree):
    output_lines = []

    with open(input_filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            command = parts[0]
            if command == "INC" and len(parts) == 2:
                value = int(parts[1])
                tree.insert(value)
            elif command == "REM" and len(parts) == 2:
                value = int(parts[1])
                tree.delete(value)
            elif command == "SUC" and len(parts) == 3:
                value = int(parts[1])
                version = int(parts[2])
                succ = tree.successor(value, version)
                output_lines.append(f"SUC {value} {version}")
                output_lines.append(str(succ))
            elif command == "IMP" and len(parts) == 2:
                version = int(parts[1])
                result = tree.print_version(version)
                output_lines.append(f"IMP {version}")
                output_lines.append(" ".join(result))
            else:
                print(f"Invalid command: {line.strip()}")

    with open(output_filename, "w") as out_file:
        out_file.write("\n".join(output_lines))
```

### Execução principal

- Recebe o nome do arquivo de entrada via linha de comando.
- Inicializa a árvore persistente.
- Chama a função `decode_input` para processar o arquivo e gerar o resultado.
- Caso o número de argumentos esteja incorreto, imprime instrução de uso e encerra o programa.

```python
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <input_file.txt>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "output.txt"
    tree = PersistentRedBlackTree()
    decode_input(input_filename, output_filename, tree)
```