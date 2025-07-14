import random
import copy
from itertools import permutations

# Lista de ciudades
ciudades = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] #son los nodos
num_ciudades = len(ciudades) #número de nodos

# Matriz de distancias entre ciudades (0 indica que no hay conexión directa)
matriz_costos = [
    [0, 12, 0, 10, 0, 12, 0],
    [12, 0, 12, 8, 0, 0, 0],
    [0, 12, 0, 11, 11, 0, 10],
    [10, 8, 11, 0, 3, 9, 0],
    [0, 0, 11, 3, 0, 7, 6],
    [12, 0, 0, 9, 7, 0, 9],
    [0, 0, 10, 0, 6, 9, 0]
]

# Costo es el peso de los arcos
def calcular_costo(ruta):
    costo_total = 0
    for i in range(len(ruta) - 1):
        costo = matriz_costos[ruta[i]][ruta[i+1]]
        if costo == 0:
            return float('inf')  # trayecto inexistente
        costo_total += costo
    retorno = matriz_costos[ruta[-1]][ruta[0]]
    if retorno == 0:
        return float('inf')
    costo_total += retorno
    return costo_total

# Genera rutas vecinas invirtiendo segmentos
def obtener_vecinos(camino):
    opciones = []
    for i in range(1, len(camino) - 2):
        for j in range(i + 1, len(camino) - 1):
            candidato = camino[:i] + camino[i:j+1][::-1] + camino[j+1:]
            opciones.append((i, j, candidato))
    return opciones

# Intenta construir una ruta inicial completamente conectada
def crear_ruta_inicial():
    for secuencia in permutations(range(num_ciudades)):
        if all(matriz_costos[secuencia[i]][secuencia[i+1]] > 0 for i in range(num_ciudades - 1)) and matriz_costos[secuencia[-1]][secuencia[0]] > 0:
            return list(secuencia)
    return None

# Algoritmo principal de búsqueda tabú
def tabu_search(cadena_base, max_pasos=100):
    actual = cadena_base[:]
    mejor_camino = actual[:]
    menor_costo = calcular_costo(actual)

    memoria_tabu = []
    sin_novedad = 0
    paso = 0

    while paso < max_pasos and sin_novedad < 3:
        alternativas = obtener_vecinos(actual)
        top_vecino = None
        top_costo = float('inf')
        mov_restringido = None

        for (i, j, posible) in alternativas:
            eliminados = ((actual[i - 1], actual[i]), (actual[j], actual[j + 1]))

            if eliminados in memoria_tabu:
                continue

            costo = calcular_costo(posible)
            if costo == float('inf'):
                continue

            if costo < top_costo:
                top_costo = costo
                top_vecino = posible
                mov_restringido = eliminados

        if top_vecino is None:
            print("Sin vecinos válidos fuera de la lista tabú. Proceso finalizado.")
            break

        actual = top_vecino[:]
        if top_costo < menor_costo:
            menor_costo = top_costo
            mejor_camino = top_vecino[:]
            sin_novedad = 0
        else:
            sin_novedad += 1

        memoria_tabu.append(mov_restringido)
        if len(memoria_tabu) > 4:
            memoria_tabu.pop(0)

        paso += 1
        print(f"Paso {paso}: Camino = {[ciudades[i] for i in actual]}, Costo = {top_costo}")

    return [ciudades[i] for i in mejor_camino], menor_costo

# Crear ruta de partida
inicio = crear_ruta_inicial()
if not inicio:
    print("No fue posible construir una ruta válida.")
    exit()

mejor_camino, costo_optimo = tabu_search(inicio)

print("\nCamino óptimo hallado:", mejor_camino)
print("Costo total del recorrido:", costo_optimo)