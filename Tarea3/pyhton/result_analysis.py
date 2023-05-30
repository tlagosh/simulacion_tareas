import math

def read_file(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()
    return lines

def preprocess_results(results):
    
    new_results = []

    for result in results:
        N = result[0]
        ESTOT = result[1]
        new_results.append(N/ESTOT)
    
    return new_results

def get_mean(results):
    s = 0
    for result in results:
        s = s + result
    return s/len(results)

def get_confidence_interval(results, u):

    n = len(results) # Sacamos el numero de simulaciones
    s = 0 
    for result in results:
        s = s + (result - u)**2
    s = math.sqrt(s/(n-1)) # Sacamos la desviacion estandar
    t = 1.96 # t-student value for 95% confidence interval
    return (u - t*s/math.sqrt(n), u + t*s/math.sqrt(n)) # Sacamos el intervalo de confianza

def get_mean_error(results, prom):
    n = len(results)
    s = 0 
    for result in results:
        s = s + (result - prom)**2
    s = math.sqrt(s/(n-1)) # Sacamos la desviacion estandar
    return s/math.sqrt(n) # Sacamos el error como la desviacion estandar sobre la raiz de n

def get_percentile_80(results):
    results.sort()
    indice_80 = math.ceil(len(results)*0.8)
    return results[indice_80 - 1]

def get_percentile_confidence_interval(results, percentile, alpha):
    
    # P{Xi < q < Xj} = 1 - alpha
    # buscamos i y j tal que P{Xi < q < Xj} = 1 - alpha

    indice_80 = math.ceil(len(results)*0.8)

    def get_probability(i, j, k):
        suma = 0
        for l in range(i, j):
            suma += math.comb(k, l) * (percentile**l) * ((1-percentile)**(k-l))
        return suma
    
    n = len(results)
    i = indice_80 - 1
    j = indice_80 + 1
    increment = 1
    while True:
        if get_probability(i, j, n) < alpha:
            if i > 0 and increment == 1:
                i = i - 1
            if j < n and increment == -1:
                j = j + 1
            increment = -increment
        else:
            break
    
    print(i, " - ", indice_80, " - ", j)

    return (results[i - 1], results[j - 1])

def get_relative_error(x_i, x_j, qp):
    return (x_j - x_i)/(2*qp)

if __name__ == "__main__":

    # We read the results from the file
    lines = read_file("results.txt")
    results = []
    for line in lines:
        results.append([float(x) for x in line.split("(")[1].split(")")[0].split(",")])

    results = preprocess_results(results)
    # We calculate the confidence interval
    u = get_mean(results)
    x_1, x_2 = get_confidence_interval(results, u)
    print("Confidence interval: ", u, " +- ", x_2 - u)
    print("Mean error: ", get_mean_error(results, u))

    percentile_80 = get_percentile_80(results)
    print("Percentile 80: ", percentile_80)
    x_1, x_2 = get_percentile_confidence_interval(results, 0.8, 0.05)
    print("Percentile confidence interval: ", x_1, " - ", x_2)
    print("Relative error: ", get_relative_error(x_1, x_2, percentile_80))



