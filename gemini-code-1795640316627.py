import math
import random
import time


def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key



def heapify(arr, n, i, offset):
    largest = i
    left_child = 2 * i + 1
    right_child = 2 * i + 2

    if (
        left_child < n
        and arr[offset + left_child] > arr[offset + largest]
    ):
        largest = left_child

    if (
        right_child < n
        and arr[offset + right_child] > arr[offset + largest]
    ):
        largest = right_child

    if largest != i:
        arr[offset + i], arr[offset + largest] = (
            arr[offset + largest],
            arr[offset + i],
        )
        heapify(arr, n, largest, offset)



def heapsort(arr, left, right):
    n = right - left + 1

    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, left)

    
    for i in range(n - 1, 0, -1):
        arr[left], arr[left + i] = arr[left + i], arr[left]
        heapify(arr, i, 0, left)



def median_of_three(arr, a, b, c):
    if (arr[a] <= arr[b] <= arr[c]) or (arr[c] <= arr[b] <= arr[a]):
        return b
    elif (arr[b] <= arr[a] <= arr[c]) or (arr[c] <= arr[a] <= arr[b]):
        return a
    else:
        return c


def partition(arr, low, high):
    mid = (low + high) // 2
    pivot_idx = median_of_three(arr, low, mid, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1



def introsort_util(arr, low, high, max_depth, cutoff=16):
    size = high - low + 1

    
    if size <= cutoff:
        insertion_sort(arr, low, high)
        return

    
    if max_depth == 0:
        heapsort(arr, low, high)
        return

    
    pivot = partition(arr, low, high)
    introsort_util(arr, low, pivot - 1, max_depth - 1, cutoff)
    introsort_util(arr, pivot + 1, high, max_depth - 1, cutoff)



def introsort(arr):
    if len(arr) <= 1:
        return arr
    
    max_depth = 2 * math.floor(math.log2(len(arr)))
    introsort_util(arr, 0, len(arr) - 1, max_depth)
    return arr



if __name__ == "__main__":
    n = 50000
    datasets = {
        "Random Array": [random.randint(0, 1_000_000) for _ in range(n)],
        "Already Sorted (Worst-case for naive Quicksort)": list(range(n)),
        "Reverse Sorted": list(range(n, 0, -1)),
    }

    print(f"Benchmarking Introsort on {n} elements:\n")
    for name, data in datasets.items():
        arr_copy = data.copy()
        start = time.perf_counter()
        introsort(arr_copy)
        elapsed = time.perf_counter() - start

        assert arr_copy == sorted(data), f"Failed on {name}"
        print(f"{name:<50} -> {elapsed:.6f} sec")