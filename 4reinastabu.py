import random
import pandas as pd
from copy import deepcopy

nreinas = 4
nmax = 6
tamtabu = 2

# Generar solución inicial
def GenerarIndividuo():
    ind = list(range(1, nreinas + 1))
    random.shuffle(ind)
    return ind

# Calcular colisiones diagonales (fitness)
def CalcularFitness(ind):
    colisiones = 0
    for i in range(len(ind)):
        for j in range(i + 1, len(ind)):
            if abs(ind[i] - ind[j]) == abs(i - j):
                colisiones += 1
    return colisiones

# Imprimir tablero
def ImprimirTablero(individuo):
    for fila in range(1, nreinas + 1):
        linea = ""
        for col in range(1, nreinas + 1):
            if individuo[col - 1] == fila:
                linea += "♕ "
            else:
                linea += ". "
        print(linea)
    print()

# Generar vecindario (todos los intercambios de 2 posiciones)
def GenerarVecindario(solucion_actual):
    vecinos = []
    for i in range(nreinas):
        for j in range(i + 1, nreinas):
            vecino = solucion_actual.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append((vecino, (i, j)))
    return vecinos

# Algoritmo de búsqueda tabú
def BusquedaTabu():
    actual = GenerarIndividuo()
    mejorsol = actual
    mejorfit = CalcularFitness(actual)

    tabu = []

    print("\n Solución inicial:", actual)
    ImprimirTablero(actual)

    for iteracion in range(nmax):
        print(f"*************** Iteración {iteracion}**************")
        vecinos = GenerarVecindario(actual)
        candidatos = []

        for vecino, movimiento in vecinos:
            fit = CalcularFitness(vecino)
            if movimiento not in tabu:
                candidatos.append((vecino, fit, movimiento))

        if not candidatos:
            print(" Todos los movimientos están en la lista tabú. Se selecciona al azar.")
            vecino, fit, movimiento = random.choice(vecinos)
        else:
            vecino, fit, movimiento = min(candidatos, key=lambda x: x[1])

        print(f"Mejor movimiento: intercambio {movimiento}, fitness = {fit}")
        print(f"Nueva solución: {vecino}")
        ImprimirTablero(vecino)

        actual = vecino
        tabu.append(movimiento)
        if len(tabu) > tamtabu:
            tabu.pop(0)

        if fit < mejorfit:
            mejorfit = fit
            mejorsol = vecino

    print("\nBúsqueda finalizada.")
    print("Mejor solución encontrada:", mejorsol, "con", mejorfit, "colisiones")
    ImprimirTablero(mejorsol)
    return mejorsol

BusquedaTabu()
