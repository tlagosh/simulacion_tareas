import random
import math
import numpy as np
import matplotlib.pyplot as plt

class Camion:
    def __init__(self, id, tiempo_llegada, tiempo_reparacion, tiempo_salida):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_reparacion = tiempo_reparacion
        self.tiempo_salida = tiempo_salida

class Nave:
    def __init__(self, id):
        self.id = id
        self.camion = None
    
    def reparar_camion(self, camion):
        self.camion = camion
    
    def liberar_camion(self):
        self.camion = None
    
    def esta_libre(self):
        return self.camion == None

class Simulacion:
    def __init__(self, numero_de_camiones, numero_de_naves, lam, mu, tiempo_maximo=1000):
        self.numero_de_camiones = numero_de_camiones
        self.numero_de_naves = numero_de_naves
        self.lam = lam
        self.mu = mu
        self.tiempo_actual = 0
        self.tiempo_maximo = tiempo_maximo
        self.camiones = []
        self.naves = []
        self.camiones_en_espera = []
        self.camiones_en_reparacion = []
        self.camiones_en_operacion = []

        self.histograma_de_camiones_en_operacion = []

    def generar_tiempo_llegada(self):
        return random.expovariate(self.lam)

    def generar_tiempo_reparacion(self):
        return random.expovariate(self.mu)

    def iniciar_simulacion(self):
        # Creamos los camiones
        for i in range(self.numero_de_camiones):
            tiempo_llegada = self.generar_tiempo_llegada()
            # tiempo de reparación inicialmente infinito
            tiempo_reparacion = math.inf
            tiempo_salida = tiempo_llegada + tiempo_reparacion
            camion = Camion(i, tiempo_llegada, tiempo_reparacion, tiempo_salida)
            self.camiones.append(camion)
            # Todos los camiones empiezan en operación
            self.camiones_en_operacion.append(camion)

        # Creamos las naves
        for i in range(self.numero_de_naves):
            nave = Nave(i)
            self.naves.append(nave)

        # Iniciamos la simulación
        while self.tiempo_actual < self.tiempo_maximo:
            # Histograma

            self.histograma_de_camiones_en_operacion.append((len(self.camiones_en_operacion), self.tiempo_actual))
            #print(f"Camiones en operación: {len(self.camiones_en_operacion)}, tiempo actual: {self.tiempo_actual}")

            # Simulación en base a eventos, vemos que evento suc
            # 1. Llegada de camión
            # 2. Salida de camión

            if len(self.camiones_en_operacion) > 0:
                camion_entrante = self.camiones_en_operacion[0]
                for c in self.camiones_en_operacion:
                    if c.tiempo_llegada < camion_entrante.tiempo_llegada:
                        camion_entrante = c
                t1 = camion_entrante.tiempo_llegada
            else:
                t1 = math.inf
            
            if len(self.camiones_en_reparacion) > 0:
                camion_saliente = self.camiones_en_reparacion[0]
                for c in self.camiones_en_reparacion:
                    if c.tiempo_salida < camion_saliente.tiempo_salida:
                        camion_saliente = c
                t2 = camion_saliente.tiempo_salida
            else:
                t2 = math.inf
                
            if t1 == math.inf and t2 == math.inf:
                break

            if t1 < t2:
                # Llegada de camión
                self.tiempo_actual = camion_entrante.tiempo_llegada
                self.camiones_en_operacion.remove(camion_entrante)

                # Buscamos una nave libre
                nave_libre = None
                for n in self.naves:
                    if n.esta_libre():
                        nave_libre = n
                        break

                if nave_libre != None:
                    # La nave está libre
                    nave_libre.reparar_camion(camion_entrante)
                    self.camiones_en_reparacion.append(camion_entrante)
                    camion_entrante.tiempo_reparacion = self.generar_tiempo_reparacion()
                    camion_entrante.tiempo_salida = self.tiempo_actual + camion_entrante.tiempo_reparacion
                
                else:
                    # La nave no está libre
                    self.camiones_en_espera.append(camion_entrante)

            else:
                # Salida de camión
                self.tiempo_actual = camion_saliente.tiempo_salida
                self.camiones_en_reparacion.remove(camion_saliente)
                camion_saliente.tiempo_reparacion = math.inf
                camion_saliente.tiempo_llegada = self.generar_tiempo_llegada() + self.tiempo_actual

                # Liberamos la nave
                for n in self.naves:
                    if n.camion == camion_saliente:
                        n.liberar_camion()
                        nave_libre = n
                        break

                self.camiones_en_operacion.append(camion_saliente)

                # Vemos si hay camiones en espera
                if len(self.camiones_en_espera) > 0:
                    camion_entrante = self.camiones_en_espera[0]
                    self.camiones_en_espera.remove(camion_entrante)
                    nave_libre.reparar_camion(camion_entrante)
                    self.camiones_en_reparacion.append(camion_entrante)
                    camion_entrante.tiempo_reparacion = self.generar_tiempo_reparacion()
                    camion_entrante.tiempo_salida = self.tiempo_actual + camion_entrante.tiempo_reparacion
                    
        # Fin de la simulación

    def mostrar_resultados(self):
        # Ordenamos self.histograma_de_camiones_en_operacion por tiempo
        self.histograma_de_camiones_en_operacion.sort(key=lambda x: x[1])
        # Queremos calcular el número promedio de camiones en operación
        promedio_por_mes = {}
        for tiempo in self.histograma_de_camiones_en_operacion:
            mes = int(tiempo[1])
            if mes in promedio_por_mes:
                promedio_por_mes[mes].append(tiempo[0])
            else:
                promedio_por_mes[mes] = [tiempo[0]]
        
        promedio_por_mes_final = {}
        for mes in promedio_por_mes:
            promedio_por_mes_final[mes] = sum(promedio_por_mes[mes]) / len(promedio_por_mes[mes])

        # Mostramos el promedio de todos los meses
        print(f"Promedio de camiones en operación: {sum(promedio_por_mes_final.values()) / len(promedio_por_mes_final)}")

        # Mostramos un histograma con el promedio de camiones en operación por mes
        # plt.figure(figsize=(10, 5))
        # plt.bar(promedio_por_mes_final.keys(), promedio_por_mes_final.values())
        # plt.xlabel("Mes")
        # plt.ylabel("Promedio de camiones en operación")
        # plt.show()
        
        # Mostramos un histograma con el número de camiones en operación por cada aparicion en self.histograma_de_camiones_en_operacion
        plt.figure(figsize=(10, 5))
        # Queremos que se dibuje una linea que una los puntos
        plt.plot([x[1] for x in self.histograma_de_camiones_en_operacion], [x[0] for x in self.histograma_de_camiones_en_operacion])
        plt.xlabel("Mes")
        plt.ylabel("Número de camiones en operación")
        # dibujamos la linea de promedio
        plt.axhline(y=sum(promedio_por_mes_final.values()) / len(promedio_por_mes_final), color='r', linestyle='-')
        plt.show()

        
        
        