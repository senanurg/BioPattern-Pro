import matplotlib.pyplot as plt

def plot_performance(sizes, naive_times, bm_times, sa_search_times, bf_check_times):
    """
    Draws a line chart comparing the search times of different algorithms.
    
    Arguments:
    sizes -- List of genome sizes tested
    naive_times -- Execution times for Naive Search
    bm_times -- Execution times for Boyer-Moore
    sa_search_times -- Execution times for Suffix Array Search
    bf_check_times -- Execution times for Bloom Filter Check
    """
    plt.figure(figsize=(10, 6))
    
    # 1. Naive Search Line (Red - Baseline)
    plt.plot(sizes, naive_times, label='Naive Search (Brute Force)', 
             color='red', marker='o', linestyle='--')

    # 2. Boyer-Moore Line (Orange - Smart Search)
    plt.plot(sizes, bm_times, label='Boyer-Moore (Smart Search)', 
             color='orange', marker='D')
    
    # 3. Suffix Array Search Line (Blue - Indexed)
    plt.plot(sizes, sa_search_times, label='Suffix Array Search (Indexed)', 
             color='blue', marker='s')
    
    # 4. Bloom Filter Check Line (Green - Probabilistic)
    plt.plot(sizes, bf_check_times, label='Bloom Filter (Probabilistic)', 
             color='green', marker='^')
    
    # Graph Settings
    plt.title('BioPattern: Algorithm Search Time vs Genome Size')
    plt.xlabel('Genome Size (Base Pairs)')
    plt.ylabel('Execution Time (Seconds)')
    plt.legend() # Shows the labels
    plt.grid(True) # Adds a grid for easier reading
    
    # Save the graph to a file
    plt.savefig('performance_result.png')
    print("Graph saved as 'performance_result.png'")
    
    # Show the graph on screen
    plt.show()