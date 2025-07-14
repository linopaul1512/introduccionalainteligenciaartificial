import random
import pandas as pd
from copy import deepcopy

N_REINAS = 4
N_MAX = 6
TAM_TABU = 2

# Generar solución inicial
def generar_individuo():
    ind = list(range(1, N_REINAS + 1))
    random.shuffle(ind)
    return ind

# Calcular colisiones diagonales (fitness)
def calcular_fitness(ind):
    colisiones = 0
    for i in range(len(ind)):
        for j in range(i + 1, len(ind)):
            if abs(ind[i] - ind[j]) == abs(i - j):
                colisiones += 1
    return colisiones

# Imprimir tablero
def imprimir_tablero(individuo):
    for fila in range(1, N_REINAS + 1):
        linea = ""
        for col in range(1, N_REINAS + 1):
            if individuo[col - 1] == fila:
                linea += "♕ "
            else:
                linea += ". "
        print(linea)
    print()

# Generar vecindario (todos los intercambios de 2 posiciones)
def generar_vecindario(solucion_actual):
    vecinos = []
    for i in range(N_REINAS):
        for j in range(i + 1, N_REINAS):
            vecino = solucion_actual.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append((vecino, (i, j)))
    return vecinos

# Algoritmo de búsqueda tabú
def busqueda_tabu():
    actual = generar_individuo()
    mejor_sol = actual
    mejor_fit = calcular_fitness(actual)

    tabu = []

    print("\n🔷 Solución inicial:", actual)
    imprimir_tablero(actual)

    for iteracion in range(N_MAX):
        print(f"================== Iteración {iteracion} ==================")
        vecinos = generar_vecindario(actual)
        candidatos = []

        for vecino, movimiento in vecinos:
            fit = calcular_fitness(vecino)
            if movimiento not in tabu:
                candidatos.append((vecino, fit, movimiento))

        if not candidatos:
            print(" Todos los movimientos están en la lista tabú. Se selecciona al azar.")
            vecino, fit, movimiento = random.choice(vecinos)
        else:
            vecino, fit, movimiento = min(candidatos, key=lambda x: x[1])

        print(f"Mejor movimiento: intercambio {movimiento}, fitness = {fit}")
        print(f"Nueva solución: {vecino}")
        imprimir_tablero(vecino)

        actual = vecino
        tabu.append(movimiento)
        if len(tabu) > TAM_TABU:
            tabu.pop(0)

        if fit < mejor_fit:
            mejor_fit = fit
            mejor_sol = vecino

    print("\nBúsqueda finalizada.")
    print("Mejor solución encontrada:", mejor_sol, "con", mejor_fit, "colisiones")
    imprimir_tablero(mejor_sol)
    return mejor_sol

# Ejecutar
solucion = busqueda_tabu()
