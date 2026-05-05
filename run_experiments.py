import argparse
import time
import random
import numpy as np
import matplotlib.pyplot as plt


#Bubble Sort: simple comparison and swap
def bubble_sort(arr):
    for i in range (len(arr)-1):
        # push the largest element to the end of the array
        for j in range(len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]  # swap elements
    return arr

#Insertion Sort: builds the sorted array one element at a time
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        # shift elements to the right to make room for the key
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

#Merge Sort: divide and conquer approach
def merge_sort(arr):
    # base case: array of size 0 or 1 is already sorted
    if len(arr) <= 1:
        return arr
    # split the array into two halves
    mid = len(arr)//2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    return merge(left_half, right_half)

def merge(left, right):
    result = []
    i = j = 0
    # compare elements from left and right lists
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else :
            result.append(right[j])
            j += 1
    # add any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# generate data for the experiments
def generate_data(size, exp_type):
    # experiment 0: Completely random numbers
    if exp_type == 0:
        result = []
        for _ in range(size):
            number = random.randint(0, 1000000)
            result.append(number)
        return result
    # experiment 1 or 2: Nearly sorted arrays with noise
    arr = list(range(size))
    noise_percent = 5 if exp_type == 1 else 20
    num_swaps = int(size * (noise_percent / 100))
    # add random swaps to create the noise
    for _ in range(num_swaps):
        idx1, idx2 = random.sample(range(size), 2)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]

    return arr


if __name__ == "__main__":
    # setup command line arguments
    parser = argparse.ArgumentParser(description='Run sorting experiments.')
    parser.add_argument('-a', '--algorithms', nargs='+', type=int, required=True, help='List of algorithm IDs (1-Bubble, 2-Insertion, 3-Merge)')
    parser.add_argument('-s', '--sizes', nargs='+', type=int, required=True, help='List of array sizes')
    parser.add_argument('-e', '--experiment', type=int, required=True, help='1: 5%% noise, 2: 20%% noise, 0: Random')
    parser.add_argument('-r', '--repetitions', type=int, default=1, help='Number of repetitions for each experiment')
    args = parser.parse_args()

    # map algorithm IDs to the actual functions
    sort_functions = {
        1: bubble_sort,
        3: insertion_sort,
        4: merge_sort
    }
    # dictionaries to store mean runtimes and standard deviations
    final_means = {alg_id: [] for alg_id in args.algorithms}
    final_stds = {alg_id: [] for alg_id in args.algorithms}
    # main experiment loop
    for size in args.sizes:
        print(f"--- Testing Size: {size} ---")
        for alg_id in args.algorithms:
            run_times = []
            # run the experiment multiple times for better accuracy
            for rep in range(args.repetitions):
                data = generate_data(size, args.experiment)
                # measure the time
                start_time = time.perf_counter()
                sort_functions[alg_id](data)
                end_time = time.perf_counter()
                run_times.append(end_time - start_time)
            # calculate statistics using numpy
            avg_time = np.mean(run_times)
            std_time = np.std(run_times)
            final_means[alg_id].append(avg_time)
            final_stds[alg_id].append(std_time)

            print(f"{sort_functions[alg_id].__name__}: Avg={avg_time:.5f}s, Std={std_time:.5f}s")

    # create the final performance plot
    plt.figure(figsize=(10, 6))
    for alg_id in args.algorithms:
        means = np.array(final_means[alg_id])
        stds = np.array(final_stds[alg_id])
        plt.plot(args.sizes, means, label=sort_functions[alg_id].__name__, marker='o')
        # add shaded area for standard deviation
        plt.fill_between(args.sizes, means - stds, means + stds, alpha=0.2)

    plt.xlabel('Array Size (n)')
    plt.ylabel('Time (seconds)')
    plt.title(f'Performance - Experiment {args.experiment}')
    plt.legend()
    plt.grid(True)
    # save the file with the correct name (result1.png or result2.png)
    plt.savefig(f'result{1 if args.experiment == 0 else 2}.png')
    plt.show()