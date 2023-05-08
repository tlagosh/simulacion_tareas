import numpy as np
import matplotlib.pyplot as plt

def generar_variable_laplace(mu, b, n):
    # Generar variables aleatorias de una distribución exponencial
    y = np.random.exponential(scale=b, size=n)
    
    # Generar variables aleatorias uniformes en el rango [0, 1]
    u = np.random.rand(n)
    
    # Aplicar la función de transformación para obtener las variables aleatorias de la distribución Laplace
    x = np.where(u < 0.5, mu + y, mu - y)
    
    return x

# Parámetros de la distribución Laplace
mu = 0 # Ubicación
b = 1 # Escala

# Generar 100 instancias independientes de la variable aleatoria
n = 100
instancias = generar_variable_laplace(mu, b, n)

print("Instancias generadas de la distribución Laplace:")
print(instancias)

# Graficar las instancias generadas en un histograma
plt.hist(instancias, bins=20, density=False, alpha=0.6, color='b')
plt.xlabel('Valor de la variable aleatoria')
plt.ylabel('Frecuencia relativa')
plt.title('Histograma de la distribución Laplace')
plt.grid(True)
plt.show()
