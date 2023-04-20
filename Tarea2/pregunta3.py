import numpy as np
import matplotlib.pyplot as plt

def generar_laplace(mu, b, n):
    """
    Genera n instancias independientes de una variable aleatoria Laplace
    con media mu y parámetro de escala b.

    Args:
        mu (float): Media de la distribución Laplace.
        b (float): Parámetro de escala de la distribución Laplace.
        n (int): Número de instancias a generar.

    Returns:
        numpy.ndarray: Array con n instancias de la variable aleatoria Laplace.
    """
    u1 = np.random.uniform(size=n)
    u2 = np.random.uniform(size=n)
    signo = np.where(u1 >= 0.5, 1, -1)
    x = mu - b * signo * np.log(1 - u2)
    return x

# Parámetros de la distribución Laplace
mu = 0.0
b = 1.0

# Número de instancias a generar
n = 1000

# Generar instancias de la variable aleatoria Laplace
instancias_laplace = generar_laplace(mu, b, n)

# Generar histograma
plt.hist(instancias_laplace, bins=20, density=True)
plt.xlabel('Valor')
plt.ylabel('Densidad de probabilidad')
plt.title('Histograma de la distribución Laplace')
plt.show()