import threading
import logging
import random
import numpy as np
from classes import *
import matplotlib.pyplot as plt
import math

def simulator(N, h, trans, lam, u_1, u_2, H=60):
    print("Simulating ...")

    results = []

    for i in range(N):
        seed = random.randint(1, 1000000)
        (NP, ESTOT, stats, happy_customers) = simulate(h, trans, lam, u_1, u_2, H, seed)
        results.append((NP, ESTOT))
        print(i+1, ": ", NP/ESTOT, ", ", NP)
    
    print("Done")
    print("PROMEDIO TOTAL: ", get_results(results)[0], ", ", get_results(results)[1])
    #get_stats(results)
    x_1, u, x_2 = get_confidence_interval(results)
    print("CONFIDENCE INTERVAL: ", u, " +/- ", x_2 - u)

    mean_error = get_mean_error(results, u)
    print("MEAN ERROR: ", mean_error)

    return results

def simulate(h, trans, lam, u_1, u_2, H, seed):

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

    happy_customers = []

    stats = []
    
    while t < h:

        if t > trans:
            stats.append((t, caja_1.bussy, caja_2.bussy, len(Queue), ESTOT, NCLIENTES))
        
        if t_next <= t1 and t_next <= t2:
            t = t_next
            if t > trans:
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
            caja_1.client.departure_time = t
            if t > trans:
                ESTOT = ESTOT + caja_1.client.queue_time
                happy_customers.append(caja_1.client)
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
            caja_2.client.departure_time = t
            if t > trans:
                ESTOT = ESTOT + caja_2.client.queue_time
                happy_customers.append(caja_2.client)
            if len(Queue) > 0:
                caja_2.bussy = True
                caja_2.client = Queue.pop(0)
                t2 = t + random.expovariate(caja_2.u)
            else:
                t2 = float('inf')
        else:
            print("Error")
            break
    
    return (NCLIENTES, ESTOT, stats, happy_customers)

def get_results(results):
    PROM = 0
    NPROM = 0
    for result in results:
        N = result[0]
        ESTOT = result[1]
        NPROM = NPROM + N
        PROM = PROM + N/ESTOT
    return PROM/len(results), NPROM/len(results)

def get_stats(results):
    # We make an histogram of the queue length
    hist = []
    for result in results:
        happy_customers = result[3]
        for client in happy_customers:
            hist.append((client.departure_time, client.queue_time))
    hist.sort(key=lambda tup: tup[0])
    print(len(hist))
    # We group the clients in 100 groups based on their departure time
    # and calculate the average queue time for each group
    groups = []
    group = []
    i = 0
    for client in hist:
        if i == math.floor(len(hist)/500):
            groups.append(group)
            group = []
            i = 0
        group.append(client)
        i += 1
    groups.append(group)
    # We calculate the average queue time adn departure time for each group
    avg_queue_time = []
    avg_departure_time = []
    for group in groups:
        avg_queue_time.append(sum([x[1] for x in group])/len(group))
        avg_departure_time.append(sum([x[0] for x in group])/len(group))
    # We plot the results, the plot shows the average queue time for each group of clients
    # the plot must show a line that unites all the points
    # We put a vertical time on the point where the departure time is 100 minutes
    plt.plot(avg_departure_time, avg_queue_time)
    plt.show()

# We make a function that gets the confidence interval of the average queue time
# We use the t-student distribution

def get_confidence_interval(results):
    PROM = 0
    NPROM = 0
    for result in results:
        N = result[0]
        ESTOT = result[1]
        NPROM = NPROM + N
        PROM = PROM + N/ESTOT
    prom = PROM/len(results)
    n = len(results)
    s = 0
    for result in results:
        N = result[0]
        ESTOT = result[1]
        s = s + (N/ESTOT - prom)**2
    s = math.sqrt(s/(n-1))

    t = 1.96 # t-student value for 95% confidence interval

    return (prom - t*s/math.sqrt(n), prom, prom + t*s/math.sqrt(n))

def get_mean_error(results, prom):
    n = len(results)
    s = 0
    for result in results:
        N = result[0]
        ESTOT = result[1]
        s = s + (N/ESTOT - prom)**2
    s = math.sqrt(s/(n-1))
    return s/math.sqrt(n)

if __name__ == "__main__":

    h = int(input("Ingrese H: "))
    trans = int(input("Ingrese el periodo Transiente: "))
    lam = 20 #int(input("Ingrese lambda: "))
    u_1 = 12 #int(input("Ingrese u1: "))
    u_2 = 10 #int(input("Ingrese u2: "))
    N = int(input("Ingrese Número de simulaciones: "))

    results = simulator(N, h, trans, lam, u_1, u_2)

    # We save the results in a file
    with open('results.txt', 'w') as f:
        for result in results:
            f.write(str(result) + '\n')