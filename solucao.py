from typing import Iterable, Set, Tuple
import heapq
from heapq import heappush, heappop

class Nodo:
    """
    Classe que representa um nó no grafo de busca do 8-puzzle.
    Cada nó contém informações sobre o estado do jogo, o nó pai,
    a ação que levou a esse nó e o custo do caminho até esse nó.
    """

    def __init__(self, estado: str, pai: 'Nodo' = None, acao: str = None, custo: int = 0):
        """
        inicializa o nó com os atributos recebidos.
        :param estado: str, representação do estado do 8-puzzle
        :param pai: Nodo, referência ao nó pai (None no caso do nó raiz)
        :param acao: str, ação a partir do pai que leva a este nó (None no caso do nó raiz)
        :param custo: int, custo do caminho da raiz até este nó
        """
        self.estado = estado  
        self.pai = pai  
        self.acao = acao  # Ação que levou a esse nó a partir do pai (None para o nó raiz)
        self.custo = custo  # Custo do caminho da raiz até esse nó
        self.filhos = []  # Lista para armazenar os nós filhos 

    def __eq__(self, other):
        """
        verifica igualdade entre dois nós
        """
        if isinstance(other, Nodo):
            return self.estado == other.estado
        return False

    def __ne__(self, other):
        """
        verifica desigualdade entre dois nós
        """
        return not self.__eq__(other)
    
    def __lt__(self, other):
        """
        compara dois nós, utilizado pela fila de prioridade
        Compara os custos dos nós.
        :param other: Nodo, outro nó para comparação
        :return: bool, True se o custo deste nó é menor que o custo do outro nó, False caso contrário
        """
        return self.custo < other.custo

    def __hash__(self):
        """
        obtem o hash do nó.
        """
        return hash(self.estado)


