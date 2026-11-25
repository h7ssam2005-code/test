import random
import time
import matplotlib.pyplot as plt



def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key



def merge(arr, left, mid, right):
    left_part = arr[left : mid + 1]
    right_part = arr[mid + 1 : right + 1]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1



def hybrid_sort(arr, left, right, cutoff):
    if left < right:
        # Switch to Insertion Sort when subarray size is <= cutoff (k)
        if (right - left + 1) <= cutoff:
            insertion_sort(arr, left, right)
        else:
            mid = (left + right) // 2
            hybrid_sort(arr, left, mid, cutoff)
            hybrid_sort(arr, mid + 1, right, cutoff)
            merge(arr, left, mid, right)


def find_best_cutoff(array_size=50000, k_values=None, trials=3):
    if k_values is None:
        # Test cutoff values from 1 (pure Merge Sort) up to 100
        k_values = [1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 50, 64, 80, 100]

    base_array = [random.randint(0, 1_000_000) for _ in range(array_size)]
    results = {}

    print(
        f"Testing array size {array_size} (average of {trials} trials per k)...\n"
    )
    print(f"{'Cutoff (k)':<15} | {'Avg Time (sec)':<15}")
    print("-" * 34)

    for k in k_values:
        total_time = 0.0
        for _ in range(trials):
            arr_copy = base_array.copy()
            start_time = time.perf_counter()
            hybrid_sort(arr_copy, 0, len(arr_copy) - 1, k)
            end_time = time.perf_counter()
            total_time += end_time - start_time

        
            assert arr_copy == sorted(base_array), f"Sorting failed for k={k}"

        avg_time = total_time / trials
        results[k] = avg_time
        print(f"{k:<15} | {avg_time:.6f}")

    best_k = min(results, key=results.get)
    print("-" * 34)
    print(
        f"\nBest Cutoff (k): {best_k} with an average time of {results[best_k]:.6f}s"
    )
    print(f"Pure Merge Sort (k=1) average time: {results[1]:.6f}s")

    return results, best_k


def plot_results(results, best_k):
    k_vals = list(results.keys())
    times = list(results.values())

    plt.figure(figsize=(10, 5))
    plt.plot(k_vals, times, marker="o", linestyle="-", color="#2563eb")
    plt.axvline(
        x=best_k, color="red", linestyle="--", label=f"Best k = {best_k}"
    )
    plt.title("Hybrid Sort Performance: Finding Optimal Cutoff (k)")
    plt.xlabel("Cutoff Size (k)")
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results, best_k = find_best_cutoff(array_size=50000, trials=3)

    try:
        plot_results(results, best_k)
    except ImportError:
        print("\nInstall matplotlib to display the plot: pip install matplotlib")