def buscar_minimo(f, a, b, n):
    d = (b - a) / n
    valores_x = []
    valores_f = []

    x = a
    for i in range(n + 1):
        fx = f(x)
        valores_x.append(x)
        valores_f.append(fx)
        x += d

    # buscar el valor minimo de f y su correspondiente x
    minimo_valor = min(valores_f)
    indice_minimo = valores_f.index(minimo_valor)
    x_minimo = valores_x[indice_minimo]

    return x_minimo, minimo_valor

# Ejemplo de uso
def funcion_objetivo(x):
    return x**2 + 2*x + 1  # ejemplo: (x+1)^2, minimo en x = -1

a = -4.25
b = -1.5
n = 3

x_min, f_min = buscar_minimo(funcion_objetivo, a, b, n)
print(f"Minimo aproximado en x = {x_min}, f(x) = {f_min}")
