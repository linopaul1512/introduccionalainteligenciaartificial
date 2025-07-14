import random
import pandas as pd

# Parámetros
N_REINAS = 4
TAM_POBLACION = 6
N_MAX = 5
PROB_MUTACION = 0.1

# Generar individuo aleatoriamente como permutación
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

# Selección por ruleta con impresión didáctica del número aleatorio
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
    print(f"  → Número aleatorio r = {round(r, 3)}")

    for i, p in enumerate(prob_acum):
        if r < p:
            print(f"  → Individuo seleccionado: {poblacion[i]} (índice {i})")
            return poblacion[i]

    print("  → Selección por defecto: último individuo")
    return poblacion[-1]

# Cruce alternado sin repetición
def cruzar(p1, p2):
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

# Mutación por intercambio de dos posiciones
def mutar(ind):
    a, b = random.sample(range(N_REINAS), 2)
    original = ind.copy()
    ind[a], ind[b] = ind[b], ind[a]
    print(f"Mutación aplicada: {original} → {ind} (índices intercambiados: {a}, {b})")
    return ind

# Imprimir el tablero de ajedrez de un individuo
def imprimir_tablero(individuo):
    N = len(individuo)
    for fila in range(1, N + 1):
        linea = ""
        for col in range(1, N + 1):
            if individuo[col - 1] == fila:
                linea += "♕ "
            else:
                linea += ". "
        print(linea)
    print()

# Algoritmo genético principal
def algoritmo_genetico_n_reinas():
    poblacion = [generar_individuo() for _ in range(TAM_POBLACION)]

    print("\n🟩 Población inicial (posiciones de las reinas):")
    tabla_inicial = pd.DataFrame(poblacion, columns=[f"R{i+1}" for i in range(N_REINAS)])
    print(tabla_inicial)

    print("\n Tableros de ajedrez de la población inicial:")
    for i, ind in enumerate(poblacion):
        print(f"Individuo {i + 1}: {ind}")
        imprimir_tablero(ind)

    for generacion in range(N_MAX):
        print(f"\n==================== Generación {generacion} ====================")
        fitnesses = [calcular_fitness(ind) for ind in poblacion]

        # Mostrar tabla con fitness y ruleta
        tabla = pd.DataFrame(poblacion, columns=[f"R{i+1}" for i in range(N_REINAS)])
        tabla["Fitness"] = fitnesses
        inv_fit = [1 / (f + 1) for f in fitnesses]
        total_inv = sum(inv_fit)
        tabla["Prob"] = [round(f / total_inv, 3) for f in inv_fit]
        tabla["Prob Acum"] = tabla["Prob"].cumsum().round(3)
        print(tabla)

        # Verificar si hay solución perfecta (fitness 0)
        if 0 in fitnesses:
            solucion = poblacion[fitnesses.index(0)]
            print("\n ¡Solución encontrada!", solucion)
            print("\n Tablero de la solución:")
            imprimir_tablero(solucion)
            return solucion

        nueva_poblacion = []

        while len(nueva_poblacion) < TAM_POBLACION:
            randomIII = random.random()
            print(f"randomIII: {randomIII}")
            if randomIII < PROB_MUTACION:
                # MUTACIÓN
                padre = seleccion_ruleta(poblacion, fitnesses)
                hijo = mutar(padre.copy())
                nueva_poblacion.append(hijo)
            else:
                # CRUCE
                padre1 = seleccion_ruleta(poblacion, fitnesses)
                padre2 = seleccion_ruleta(poblacion, fitnesses)
                hijo1, hijo2 = cruzar(padre1, padre2)
                print(f"Cruce aplicado: {padre1} + {padre2} → {hijo1}, {hijo2}")
                nueva_poblacion.append(hijo1)
                if len(nueva_poblacion) < TAM_POBLACION:
                    nueva_poblacion.append(hijo2)


        poblacion = nueva_poblacion

    print("\n No se encontró solución en Nmax generaciones.")
    return None

solucion = algoritmo_genetico_n_reinas()
print("\n  Solución final:", solucion)
