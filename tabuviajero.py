import random
from itertools import permutations

# Lista de ciudades
ciudades = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] #son los nodos
cantciudades = len(ciudades) #número de nodos

matrizcostos = [
    [0, 12, 0, 10, 0, 12, 0],
    [12, 0, 12, 8, 0, 0, 0],
    [0, 12, 0, 11, 11, 0, 10],
    [10, 8, 11, 0, 3, 9, 0],
    [0, 0, 11, 3, 0, 7, 6],
    [12, 0, 0, 9, 7, 0, 9],
    [0, 0, 10, 0, 6, 9, 0]
]

# Costo es el peso de los arcos
def CalcularCostos(ruta):
    costototal = 0
    for i in range(len(ruta) - 1):
        costo = matrizcostos[ruta[i]][ruta[i+1]]
        if costo == 0:
            return float('inf')  # trayecto inexistente
        costototal += costo
    retorno = matrizcostos[ruta[-1]][ruta[0]]
    if retorno == 0:
        return float('inf')
    costototal += retorno
    return costototal

# Genera rutas vecinas invirtiendo segmentos
def ObtenerVecinos(camino):
    vecinos = []
    tam = len(camino)

    for inicio in range(1, tam - 2):  # Saltamos el primer nodo (ciudad de inicio)
        for fin in range(inicio + 1, tam - 1): 
            # Copiar los segmentos
            antes = camino[:inicio]
            medio = camino[inicio:fin + 1]
            despues = camino[fin + 1:]

            # Invertimos
            medio.reverse()

            nuevo_camino = antes + medio + despues
            vecinos.append((inicio, fin, nuevo_camino))
    
    return vecinos

# Intenta construir una ruta inicial completamente conectada
def CrearRutaInicial():
    for secuencia in permutations(range(cantciudades)):
        conexionvalida = True
        for i in range(cantciudades - 1):
            if matrizcostos[secuencia[i]][secuencia[i + 1]] == 0:
                conexionvalida = False
                break

        retornovalido = matrizcostos[secuencia[-1]][secuencia[0]] > 0

        if conexionvalida and retornovalido:
            return list(secuencia)

    return None

# Algoritmo principal de búsqueda tabú
def BusquedaTabu(cadena_base, max_pasos=100):
    actual = cadena_base[:]
    mejorcamino = actual[:]
    menorcosto = CalcularCostos(actual)

    memoriatabu = []
    sinnovedad = 0
    paso = 0

    while paso < max_pasos and sinnovedad < 3:
        alternativas = ObtenerVecinos(actual)
        topvecino = None
        topcosto = float('inf')
        movrestringido = None

        for (i, j, posible) in alternativas:
            eliminados = ((actual[i - 1], actual[i]), (actual[j], actual[j + 1]))

            if eliminados in memoriatabu:
                continue

            costo = CalcularCostos(posible)
            if costo == float('inf'):
                continue

            if costo < topcosto:
                topcosto = costo
                topvecino = posible
                movrestringido = eliminados

        if topvecino is None:
            print("Sin vecinos válidos fuera de la lista tabú. Proceso finalizado.")
            break

        actual = topvecino[:]
        if topcosto < menorcosto:
            menorcosto = topcosto
            mejorcamino = topvecino[:]
            sinnovedad = 0
        else:
            sinnovedad += 1

        memoriatabu.append(movrestringido)
        if len(memoriatabu) > 4:
            memoriatabu.pop(0)

        paso += 1
        print(f"Paso {paso}: Camino = {[ciudades[i] for i in actual]}, Costo = {topcosto}")

    return [ciudades[i] for i in mejorcamino], menorcosto

# Crear ruta de partida
inicio = CrearRutaInicial()
if not inicio:
    print("No fue posible construir una ruta válida.")
    exit()

mejorcamino, costooptimo = BusquedaTabu(inicio)

print("\nCamino óptimo hallado:", mejorcamino)
print("Costo total del recorrido:", costooptimo)