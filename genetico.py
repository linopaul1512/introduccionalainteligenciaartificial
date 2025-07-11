import random
import pandas as pd

# Parámetros del Algoritmo genético
pop_size     = 10    # tamaño de población
generaciones = 20    # número de generaciones
tasa_mut     = 0.1   # probabilidad de mutación

# Rango real requerido por el problema: -1 ≤ x ≤ 5
a = -1
b = 5
bits = 5

# Convierte número entero a binario de 5 bits (para mostrar)
def binario_nbits(n, bits=5):
    return f"{int(n):0{bits}b}"

# Convierte binario a entero decimal
def decodificar(binario):
    return int(binario, 2)

#convierte entero entre 0 y 31 a un valor real entre -1 y 5
def bin_a_real(n, bits=5, a=-1, b=5):
    max_bin = 2**bits - 1  # 31
    return a + (n / max_bin) * (b - a)

# Mutación
def mutar_binario(binario):
    idx = random.randrange(len(binario))
    lista = list(binario)
    lista[idx] = '1' if lista[idx] == '0' else '0'
    return ''.join(lista), idx

# Cruce
def cruzar_binario(p, m):
    punto = random.randrange(1, len(p))
    h1 = p[:punto] + m[punto:]
    h2 = m[:punto] + p[punto:]
    return h1, h2, punto

def algoritmo_genetico():
    # 1) Inicializar población aleatoria: números enteros entre 0 y 31 (porque usamos 5 bits)
    # Cada número se decodificará como valor real entre -1 y 5
    poblacion = [random.randint(0, 2**bits - 1) for _ in range(pop_size)]

    for gen in range(1, generaciones + 1):
        print(f"\n==== Generación {gen} ====")

        # 2) Evaluar fitness usando la función f(x) = x³ - 2x + 3
        # Primero convertimos los enteros de la población a sus valores reales
        #  bin_a_real(): convierte enteros en el rango [0,31] a valores reales [-1,5]
        valores_real = [bin_a_real(x, bits, a, b) for x in poblacion]

        # se aplica f(x) = x³ - 2x + 3 para calcular fitness
        fitness_vals = [x**3 - 2*x + 3 for x in valores_real]
        total_f = sum(fitness_vals)

        # 3) Calcular probabilidades individuales y acumuladas
        probs = [f/total_f if total_f > 0 else 0 for f in fitness_vals]
        acc_probs = []
        acum = 0
        for p in probs:
            acum += p
            acc_probs.append(acum)

        # 4) Mostrar tabla
        df = pd.DataFrame({
            'Idx':     list(range(pop_size)),
            'Bin':     [binario_nbits(x) for x in poblacion],   # Muestra binario
            'Decimal': poblacion,                                # Muestra entero original (0–31)
            'Real':    [round(r, 4) for r in valores_real],      # USO de bin_a_real(): valor real correspondiente
            'Fitness': [round(f, 4) for f in fitness_vals],      # Fitness según f(x)
            'P_ind':   [round(p, 5) for p in probs],
            'P_acum':  [round(p, 5) for p in acc_probs],
        })
        print(df)

        # 5) Generar nueva población mediante selección, cruce y mutación
        nueva = []
        for _ in range(pop_size):
            # Selección por ruleta para el padre
            r1 = random.random()
            i1 = next(i for i, p in enumerate(acc_probs) if r1 <= p)
            padre = poblacion[i1]
            pad_bin = binario_nbits(padre, bits)

            if random.random() < tasa_mut:
                # MUTACIÓN
                hijo_bin, bit = mutar_binario(pad_bin)
                hijo = decodificar(hijo_bin)
                print(f"Mutación: padre={padre} ({pad_bin}), bit invertido={bit} -> hijo={hijo} ({hijo_bin})")
            else:
                # CRUCE
                r2 = random.random()
                i2 = next(i for i, p in enumerate(acc_probs) if r2 <= p)
                madre = poblacion[i2]
                mad_bin = binario_nbits(madre, bits)

                #  genera hijos a partir de los binarios de padre y madre
                h1_bin, h2_bin, pt = cruzar_binario(pad_bin, mad_bin)
                hijo = decodificar(h1_bin)
                print(f"Cruce pto={pt}: {padre} ({pad_bin}) × {madre} ({mad_bin}) -> hijo={hijo} ({h1_bin})")

            nueva.append(hijo)

        # 6) Reemplazar población con los nuevos hijos
        poblacion = nueva

if __name__ == "__main__":
    algoritmo_genetico()