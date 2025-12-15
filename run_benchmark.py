import time
import random
import os
import matplotlib.pyplot as plt

# Import our algorithms
from algorithms import naive_search, build_suffix_array, suffix_array_search, build_bloom_filter, boyer_moore_search

def generate_dna_to_file(length, filename="genome_data.txt"):
    """
    Generates DNA data and saves it to a file.
    This allows visual inspection of the generated data.
    """
    dna_data = ''.join(random.choice('ACGT') for _ in range(length))
    
    # Write to file
    with open(filename, "w") as f:
        f.write(dna_data)
    
    print(f"-> Data generated and saved to '{filename}'.")
    return dna_data

def read_dna_from_file(filename="genome_data.txt"):
    with open(filename, "r") as f:
        return f.read()

if __name__ == "__main__":
    print("\n--- BioPattern: Starting Benchmark Suite ---")
    
    # Step 1: Define Genome Sizes to Test
    # Since Boyer-Moore is fast, we can test with larger sizes compared to just Naive.
    genome_sizes = [5000, 10000, 20000, 40000, 60000]
    
    # Lists to store timing results
    naive_times = []
    bm_times = []      
    sa_search_times = []
    bf_check_times = []

    pattern = "ACGTAC"
    
    print(f"Pattern to Search: {pattern}")
    print("Data will be generated, saved to files, and processed...\n")

    for size in genome_sizes:
        print(f"Processing Genome Size: {size}...")
        
        # 1. Generate and Save Data (So you can see the file)
        filename = f"test_genome_{size}.txt"
        text = generate_dna_to_file(size, filename)
        
        # 2. Measure Naive Search
        start = time.time()
        naive_search(pattern, text)
        naive_times.append(time.time() - start)
        
        # 3. Measure Boyer-Moore (Smart Search)
        start = time.time()
        boyer_moore_search(pattern, text)
        bm_times.append(time.time() - start)
        
        # 4. Measure Suffix Array (Indexing + Search)
        # Note: We measure search time, assuming index is built once.
        sa = build_suffix_array(text) 
        start = time.time()
        suffix_array_search(pattern, text, sa)
        sa_search_times.append(time.time() - start)
        
        # 5. Measure Bloom Filter (Probabilistic Check)
        bf = build_bloom_filter(text, len(pattern))
        start = time.time()
        bf.check(pattern)
        bf_check_times.append(time.time() - start)
        
        # Cleanup: We keep the file so you can inspect it if needed.
        # os.remove(filename) 

    print("\nBenchmark completed!")
    print("Launching Graph...")
    
    # Define plotting logic here temporarily to include all new metrics
    plt.figure(figsize=(10, 6))
    
    plt.plot(genome_sizes, naive_times, label='Naive Search', color='red', marker='o', linestyle='--')
    plt.plot(genome_sizes, bm_times, label='Boyer-Moore (Smart)', color='orange', marker='D')
    plt.plot(genome_sizes, sa_search_times, label='Suffix Array (Indexed)', color='blue', marker='s')
    plt.plot(genome_sizes, bf_check_times, label='Bloom Filter', color='green', marker='^')
    
    plt.title('BioPattern: Algorithm Performance Comparison')
    plt.xlabel('Genome Size (Base Pairs)')
    plt.ylabel('Time (Seconds)')
    plt.legend()
    plt.grid(True)
    
    # Save the result
    plt.savefig('final_result_with_BM.png')
    print("Graph saved as 'final_result_with_BM.png'")
    
    # Show the plot
    plt.show()