def insertion_sort(A):
    for j in range(1, len(A)):
        key = A[j]
        #Insert A[j] into the sorted sequence A[0...j-1]
        i = j-1

        while ((i >= 0) and (A[i] > key)):
            #print(i+j)
            A[i+1] = A[i]
            i = i-1
        A[i + 1] = key

A = [10, 8, 6, 4, 2, 0, 9, 7, 5, 3, 1]
print(A)
insertion_sort(A)
print(A)
