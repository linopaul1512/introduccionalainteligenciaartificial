import random
import pandas as pd

# Parámetros
N_REINAS = 4
TAM_POBLACION = 6
N_MAX = 5
PROB_MUTACION = 0.1

# Generar individuo
def generar_individuo():
    ind = list(range(1, N_REINAS + 1))
    random.shuffle(ind)
    return ind

# Fitness: número de colisiones diagonales
def calcular_fitness(ind):
    colisiones = 0
    for i in range(len(ind)):
        for j in range(i + 1, len(ind)):
            if abs(ind[i] - ind[j]) == abs(i - j):
                colisiones += 1
    return colisiones

# Selección por ruleta (fitness inverso)
def seleccion_ruleta(poblacion, fitnesses):
    inv_fitness = [1 / (f + 1) for f in fitnesses]
    total = sum(inv_fitness)
    probs = [f / total for f in inv_fitness]
    prob_acum = []
    acum = 0
    for p in probs:
        acum += p
        prob_acum.append(acum)
    r = random.random()
    for i, p in enumerate(prob_acum):
        if r <= p:
            return poblacion[i]
    return poblacion[-1]

# Cruce alternado
def cruzar_alternado(p1, p2):
    def crear_hijo(orden):
        hijo, usados = [], set()
        for gen in orden:
            if gen not in usados:
                hijo.append(gen)
                usados.add(gen)
        return hijo
    orden_h1 = [p1[0], p2[0], p1[1], p2[1], p1[2], p2[2], p1[3], p2[3]]
    orden_h2 = [p2[0], p1[0], p2[1], p1[1], p1[2], p2[2], p1[3], p2[3]]
    return crear_hijo(orden_h1), crear_hijo(orden_h2)

# Mutación por intercambio
def mutar(ind):
    a, b = random.sample(range(N_REINAS), 2)
    ind[a], ind[b] = ind[b], ind[a]
    return ind

# Algoritmo principal
def algoritmo_genetico_n_reinas():
    poblacion = [generar_individuo() for _ in range(TAM_POBLACION)]
    for generacion in range(N_MAX):
        fitnesses = [calcular_fitness(ind) for ind in poblacion]
        
        tabla = pd.DataFrame(poblacion, columns=[f"R{i+1}" for i in range(N_REINAS)])
        tabla["Fitness"] = fitnesses
        inv_fit = [1 / (f + 1) for f in fitnesses]
        total_inv = sum(inv_fit)
        tabla["Prob"] = [round(f / total_inv, 3) for f in inv_fit]
        tabla["Prob Acum"] = tabla["Prob"].cumsum().round(3)
        print(f"\nGeneración {generacion}:\n", tabla)

        if 0 in fitnesses:
            solucion = poblacion[fitnesses.index(0)]
            print("\n¡Solución encontrada!", solucion)
            return solucion

        nueva_poblacion = []
        while len(nueva_poblacion) < TAM_POBLACION:
            padre1 = seleccion_ruleta(poblacion, fitnesses)

            if random.random() < PROB_MUTACION:
                hijo = mutar(padre1.copy())
                print(f"Mutación aplicada: {padre1} → {hijo}")
                nueva_poblacion.append(hijo)
            else:
                padre2 = seleccion_ruleta(poblacion, fitnesses)
                hijo1, hijo2 = cruzar_alternado(padre1, padre2)
                print(f"Cruce aplicado: {padre1} + {padre2} → {hijo1}, {hijo2}")
                nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion[:TAM_POBLACION]

    print("\nNo se encontró solución en Nmax generaciones.")
    return None

# Ejecutar
solucion = algoritmo_genetico_n_reinas()
print("\nSolución final:", solucion)