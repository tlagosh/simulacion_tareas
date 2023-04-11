import threading
import logging
import random
import numpy as np
from classes import *

def simulator(N, lam, u_1, u_2, H=60):
    print("Simulating ...")

    results = []

    for i in range(N):
        seed = random.randint(1, 1000000)
        (NP, ESTOT) = simulate(lam, u_1, u_2, H, seed)
        results.append((NP, ESTOT))
        print(i+1, ": ", NP/ESTOT, ", ", NP)
    
    print("Done")
    print("PROMEDIO TOTAL: ", get_results(results)[0], ", ", get_results(results)[1])
    return get_results(results)

def simulate(lam, u_1, u_2, H, seed):

    random.seed(seed)

    caja_1 = Checkout(u_1) # caja 1
    caja_2 = Checkout(u_2) # caja 2

    t1 = float('inf') # tiempo de la proxima salida de la caja 1
    t2 = float('inf') # tiempo de la proxima salida de la caja 2
    t_next = np.random.poisson(1/lam) # tiempo de la proxima llegada de un cliente

    t = 0 # tiempo actual
    ESTOT = 0 # tiempo total en cola
    NCLIENTES = 0 # número de clientes atendidos
    Queue = [] # cola de clientes
    
    while t < H:
        
        if t_next <= t1 and t_next <= t2:
            t = t_next
            NCLIENTES += 1
            client = Client(t)
            if caja_1.bussy == False:
                caja_1.bussy = True
                caja_1.client = client
                t1 = t + random.expovariate(caja_1.u)
            elif caja_2.bussy == False:
                caja_2.bussy = True
                caja_2.client = client
                t2 = t + random.expovariate(caja_2.u)
            else:
                Queue.append(client)
            t_next = t + np.random.poisson(1/lam)
        elif t1 <= t_next and t1 <= t2:
            t = t1
            caja_1.bussy = False
            caja_1.client.queue_time = t - caja_1.client.arrival_time
            ESTOT = ESTOT + caja_1.client.queue_time
            if len(Queue) > 0:
                caja_1.bussy = True
                caja_1.client = Queue.pop(0)
                t1 = t + random.expovariate(caja_1.u)
            else:
                t1 = float('inf')
        elif t2 <= t_next and t2 <= t1:
            t = t2
            caja_2.bussy = False
            caja_2.client.queue_time = t - caja_2.client.arrival_time
            ESTOT = ESTOT + caja_2.client.queue_time
            if len(Queue) > 0:
                caja_2.bussy = True
                caja_2.client = Queue.pop(0)
                t2 = t + random.expovariate(caja_2.u)
            else:
                t2 = float('inf')
        else:
            print("Error")
            break
    
    return (NCLIENTES, ESTOT)

def get_results(results):
    PROM = 0
    NPROM = 0
    for result in results:
        N = result[0]
        ESTOT = result[1]
        NPROM = NPROM + N
        PROM = PROM + N/ESTOT
    return PROM/len(results), NPROM/len(results)

if __name__ == "__main__":

    lam = int(input("Ingrese lambda: "))
    u_1 = int(input("Ingrese u1: "))
    u_2 = int(input("Ingrese u2: "))
    N = int(input("Ingrese Número de simulaciones: "))

    is_interrupt_task = True
    testLoop = threading.Thread(target=simulator, args=(N, lam, u_1, u_2), daemon=is_interrupt_task)
    testLoop.start()

    logging.info('starting main loop ...')
    while True:  
        userinput = input()
        command = userinput.strip()

        if command == 'q':
            logging.info("main quits")
            break