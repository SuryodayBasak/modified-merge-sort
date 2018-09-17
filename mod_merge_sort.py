import numpy as np
import time
import random

#Procedure to check if the modified merge sort procedure worked or not
def check(A):
    for i in range(len(A) - 1):
        if (A[i] > A[i+1]):
            print("Array not sorted.")
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

#Original data to work with
A = np.random.uniform(-1,1,4000000)

#Genetic algorithm parameters
k_low = 1
k_high = 100
mut_rate = 0.5
sub_smpl_size = 100
pop_init = []
n_gens = 50
n_children = 100
n_parents = 40
best_k_ga = -1
best_k_exh = -1

#Implementing genetic algorithm
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
print("Best k = ", best_k_ga)

