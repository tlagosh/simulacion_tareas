import random
import math
import matplotlib.pyplot as plt
import numpy as np

class Sistema:
    def __init__(self, producto1, producto2):
        self.producto1 = producto1
        self.producto2 = producto2

    def generar_xy(self):
        # Generar x condicionalmente
        x = random.uniform(1, 2) # Generar x entre 1 y 2 uniformemente
        y = None

        # Generar y condicionalmente
        while y is None:
            y_propuesto = random.uniform(0, 1) # Generar y entre 0 y 1 uniformemente
            # Comprobar si el valor propuesto de y cumple con la función de densidad conjunta
            if y_propuesto <= (1/2)*(x + y_propuesto):
                y = y_propuesto # Si cumple, asignar el valor de y propuesto

        return x, y

class Producto:
    def __init__(self, t_llegada, t1, t2):
        self.t_llegada = t_llegada
        self.t1 = t1
        self.t2 = t2
        self.tiempo_en_sistema = None

    def calcular_tiempo_en_sistema(self, t_salida):
        self.tiempo_en_sistema = t_salida - self.t_llegada
    
class Simulacion:
    def __init__(self, numero_de_productos, lam):
        self.numero_de_productos = numero_de_productos
        self.lam = lam
        self.sistema = Sistema(None, None)
        self.tiempos_promedio_en_sistema = []

    def simular_n_replicas(self, numero_de_replicas):
        for i in range(numero_de_replicas):
            print("Simulando réplica número: ", i + 1)
            random.seed(random.randint(0, 1000))
            np.random.seed(random.randint(0, 1000))
            self.simular()

    def simular(self):
        # Inicializar variables
        t = 0
        t_llegada = 0
        t_salida_1 = math.inf
        t_salida_2 = math.inf
        queue1 = []
        queue2 = []
        productos = []
        productos_listos = 0
        self.sistema.producto1 = None
        self.sistema.producto2 = None

        # Simular
        while productos_listos < self.numero_de_productos:
            # simulacion en base a eventos
            if t_llegada <= t_salida_1 and t_llegada <= t_salida_2:
                t = t_llegada
                # Generamos el tiempo de llegada del siguiente producto (poisson)
                t_llegada += np.random.poisson(self.lam)
                x, y = self.sistema.generar_xy()
                producto = Producto(t, x, y)
                productos.append(producto)
                if self.sistema.producto1 is None:
                    t_salida_1 = t + x
                    self.sistema.producto1 = producto
                else:
                    queue1.append(producto)
            elif t_salida_1 <= t_salida_2:
                t = t_salida_1
                producto = self.sistema.producto1
                if self.sistema.producto2 is None:
                    t_salida_2 = t + producto.t2
                    self.sistema.producto2 = producto
                    producto.calcular_tiempo_en_sistema(t_salida_2)
                else:
                    queue2.append(producto)
    
                if len(queue1) == 0:
                    self.sistema.producto1 = None
                    t_salida_1 = math.inf
                else:
                    producto = queue1.pop(0)
                    t_salida_1 = t + producto.t1
                    self.sistema.producto1 = producto
            else:
                t = t_salida_2
                productos_listos += 1
                if len(queue2) == 0:
                    self.sistema.producto2 = None
                    t_salida_2 = math.inf
                else:
                    producto = queue2.pop(0)
                    t_salida_2 = t + producto.t2
                    self.sistema.producto2 = producto
                    producto.calcular_tiempo_en_sistema(t_salida_2)
            
        # Calcular tiempos promedio en el sistema
        for producto in productos:
            if producto.tiempo_en_sistema is not None:
                self.tiempos_promedio_en_sistema.append(producto.tiempo_en_sistema)

    def mostrar_resultados(self, numero_de_replicas):
        # Mostrar resultados
        print("Tiempo promedio en el sistema: ", np.mean(self.tiempos_promedio_en_sistema))
        print("Desviación estándar del tiempo promedio en el sistema: ", np.std(self.tiempos_promedio_en_sistema))

        # Graficar
        plt.hist(self.tiempos_promedio_en_sistema, bins=100)
        plt.title("Frencuencia de tiempos promedio en el sistema")
        plt.xlabel("Tiempo promedio en el sistema")
        plt.ylabel("Frecuencia")
        # Dibujamos una línea vertical en el tiempo promedio en el sistema
        plt.axvline(np.mean(self.tiempos_promedio_en_sistema), color='k', linestyle='dashed', linewidth=1)
        plt.show()

