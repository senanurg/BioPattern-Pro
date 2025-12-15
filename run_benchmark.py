import time
import random
import os
# Yeni algoritmayı da import ediyoruz
from algorithms import naive_search, build_suffix_array, suffix_array_search, build_bloom_filter, boyer_moore_search
from visualization import plot_performance

def generate_dna_to_file(length, filename="genome_data.txt"):
    """
    DNA verisini oluşturur ve bir dosyaya kaydeder.
    Böylece veriyi gözle görebiliriz.
    """
    dna_data = ''.join(random.choice('ACGT') for _ in range(length))
    
    # Dosyaya yazma işlemi
    with open(filename, "w") as f:
        f.write(dna_data)
    
    print(f"-> Veri oluşturuldu ve '{filename}' dosyasına kaydedildi.")
    return dna_data

def read_dna_from_file(filename="genome_data.txt"):
    with open(filename, "r") as f:
        return f.read()

if _name_ == "_main_":
    print("\n--- BioPattern: Starting Benchmark Suite ---")
    
    # Adım 1: Test Edilecek Boyutlar
    # Boyer-Moore hızlı olduğu için boyutu biraz daha artırabiliriz
    genome_sizes = [5000, 10000, 20000, 40000, 60000]
    
    naive_times = []
    bm_times = []      # Boyer-Moore için liste
    sa_search_times = []
    bf_check_times = []

    pattern = "ACGTAC"
    
    print(f"Aranan Desen: {pattern}")
    print("Veriler dosyalara kaydedilecek ve oradan okunacak...\n")

    for size in genome_sizes:
        print(f"Processing Genome Size: {size}...")
        
        # 1. Veriyi dosyaya kaydet (Görmek istiyordun)
        filename = f"test_genome_{size}.txt"
        text = generate_dna_to_file(size, filename)
        
        # 2. Measure Naive
        start = time.time()
        naive_search(pattern, text)
        naive_times.append(time.time() - start)
        
        # 3. Measure Boyer-Moore (YENİ!)
        start = time.time()
        boyer_moore_search(pattern, text)
        bm_times.append(time.time() - start)
        
        # 4. Measure Suffix Array
        sa = build_suffix_array(text) 
        start = time.time()
        suffix_array_search(pattern, text, sa)
        sa_search_times.append(time.time() - start)
        
        # 5. Measure Bloom Filter
        bf = build_bloom_filter(text, len(pattern))
        start = time.time()
        bf.check(pattern)
        bf_check_times.append(time.time() - start)
        
        # Temizlik: Test dosyasını silmeyelim ki açıp bakabilesin.
        # os.remove(filename) 

    print("\nBenchmark completed!")
    print("Launching Graph...")
    
    # Grafik çizdirme fonksiyonunu çağırırken yeni veriyi de gönderelim
    # (Bunun için visualization.py dosyasını da güncellememiz gerekecek!)
    
    # Geçici olarak burada grafiği yeniden tanımlayalım ki visualization.py ile uğraşma
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    
    plt.plot(genome_sizes, naive_times, label='Naive Search', color='red', marker='o', linestyle='--')
    plt.plot(genome_sizes, bm_times, label='Boyer-Moore (Smart)', color='orange', marker='D') # YENİ
    plt.plot(genome_sizes, sa_search_times, label='Suffix Array (Indexed)', color='blue', marker='s')
    plt.plot(genome_sizes, bf_check_times, label='Bloom Filter', color='green', marker='^')
    
    plt.title('BioPattern: Algorithm Performance Comparison')
    plt.xlabel('Genome Size (Base Pairs)')
    plt.ylabel('Time (Seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('final_result_with_BM.png')
    plt.show()