'''
Considere que ese caso se quiere modelar con el modelo matemático M/M/C/N. C
representa el número de naves disponibles para la reparación de camiones, N es el número
de camiones. El tiempo hasta la falla de un camión es exponencial a tasa λ; el tiempo de
reparación de un camión es exponencial tasa µ. Formule y resuelva este sistema para su
operación en largo plazo. Se desea estimar el número medio de camiones operando en el
largo plazo.
Suponga ahora que N=50; C=12; El tiempo promedio hasta que falla un camión es de 2
meses; el tiempo medio de reparación es de 1 mes. Obtenga resultados numéricos. Haga
análisis de sensibilidad razonables. 
'''

from clases import *

def main():
    # Definimos los parámetros de la simulación
    numero_de_camiones = 50
    numero_de_naves = 12
    lam = 1/2
    mu = 1/1
    # pedimos el tiempo máximo de simulación
    tiempo_maximo = int(input("Ingrese el tiempo máximo de simulación: "))
    # Creamos la simulación
    simulacion = Simulacion(numero_de_camiones, numero_de_naves, lam, mu, tiempo_maximo)
    # Iniciamos la simulación
    simulacion.iniciar_simulacion()
    # Mostramos los resultados
    simulacion.mostrar_resultados()
    
if __name__ == "__main__":
    main()