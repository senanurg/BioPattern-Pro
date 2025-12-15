import time
import random
from algorithms import naive_search, build_suffix_array, suffix_array_search, build_bloom_filter
from visualization import plot_performance

def generate_dna(length):
    return ''.join(random.choice('ACGT') for _ in range(length))

if __name__ == "__main__":
    print("\n--- BioPattern: Starting Benchmark Suite ---")
    print("Collecting data for visualization... (This may take ~30 seconds)\n")

    # Test yapılacak farklı genom boyutları
    # Not: Suffix Array build süresi uzun olduğu için en fazla 40.000-50.000 yapıyoruz.
    genome_sizes = [5000, 10000, 20000, 30000, 40000]
    
    # Sonuçları saklayacağımız listeler
    naive_times = []
    sa_search_times = []
    bf_check_times = []

    pattern = "ACGTAC"

    for size in genome_sizes:
        print(f"Processing Genome Size: {size}...")
        text = generate_dna(size)
        
        # 1. Measure Naive
        start = time.time()
        naive_search(pattern, text)
        naive_times.append(time.time() - start)
        
        # 2. Measure Suffix Array (Only Search Time)
        # We build it first (setup cost), then measure search speed
        sa = build_suffix_array(text) 
        start = time.time()
        suffix_array_search(pattern, text, sa)
        sa_search_times.append(time.time() - start)
        
        # 3. Measure Bloom Filter
        bf = build_bloom_filter(text, len(pattern))
        start = time.time()
        bf.check(pattern)
        bf_check_times.append(time.time() - start)

    print("\nBenchmark completed!")
    print("Launching Graph...")
    
    # Grafiği çiz
    plot_performance(genome_sizes, naive_times, sa_search_times, bf_check_times)