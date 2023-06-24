import math


    #### PRIMEIRA ESTRATÉGIA ####
def first_try(origem, destinos):
    """
    Estratégia do cálculo de coordenadas
    Organização simples
    """
    coordenadas_ordenadas = (origem,) + tuple(sorted(destinos, key=lambda x: abs(origem[0] - x[0])))
    return coordenadas_ordenadas


    #### SEGUNDA ESTRATÉGIA ####
def second_try(coordenadas):
    """
    Estratégia "vizinho mais próximo"
    - Retorna uma lista de tuplas com coordenadas -
    """
    visitados = [False] * len(coordenadas)
    caminho = []
    inicio = 0
    caminho.append(inicio)
    visitados[inicio] = True

    while len(caminho) < len(coordenadas):
        ultimo_vertice = caminho[-1]
        proximo_vertice = None
        menor_distancia = float('inf')
        
        for i in range(len(coordenadas)):
            if not visitados[i]:
                distancia = calcular_distancia(coordenadas[ultimo_vertice], coordenadas[i])
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    proximo_vertice = i
        
        caminho.append(proximo_vertice)
        visitados[proximo_vertice] = True
    return caminho

def calcular_distancia(coordenada1, coordenada2):
    """
    Função auxiliar da estratégia "vizinho mais próximo"
    """
    lat1, lon1 = coordenada1
    lat2, lon2 = coordenada2
    dist = math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
    return dist
     

    ### TERCEIRA ESTRATÉGIA ###    
def distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    

def tsp_branch_and_bound(coordinates):

    num_cities = len(coordinates)
    distance_matrix = [[distance(coord1, coord2) for coord2 in coordinates] for coord1 in coordinates]

    # Função auxiliar para calcular o custo de um caminho parcial
    def calculate_path_cost(path):
        cost = 0
        for i in range(len(path) - 1):
            cost += distance_matrix[path[i]][path[i+1]]
        return cost

    # Função auxiliar para verificar se um caminho parcial é promissor
    def is_promising(path):
        # Verifica se todas as cidades já foram visitadas
        if len(path) == num_cities:
            return True

        # Calcula o custo mínimo do caminho parcial
        min_cost = calculate_path_cost(path)

        # Verifica se o custo mínimo é menor que o melhor custo atual
        if min_cost < best_cost[0]:
            return True

        return False

    # Função recursiva para realizar a busca branch-and-bound
    def branch_and_bound(path):
        if is_promising(path):
            # Se o caminho parcial for promissor, continua a busca
            if len(path) == num_cities:
                # Se todas as cidades foram visitadas, atualiza o melhor custo e caminho
                cost = calculate_path_cost(path)
                if cost < best_cost[0]:
                    best_cost[0] = cost
                    best_path[0] = path
            else:
                # Se ainda há cidades não visitadas, continua a busca recursivamente
                for city in range(num_cities):
                    if city not in path:
                        branch_and_bound(path + [city])

    # Inicializa o melhor custo e caminho com valores altos
    best_cost = [float('inf')]
    best_path = [[]]

    # Inicia a busca a partir da cidade de origem (índice 0)
    branch_and_bound([0])

    # Retorna o melhor caminho encontrado
    return [coordinates[i] for i in best_path[0]]
