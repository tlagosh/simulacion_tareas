'''
Considere un taller de proceso productivo al que llegan productos terminados a dos
etapas en serie: inspección y re-proceso. Las llegadas son de Poisson con tiempo promedio
entre llegadas igual a 1.8. Los tiempos de inspección y re-proceso para un producto dado
son v.a. dependientes con función densidad conjunta:
f (x, y) = (1/ 2)(x + y); 1 <= x <= 2; 0 <= y <= 1
Se desea generar el paso de 1000 productos por este sistema. Desarrolle un modelo de
simulación para estimar el tiempo promedio de permanencia de un producto en este
sistema. El sistema parte vacío. Utilice el método de las distribuciones condicionales para
generar las instancias de v.a. dependientes de este caso. Desarrolle 20 réplicas y presente
adecuadamente su resultados. 
'''

from clases import *

def main():
    # Definimos los parámetros de la simulación
    numero_de_productos = 1000
    lam = 1.8
    # pedimos el número de réplicas
    numero_de_replicas = int(input("Ingrese el número de réplicas: "))
    # Creamos la simulación
    simulacion = Simulacion(numero_de_productos, lam)
    # Iniciamos la simulación
    simulacion.simular_n_replicas(numero_de_replicas)
    # Mostramos los resultados
    simulacion.mostrar_resultados(numero_de_replicas)

if __name__ == "__main__":
    main()