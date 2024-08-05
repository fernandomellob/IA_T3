from typing import Iterable, Set, Tuple

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado: str, pai: 'Nodo' = None, acao: str = None, custo: int = 0):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado: str, representacao do estado do 8-puzzle
        :param pai: Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao: str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo: int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.filhos = []

    def __eq__(self, other):
        if isinstance(other, Nodo):
            return self.estado == other.estado
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.estado)


def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    espacoVazio = estado.rfind("_")
    linha = espacoVazio // 3
    coluna = espacoVazio % 3
    retorno = []
    
    def trocar(estado, i, j):
        estado = list(estado)
        estado[i], estado[j] = estado[j], estado[i]
        return ''.join(estado)

    if coluna > 0: 
        novo_estado = trocar(estado, espacoVazio, espacoVazio - 1)
        retorno.append(("esquerda", novo_estado))
    
    if coluna < 2:
        novo_estado = trocar(estado, espacoVazio, espacoVazio + 1)
        retorno.append(("direita", novo_estado))
    
    if linha > 0:
        novo_estado = trocar(estado, espacoVazio, espacoVazio - 3)
        retorno.append(("acima", novo_estado))
    
    if linha < 2: 
        novo_estado = trocar(estado, espacoVazio, espacoVazio + 3)
        retorno.append(("abaixo", novo_estado))

    return retorno


def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
