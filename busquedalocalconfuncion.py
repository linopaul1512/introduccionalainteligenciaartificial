import numpy as np


def encontrar_minimo_local(funcion, limite_izq, limite_der, pasos):
    # Generar puntos equidistantes en el rango especificado
    puntos = np.linspace(limite_izq, limite_der, pasos + 1)
    
    # Evaluar la función en cada punto
    resultados = [funcion(p) for p in puntos]
    
    # Determinar la posición del menor valor
    pos_min = np.argmin(resultados)
    
    # Recuperar x y f(x) correspondientes al mínimo encontrado
    mejor_x = puntos[pos_min]
    mejor_fx = resultados[pos_min]
    
    return mejor_x, mejor_fx

# Definir la función que se desea minimizar
def evaluar_funcion_objetivo(x):

    return x**3 - 2 * x + 3

# Establecer los límites del dominio y la cantidad de particiones
inicio_intervalo = -1
fin_intervalo = 5
divisiones = 100

# Ejecutar la búsqueda del valor mínimo
punto_optimo, valor_minimo = encontrar_minimo_local(evaluar_funcion_objetivo, inicio_intervalo, fin_intervalo, divisiones)

# Mostrar resultados obtenidos
print(f"El mínimo estimado está en x = {punto_optimo}, con f(x) = {valor_minimo}")