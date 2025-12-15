import streamlit as st
import time
import random
import matplotlib.pyplot as plt
from algorithms import naive_search, boyer_moore_search, build_suffix_array, suffix_array_search, build_bloom_filter

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="BioPattern Analysis", page_icon="🧬", layout="wide")

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #27ae60;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TITLE & DESCRIPTION ---
st.title("🧬 BioPattern: Genomic Algorithm Analyzer")
st.markdown("""
This application benchmarks different string matching algorithms on DNA sequences.
It compares *Brute Force, **Smart Search (Boyer-Moore), **Indexing (Suffix Array), and **Probabilistic (Bloom Filter)* approaches.
""")

# --- SIDEBAR: SETTINGS ---
st.sidebar.header("⚙ Configuration")

# 1. Genome Generation
genome_size = st.sidebar.slider("Genome Size (Base Pairs)", min_value=1000, max_value=100000, value=50000, step=1000)
pattern = st.sidebar.text_input("DNA Pattern to Search", value="ACGTAC")

if st.sidebar.button("Generate New Genome"):
    new_genome = ''.join(random.choice('ACGT') for _ in range(genome_size))
    st.session_state['genome'] = new_genome
    st.sidebar.success(f"Generated {genome_size} bp genome!")

# Load genome from session state or generate default
if 'genome' not in st.session_state:
    st.session_state['genome'] = ''.join(random.choice('ACGT') for _ in range(genome_size))

genome_data = st.session_state['genome']

# Show Genome Preview
with st.expander("🔎 View Genome Data (Preview first 500 chars)"):
    st.code(genome_data[:500] + "...", language='text')

# --- MAIN BENCHMARKING SECTION ---
if st.button("🚀 Run Benchmark Analysis"):
    st.write("### ⏱ Performance Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 1. NAIVE
    start = time.time()
    matches_naive = naive_search(pattern, genome_data)
    time_naive = time.time() - start
    col1.metric("Naive Search", f"{time_naive:.5f} s", f"{len(matches_naive)} matches")

    # 2. BOYER-MOORE
    start = time.time()
    matches_bm = boyer_moore_search(pattern, genome_data)
    time_bm = time.time() - start
    col2.metric("Boyer-Moore", f"{time_bm:.5f} s", "Smart Search")

    # 3. SUFFIX ARRAY
    t0 = time.time()
    sa = build_suffix_array(genome_data)
    build_time = time.time() - t0
    
    t1 = time.time()
    matches_sa = suffix_array_search(pattern, genome_data, sa)
    search_time = time.time() - t1
    
    col3.metric("Suffix Array (Search)", f"{search_time:.5f} s", f"Build: {build_time:.2f}s")

    # 4. BLOOM FILTER
    t0 = time.time()
    bf = build_bloom_filter(genome_data, len(pattern))
    
    t1 = time.time()
    exists = bf.check(pattern)
    check_time = time.time() - t1
    
    status = "Present" if exists else "Absent"
    col4.metric("Bloom Filter", f"{check_time:.6f} s", status)

    # --- VISUALIZATION ---
    st.write("---")
    st.write("### 📊 Interactive Performance Graph")
    
    # Generate data for the graph dynamically based on current selection
    sizes = [int(genome_size * 0.2), int(genome_size * 0.5), int(genome_size * 0.8), genome_size]
    n_times, bm_times, sa_times, bf_times = [], [], [], []
    
    progress_bar = st.progress(0)
    
    for i, size in enumerate(sizes):
        sub_genome = genome_data[:size]
        
        # Naive
        s = time.time()
        naive_search(pattern, sub_genome)
        n_times.append(time.time() - s)
        
        # BM
        s = time.time()
        boyer_moore_search(pattern, sub_genome)
        bm_times.append(time.time() - s)
        
        # SA (Search only)
        temp_sa = build_suffix_array(sub_genome)
        s = time.time()
        suffix_array_search(pattern, sub_genome, temp_sa)
        sa_times.append(time.time() - s)
        
        # BF
        temp_bf = build_bloom_filter(sub_genome, len(pattern))
        s = time.time()
        temp_bf.check(pattern)
        bf_times.append(time.time() - s)
        
        progress_bar.progress((i + 1) / len(sizes))

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sizes, n_times, label='Naive', marker='o', linestyle='--')
    ax.plot(sizes, bm_times, label='Boyer-Moore', marker='D')
    ax.plot(sizes, sa_times, label='Suffix Array', marker='s')
    ax.plot(sizes, bf_times, label='Bloom Filter', marker='^')
    
    ax.set_xlabel("Genome Size (Base Pairs)")
    ax.set_ylabel("Time (Seconds)")
    ax.set_title("Algorithm Scalability Analysis")
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
    st.success("Analysis Completed Successfully!")

# --- FOOTER ---
st.markdown("---")
st.caption("Project by: Büşra Çakmak & Sena Nur Güngez | Bioinformatics Algorithms Course Project")