def sucessor(estado: str) -> Set[Tuple[str, str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação, estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado: string representando o estado atual do jogo
    :return: conjunto de tuplas (ação, novo_estado)
    """
    # Encontra a posição do espaço vazio '_' no estado
    espacoVazio = estado.rfind("_")
    
    # Calcula a linha e coluna correspondentes à posição do espaço vazio
    linha = espacoVazio // 3
    coluna = espacoVazio % 3
    
    # Lista para armazenar as tuplas (ação, novo_estado)
    retorno = []
    
    # Função auxiliar para trocar dois caracteres em uma string
    def trocar(estado, i, j):
        estado = list(estado)  # Converte a string para lista
        estado[i], estado[j] = estado[j], estado[i]  # Troca os caracteres
        return ''.join(estado)  # Converte a lista de volta para string

    # Verifica se é possível mover para a esquerda
    if coluna > 0:
        novo_estado = trocar(estado, espacoVazio, espacoVazio - 1)
        retorno.append(("esquerda", novo_estado))

    # Verifica se é possível mover para a direita
    if coluna < 2:
        novo_estado = trocar(estado, espacoVazio, espacoVazio + 1)
        retorno.append(("direita", novo_estado))

    # Verifica se é possível mover para cima
    if linha > 0:
        novo_estado = trocar(estado, espacoVazio, espacoVazio - 3)
        retorno.append(("acima", novo_estado))

    # Verifica se é possível mover para baixo
    if linha < 2:
        novo_estado = trocar(estado, espacoVazio, espacoVazio + 3)
        retorno.append(("abaixo", novo_estado))

    return retorno


def expande(nodo: Nodo) -> Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é um sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return: conjunto de nodos sucessores
    """
    # Chama a função sucessor para obter as ações possíveis e os estados atingidos
    sucessores = sucessor(nodo.estado)

    # Conjunto para armazenar os nodos sucessores
    nodos_sucessores = set()

    # Itera sobre as tuplas (ação, estado) retornadas pela função sucessor
    for acao, novo_estado in sucessores:
        # Cria um novo nodo com o novo estado, tendo o nodo atual como pai
        novo_nodo = Nodo(
            estado=novo_estado,
            pai=nodo,
            acao=acao,
            custo=nodo.custo + 1  # O custo é incrementado em 1 para cada movimento
        )

        # Adiciona o novo nodo ao conjunto de nodos sucessores
        nodos_sucessores.add(novo_nodo)

    return nodos_sucessores


def astar_hamming(estado: str) -> list[str] | None:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.
    :param estado: str
    :return: list[str] | None
    """
    # Estado objetivo
    objetivo = "12345678_"

    # Cria o nó raiz
    nodo_raiz = Nodo(estado)

    # Conjunto para armazenar os nós já explorados
    explorados = set()

    # Fila de prioridade para a fronteira, ordenada pelo custo f(n) = g(n) + h(n)
    fronteira = []

    # Adiciona o nó raiz à fronteira
    heappush(fronteira, (hamming_heuristica(nodo_raiz.estado), nodo_raiz))

    while fronteira:
        # Extrai o nó com menor custo f(n) da fronteira
        _, nodo_atual = heappop(fronteira)

        # Verifica se o nó atual é o objetivo
        if nodo_atual.estado == objetivo:
            # Reconstrói o caminho a partir do nó objetivo
            caminho = []
            while nodo_atual.pai is not None:
                caminho.append(nodo_atual.acao)
                nodo_atual = nodo_atual.pai
            caminho.reverse()
            return caminho

        # Marca o nó atual como explorado
        explorados.add(nodo_atual.estado)

        # Expande o nó atual e adiciona os sucessores não explorados à fronteira
        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados:
                custo_f = nodo_sucessor.custo + hamming_heuristica(nodo_sucessor.estado)
                heappush(fronteira, (custo_f, nodo_sucessor))

    # Caso não haja solução
    return None

def hamming_heuristica(estado: str) -> int:
    """
    Calcula a distância de Hamming entre o estado atual e o estado objetivo.
    :param estado: str
    :return: int
    """
    objetivo = "12345678_"
    distancia = 0
    for i in range(9):
        if estado[i] != objetivo[i] and estado[i] != "_":
            distancia += 1
    return distancia


def astar_manhattan(estado: str) -> list[str] | None:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.
    :param estado: str
    :return: list[str] | None
    """
    # Estado objetivo
    objetivo = "12345678_"

    # Cria o nó raiz
    nodo_raiz = Nodo(estado)

    # Conjunto para armazenar os nós já explorados
    explorados = set()

    # Fila de prioridade para a fronteira, ordenada pelo custo f(n) = g(n) + h(n)
    fronteira = []

    # Adiciona o nó raiz à fronteira
    heapq.heappush(fronteira, (manhattan_heuristica(nodo_raiz.estado), nodo_raiz))

    while fronteira:
        # Extrai o nó com menor custo f(n) da fronteira
        _, nodo_atual = heapq.heappop(fronteira)

        # Verifica se o nó atual é o objetivo
        if nodo_atual.estado == objetivo:
            # Reconstrói o caminho a partir do nó objetivo
            caminho = []
            while nodo_atual.pai is not None:
                caminho.append(nodo_atual.acao)
                nodo_atual = nodo_atual.pai
            caminho.reverse()
            return caminho

        # Marca o nó atual como explorado
        explorados.add(nodo_atual.estado)

        # Expande o nó atual e adiciona os sucessores não explorados à fronteira
        for nodo_sucessor in expande(nodo_atual):
            if nodo_sucessor.estado not in explorados:
                custo_f = nodo_sucessor.custo + manhattan_heuristica(nodo_sucessor.estado)
                heapq.heappush(fronteira, (custo_f, nodo_sucessor))

    # Caso não haja solução
    return None

def manhattan_heuristica(estado: str) -> int:
    """
    Calcula a soma das distâncias de Manhattan entre o estado atual e o estado objetivo.
    :param estado: str
    :return: int
    """
    objetivo = "12345678_"
    distancia = 0
    for i in range(9):
        if estado[i] != "_":
            posicao_correta = objetivo.index(estado[i])
            linha_correta, coluna_correta = posicao_correta // 3, posicao_correta % 3
            linha_atual, coluna_atual = i // 3, i % 3
            distancia += abs(linha_correta - linha_atual) + abs(coluna_correta - coluna_atual)
    return distancia

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
