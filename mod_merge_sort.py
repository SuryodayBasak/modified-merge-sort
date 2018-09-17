import numpy as np
import time
import random

#Procedure to check if the modified merge sort procedure worked or not
def check(A):
    for i in range(len(A) - 1):
        if (A[i] > A[i+1]):
            #print("Array not sorted.")
            return -1
    return 0

#Insertion sort procedure
def insertion_sort(A, p, r):
    for j in range(p+1, r):
        key = A[j]
        #Insert A[j] into the sorted sequence A[0...j-1]
        i = j-1

        while ((i >= p) and (A[i] > key)):
            #print(i+j)
            A[i+1] = A[i]
            i = i-1
        A[i + 1] = key

#Merge procedure
def merge(A, p, q, r):
    n1 = q-p+1
    n2 = r-q

    L = []
    R = []

    for i in range(0, n1):
        L.append(A[p+i])

    for j in range(0, n2):
        R.append(A[q+j+1])

    L.append(99999)
    R.append(99999)
    
    i = 0
    j = 0

    for k in range (p, r+1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i = i + 1
        else:
            A[k] = R[j]
            j = j + 1

#Merge sort procedure but there is insertion sort for sublists of size less than a constant k
def merge_sort(A, p, r, k):
    if (r-p <= k):
        insertion_sort(A, p, r+1)
   
    elif p < r:
        q = int((p+r)/2)
        merge_sort(A, p, q, k)
        merge_sort(A, q+1, r, k)
        merge(A, p, q, r)

#Genetic algorithm crossover procedure
def crossover(k1, k2, mut_rate):
    op = np.random.choice([-1, 1], size=(1), p=[1./2, 1./2])[0]
    k_child = (k1 + k2)/2 + (op*mut_rate)
    return k_child


#GA params
k_low = 1
k_high = 20
mut_rate = 0.5
sub_smpl_size = 1000
n_gens = 10
n_children = 300
n_parents = 100
n_runs = 15


print('best_k_ga, avg_t_ga, ga_total_time, best_k_exh, avg_t_exh, exh_total_time')
for ITER in range(0,20):
    #Original data to work with
    A = np.random.uniform(-1,1,400000)

    #Genetic algorithm data and results 
    pop_init = []
    best_k_ga = -1
    best_k_exh = -1
    avg_t_ga = -1
    avg_t_exh = -1
    total_t_ga = -1
    total_t_exh = -1

    #Implementing genetic algorithm
    time_ga_start = time.time()
    #Population initializaton:
    for i in range(0, n_children):
        k = int(np.random.uniform(k_low, k_high))
        #print(k)
        A1 = [A[i] for i in sorted(random.sample(range(len(A)), sub_smpl_size))]
        start_time = time.time()
        merge_sort(A1, 0, len(A1)-1, k)
        t = time.time() - start_time
        #print("Time = ", t)
        pop_init.append([t, k])
        if check(A1) == -1:
            print("Array not sorted.")

    pop_init = sorted(pop_init)
    parents = pop_init

    for i in range(n_gens):
        parents = parents[0:n_parents]
        #print(parents)
        cur_pop = []
        for j in range(n_children):
            k1_ind = int(np.random.uniform(0, n_parents))
            k2_ind = int(np.random.uniform(0, n_parents))
            k1 = parents[k1_ind][1]
            k2 = parents[k2_ind][1]
            k = crossover(k1, k2, mut_rate)

            A1 = [A[i] for i in sorted(random.sample(range(len(A)), sub_smpl_size))]
            start_time = time.time()
            merge_sort(A1, 0, len(A1)-1, k)
            t = time.time() - start_time
            #print("Time = ", t)
            cur_pop.append([t, k])
            if check(A1) == -1:
                print("Array not sorted.")
        parents = sorted(cur_pop)
        #print(parents[1])

    best_k_ga = int(parents[0][1])

    #print("Best k by GA= ", best_k_ga, "\tTime = ", parents[0][0])
    del parents
    del pop_init
    time_ga_end = time.time()

    #Implementing exhaustive search method to determine the best value of k
    time_exh_start = time.time()
    results_exh = []
    for k in range(k_low, k_high):
        #print(k)
        #print("Checking A")
        #if check(A) == -1:
        #    print("A is not sorted")
        A_cpy = A.copy()
        start_time = time.time()
        merge_sort(A_cpy, 0, len(A_cpy)-1, k)
        t = time.time() - start_time
        results_exh.append([t, k])
        if check(A_cpy) == -1:
            print("Array not sorted.")
        #print()
        del A_cpy
    results_exh = sorted(results_exh)
    #print(results_exh[0])
    best_k_exh = results_exh[0][1]

    #Rechecking GA
    for i in range(0, n_runs):
        A_cpy = A.copy()
        start_time = time.time()
        merge_sort(A_cpy, 0, len(A_cpy)-1,best_k_ga)
        total_time = time.time() - start_time
        del A_cpy
    avg_t_ga = total_time/n_runs

    #Rechecking exhaustive search 
    for i in range(0, n_runs):
        A_cpy = A.copy()
        start_time = time.time()
        merge_sort(A_cpy, 0, len(A_cpy)-1,best_k_exh)
        total_time = time.time() - start_time
        del A_cpy
    avg_t_exh = total_time/n_runs
    time_exh_end = time.time()

    print(best_k_ga, ',', avg_t_ga, ',', time_ga_end-time_ga_start,',', best_k_exh, ',', avg_t_exh, ',',time_exh_end-time_exh_start)
