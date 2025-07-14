import random
import math

# Lista de ciudades
ciudades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
num_ciudades = len(ciudades)

# Matriz de distancias entre ciudades (0 = sin conexión directa)
matriz_costos = [
    [0, 12, 0, 10, 0, 12, 0], #A
    [12, 0, 12, 8, 0, 0, 0], #B
    [0, 12, 0, 11, 11, 0, 10], #C
    [10, 8, 11, 0, 3, 9, 0], #D 
    [0, 0, 11, 3, 0, 7, 6], #E
    [12, 0, 0, 9, 7, 0, 9], #F
    [0, 0, 10, 0, 6, 9, 0] #G
]

def calcular_costo(ruta):
    costo_total = 0
    for i in range(len(ruta) - 1):
        costo = matriz_costos[ruta[i]][ruta[i + 1]]
        if costo == 0:
            return float('inf')
        costo_total += costo
    # Retorno a la ciudad inicial
    retorno = matriz_costos[ruta[-1]][ruta[0]]
    if retorno == 0:
        return float('inf')
    costo_total += retorno
    return costo_total

def obtener_vecino(ruta):
    a, b = sorted(random.sample(range(len(ruta)), 2))
    vecino = ruta[:a] + ruta[a:b + 1][::-1] + ruta[b + 1:]
    return vecino

def ruta_inicial_valida():
    from itertools import permutations
    for ruta in permutations(range(num_ciudades)):
        if calcular_costo(ruta) != float('inf'):
            return list(ruta)
    return None

def recocido_simulado(max_iter=500, temp_inicial=100.0, enfriamiento=0.95):
    actual = ruta_inicial_valida()
    if actual is None:
        print("No se pudo encontrar una ruta válida inicial.")
        return

    costo_actual = calcular_costo(actual)
    mejor = actual[:]
    mejor_costo = costo_actual

    temperatura = temp_inicial

    print("Ruta inicial:", [ciudades[i] for i in actual], "Costo:", costo_actual)

    for iteracion in range(max_iter):
        vecino = obtener_vecino(actual)
        costo_vecino = calcular_costo(vecino)

        delta = costo_vecino - costo_actual

        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            actual = vecino
            costo_actual = costo_vecino

        if costo_actual < mejor_costo:
            mejor = actual[:]
            mejor_costo = costo_actual

        temperatura *= enfriamiento

        print(f"Iteración {iteracion + 1}: Ruta = {[ciudades[i] for i in actual]}, Costo = {costo_actual}, Temp = {round(temperatura, 2)}")

        if temperatura < 0.01:
            break

    print("\n Mejor ruta encontrada:", [ciudades[i] for i in mejor])
    print("Costo total:", mejor_costo)

# Ejecutar
recocido_simulado()
