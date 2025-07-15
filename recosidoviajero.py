import random
import math

# Lista de ciudades
ciudades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
cantciudades = len(ciudades)

# Matriz de costos
matrizcostos = [
    [0, 12, 0, 10, 0, 12, 0],
    [12, 0, 12, 8, 0, 0, 0],
    [0, 12, 0, 11, 11, 0, 10],
    [10, 8, 11, 0, 3, 9, 0],
    [0, 0, 11, 3, 0, 7, 6],
    [12, 0, 0, 9, 7, 0, 9],
    [0, 0, 10, 0, 6, 9, 0]
]

def CalcularCosto(ruta):
    costo_total = 0
    for i in range(len(ruta) - 1):
        costo = matrizcostos[ruta[i]][ruta[i + 1]]
        if costo == 0:
            return float('inf')
        costo_total += costo
    retorno = matrizcostos[ruta[-1]][ruta[0]]
    if retorno == 0:
        return float('inf')
    return costo_total + retorno

def RutaInicialValida():
    from itertools import permutations
    for perm in permutations(range(cantciudades)):
        if CalcularCosto(perm) != float('inf'):
            return list(perm)
    return None

# Escoge nodo inicial y final usando ruleta
def EscogerIndicesPorRuleta(nodos_disponibles):
    prob = 1 / len(nodos_disponibles)
    ruleta = []
    acumulado = 0
    for nodo in nodos_disponibles:
        ruleta.append((acumulado, acumulado + prob, nodo))
        acumulado += prob
    r = random.random()
    for (ini, fin, nodo) in ruleta:
        if ini <= r < fin:
            return nodo
    return nodos_disponibles[-1]

def ObtenerVecino(ruta):
    for intento in range(10):  # Hasta 10 intentos para generar un vecino distinto
        nodos_validos = ruta[1:-1]
        nodo_ini = EscogerIndicesPorRuleta(nodos_validos)
        idx_ini = ruta.index(nodo_ini)

        posibles_finales = ruta[idx_ini + 1:-1]
        if not posibles_finales:
            continue
        nodo_fin = EscogerIndicesPorRuleta(posibles_finales)
        idx_fin = ruta.index(nodo_fin)

        if idx_ini >= idx_fin:
            continue

        subruta = ruta[idx_ini:idx_fin + 1]
        subruta_invertida = subruta[::-1]

        nueva = ruta[:idx_ini] + subruta_invertida + ruta[idx_fin + 1:]

        if nueva != ruta and CalcularCosto(nueva) != float('inf'):
            return nueva
    return ruta  # Si no se pudo generar uno distinto válido

def Recocido():
    ruta_actual = RutaInicialValida()
    if ruta_actual is None:
        print("No se encontró una ruta inicial válida.")
        return

    zc = CalcularCosto(ruta_actual)
    mejor_ruta = ruta_actual[:]
    mejor_costo = zc

    # Temperaturas fijas como sugirió Clavel
    t1 = 0.2 * zc
    T = [t1]
    for _ in range(4):
        T.append(0.5 * T[-1])

    print("*** Ruta inicial:", [ciudades[i] for i in ruta_actual], "Costo:", zc)
        
    for i, temp in enumerate(T):
        print(f"\n*** Iteración {i + 1} con T = {round(temp, 2)}")
        vecino = ObtenerVecino(ruta_actual)
        zn = CalcularCosto(vecino)

        print("*** Ruta candidata:", [ciudades[i] for i in vecino], "Costo:", zn)

        if zn < zc:
            print("*** Mejor vecino encontrado (mejor costo):", zn)
            ruta_actual = vecino
            zc = zn
            if zn < mejor_costo:
                mejor_ruta = vecino
                mejor_costo = zn
        else:
            delta = zc - zn
            prob_acept = math.exp(delta / temp)
            r = random.random()
            print(f" Zn > Zc. Δ={delta:.2f}, Probabilidad de aceptación={round(prob_acept, 3)}, r={round(r, 3)}")
            if r < prob_acept:
                print(" *** Se acepta solución peor por probabilidad. ***")
                ruta_actual = vecino
                zc = zn
            else:
                print(" *** Rechazada. Se mantiene la anterior. ***")

        print("*** Ruta actual:", [ciudades[i] for i in ruta_actual], "Costo:", zc)

    print("\n*** Mejor ruta encontrada:", [ciudades[i] for i in mejor_ruta])
    print("*** Costo total:", mejor_costo)

solucion = Recocido()
