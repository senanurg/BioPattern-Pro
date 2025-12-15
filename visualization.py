import matplotlib.pyplot as plt

def plot_performance(sizes, naive_times, sa_search_times, bf_check_times):
    """
    Draws a line chart comparing the search times of different algorithms.
    """
    plt.figure(figsize=(10, 6))
    
    # 1. Naive Search Line (Red)
    plt.plot(sizes, naive_times, label='Naive Search (Brute Force)', 
             color='red', marker='o', linestyle='--')
    
    # 2. Suffix Array Search Line (Blue)
    plt.plot(sizes, sa_search_times, label='Suffix Array Search (Indexed)', 
             color='blue', marker='s')
    
    # 3. Bloom Filter Check Line (Green)
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