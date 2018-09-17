import numpy as np

def check(A):
    for i in range(len(A) - 1):
        if (A[i] > A[i+1]):
            print("Array not sorted.")
            return -1
    print("OK.")

def insertion_sort(A, p, r):
    #print(A[p:r])
    for j in range(p+1, r):
        key = A[j]
        #Insert A[j] into the sorted sequence A[0...j-1]
        i = j-1

        while ((i >= p) and (A[i] > key)):
            #print(i+j)
            A[i+1] = A[i]
            i = i-1
        A[i + 1] = key
    #print(A[p:r])
    #print()

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

def merge_sort(A, p, r, k):

    #print('p+k=', p+k)
    #print('r = ', r)
    #print()
    if (r-p <= k):
        insertion_sort(A, p, r+1)
   
    elif p < r:
        q = int((p+r)/2)
        merge_sort(A, p, q, k)
        merge_sort(A, q+1, r, k)
        merge(A, p, q, r)

k = 4
A = [1000, 99, 6462, 11, 7, 44, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 99, 6462, 11, 7, 44, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
A = np.random.uniform(-1,0,400000)
print(A)
merge_sort(A, 0, len(A)-1, k)
print(A)
check(A)
