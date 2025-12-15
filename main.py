import time
import random
import sys

# Importing all algorithms from our module
from algorithms import (
    naive_search, 
    rabin_karp_search, 
    kmp_search, 
    boyer_moore_search, 
    build_suffix_array, 
    suffix_array_search, 
    build_bloom_filter
)

# Helper function to generate random DNA sequence
def generate_dna(length):
    return ''.join(random.choice('ACGT') for _ in range(length))

if _name_ == "_main_":
    print("\n" + "="*60)
    print("       🧬 BioPattern: Algorithm Performance Analysis       ")
    print("="*60 + "\n")
    
    # PARAMETERS
    GENOME_SIZE = 50_000  # Size of the DNA sequence
    PATTERN = "ACGTAC"    # The pattern we are looking for
    
    print(f"[*] Generating dataset ({GENOME_SIZE} base pairs)...")
    genome_data = generate_dna(GENOME_SIZE)
    print(f"[*] Target Pattern: {PATTERN}")
    print("-" * 60)

    # --- 1. NAIVE SEARCH ---
    print("[1] Running Naive Search (Brute Force)...")
    start = time.time()
    matches_naive = naive_search(PATTERN, genome_data)
    dur_naive = time.time() - start
    print(f"    Matches: {len(matches_naive)}")
    print(f"    Time   : {dur_naive:.5f} sec")
    print("-" * 60)

    # --- 2. RABIN-KARP ---
    print("[2] Running Rabin-Karp (Rolling Hash)...")
    start = time.time()
    matches_rk = rabin_karp_search(PATTERN, genome_data)
    dur_rk = time.time() - start
    print(f"    Matches: {len(matches_rk)}")
    print(f"    Time   : {dur_rk:.5f} sec")
    print("-" * 60)

    # --- 3. KMP SEARCH ---
    print("[3] Running Knuth-Morris-Pratt (KMP)...")
    start = time.time()
    matches_kmp = kmp_search(PATTERN, genome_data)
    dur_kmp = time.time() - start
    print(f"    Matches: {len(matches_kmp)}")
    print(f"    Time   : {dur_kmp:.5f} sec")
    print("-" * 60)

    # --- 4. BOYER-MOORE ---
    print("[4] Running Boyer-Moore (Smart Search)...")
    start = time.time()
    matches_bm = boyer_moore_search(PATTERN, genome_data)
    dur_bm = time.time() - start
    print(f"    Matches: {len(matches_bm)}")
    print(f"    Time   : {dur_bm:.5f} sec")
    print("-" * 60)

    # --- 5. SUFFIX ARRAY ---
    print("[5] Suffix Array (Indexing + Search)...")
    
    # Build Phase
    t0 = time.time()
    sa = build_suffix_array(genome_data)
    build_time = time.time() - t0
    
    # Search Phase
    t1 = time.time()
    matches_sa = suffix_array_search(PATTERN, genome_data, sa)
    search_time = time.time() - t1
    
    print(f"    Build Time : {build_time:.5f} sec")
    print(f"    Search Time: {search_time:.5f} sec")
    print(f"    Matches    : {len(matches_sa)}")
    print("-" * 60)

    # --- 6. BLOOM FILTER ---
    print("[6] Bloom Filter (Probabilistic Check)...")
    
    t0 = time.time()
    bf = build_bloom_filter(genome_data, len(PATTERN))
    bf_build_time = time.time() - t0
    
    t1 = time.time()
    exists = bf.check(PATTERN)
    bf_check_time = time.time() - t1
    
    print(f"    Build Time : {bf_build_time:.5f} sec")
    print(f"    Check Time : {bf_check_time:.5f} sec")
    print(f"    Exists?    : {'YES (Probable)' if exists else 'NO'}")
    
    print("=" * 60)
    print("DONE. All algorithms benchmarked successfully.")