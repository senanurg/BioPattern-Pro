import streamlit as st
import time
import random
import sys
import matplotlib.pyplot as plt
import os
from PIL import Image

# Algoritmalarımızı çağırıyoruz
from algorithms import naive_search, boyer_moore_search, build_suffix_array, suffix_array_search, build_bloom_filter, kmp_search

# --- SAYFA AYARLARI (Geniş Ekran) ---
st.set_page_config(page_title="BioPattern Ultimate", page_icon="🧬", layout="wide")

# --- ÖZEL CSS TASARIMI (Makyaj Kısmı 💄) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(to bottom right, #f0f2f6, #e2eafc);
    }
    
    /* Başlık Stili */
    .title-box {
        background-color: #1e3799;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Sidebar (Yan Menü) Stili */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dcdcdc;
    }
    
    /* Sonuç Kartları (Metric Box) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #4a69bd;
    }
    
    /* İsimlerin yazdığı footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1e3799;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (Görsel ve Başlık) ---
# Eğer klasörde 'dna_banner.jpg' varsa onu göster, yoksa sadece başlığı göster.
if os.path.exists("dna_banner.jpg"):
    st.image("dna_banner.jpg", use_column_width=True)

st.markdown("""
    <div class="title-box">
        <h1>🧬 BioPattern: Advanced Genomic Analysis</h1>
        <p>Comparative Analysis of String Matching Algorithms on Big Data</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: AYARLAR VE EKİP ---
st.sidebar.header("⚙️ Simulation Settings")

# 1. Genom Ayarları
genome_size = st.sidebar.slider("🧬 Genome Size (Base Pairs)", 5000, 200000, 50000, 5000)
pattern = st.sidebar.text_input("🔍 DNA Pattern", "ACGTAC")

# 2. Butonlar
if 'genome' not in st.session_state or st.sidebar.button("🔄 Generate New Genome"):
    st.session_state['genome'] = ''.join(random.choice('ACGT') for _ in range(genome_size))
    st.sidebar.success("New DNA Sequence Generated!")

genome_data = st.session_state['genome']

st.sidebar.markdown("---")

# --- PROJE EKİBİ (İSİMLER BURADA) ---
st.sidebar.subheader("🎓 Project Team")
st.sidebar.info("**Büşra Çakmak**\n\n**Sena Nur Güngez**")
st.sidebar.caption("Computer Engineering | Bioinformatics Course Project")
st.sidebar.markdown("---")

# --- ANA EKRAN: DATA ÖNİZLEME ---
with st.expander("🔬 View Raw Genome Data (First 500 Characters)"):
    st.code(genome_data[:500] + "...", language='text')
    st.caption(f"Total Length: {len(genome_data)} Base Pairs")

# --- ANALİZ BUTONU ---
if st.button("🚀 START COMPREHENSIVE BENCHMARK", type="primary"):
    
    st.markdown("### 📊 Performance Results")
    
    # İlerletme Çubuğu (Heyecan yaratır)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = {}
    
    # Adım Adım Analiz (Görsel olarak tek tek hesaplandığını hissettiriyoruz)
    
    # 1. Naive
    status_text.text("Running Naive Algorithm...")
    t0 = time.time()
    matches = naive_search(pattern, genome_data)
    results['Naive'] = {'time': time.time()-t0, 'matches': len(matches), 'memory': sys.getsizeof(matches)}
    progress_bar.progress(20)

    # 2. KMP
    status_text.text("Running Knuth-Morris-Pratt (KMP)...")
    t0 = time.time()
    kmp_search(pattern, genome_data)
    results['KMP'] = {'time': time.time()-t0, 'matches': len(matches), 'memory': sys.getsizeof(matches)}
    progress_bar.progress(40)

    # 3. Boyer-Moore
    status_text.text("Running Boyer-Moore (Smart Search)...")
    t0 = time.time()
    boyer_moore_search(pattern, genome_data)
    results['Boyer-Moore'] = {'time': time.time()-t0, 'matches': len(matches), 'memory': sys.getsizeof(matches)}
    progress_bar.progress(60)

    # 4. Suffix Array
    status_text.text("Building & Searching Suffix Array...")
    t0 = time.time()
    sa = build_suffix_array(genome_data)
    build_time = time.time() - t0
    t1 = time.time()
    suffix_array_search(pattern, genome_data, sa)
    search_time = time.time() - t1
    results['Suffix Array'] = {'time': search_time, 'matches': len(matches), 'memory': sys.getsizeof(sa)}
    progress_bar.progress(80)

    # 5. Bloom Filter
    status_text.text("Checking Bloom Filter...")
    bf = build_bloom_filter(genome_data, len(pattern))
    t0 = time.time()
    bf.check(pattern)
    results['Bloom Filter'] = {'time': time.time()-t0, 'matches': "N/A", 'memory': sys.getsizeof(bf.bit_array)}
    progress_bar.progress(100)
    
    status_text.empty() # Yazıyı temizle

    # --- TABLI SONUÇ GÖSTERİMİ ---
    tab1, tab2, tab3 = st.tabs(["⏱️ Speed Analysis", "💾 Memory Analysis", "📍 Match Distribution"])

    # TAB 1: HIZ
    with tab1:
        st.subheader("⚡ Execution Time Comparison")
        cols = st.columns(5)
        algos = ['Naive', 'KMP', 'Boyer-Moore', 'Suffix Array', 'Bloom Filter']
        
        for i, algo in enumerate(algos):
            cols[i].metric(label=algo, value=f"{results[algo]['time']:.5f} s")
            
        # Grafik
        fig_time, ax_time = plt.subplots(figsize=(10, 4))
        times = [results[a]['time'] for a in algos]
        colors = ['#e74c3c', '#e67e22', '#f1c40f', '#3498db', '#2ecc71'] # Modern renk paleti
        ax_time.bar(algos, times, color=colors)
        ax_time.set_ylabel("Time (seconds)")
        ax_time.set_title("Search Speed (Lower is Better)")
        ax_time.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig_time)
        
        st.success("💡 **Insight:** Suffix Array provides near-instant search results for massive datasets!")

    # TAB 2: HAFIZA
    with tab2:
        st.subheader("💾 RAM Usage Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.info("""
            **Why Memory Matters?**
            Some algorithms like **Suffix Array** are extremely fast but require building a large index in memory first.
            **Bloom Filters** use very little memory but are probabilistic.
            """)
        
        with col2:
            mem_sizes = [results[a]['memory'] for a in algos]
            fig_mem, ax_mem = plt.subplots(figsize=(8, 4))
            ax_mem.bar(algos, mem_sizes, color=['#95a5a6', '#95a5a6', '#95a5a6', '#3498db', '#2ecc71'])
            ax_mem.set_ylabel("Memory (Bytes)")
            ax_mem.set_yscale('log')
            ax_mem.set_title("Memory Footprint (Log Scale)")
            st.pyplot(fig_mem)

    # TAB 3: DAĞILIM
    with tab3:
        st.subheader("📍 Pattern Occurrences Map")
        if len(matches) > 0:
            st.markdown(f"The pattern `{pattern}` was found at **{len(matches)}** locations.")
            
            fig_dist, ax_dist = plt.subplots(figsize=(12, 2))
            ax_dist.hlines(1, 0, genome_size, color='#bdc3c7', linewidth=15) # DNA şeridi
            ax_dist.plot(matches, [1]*len(matches), 'r|', markersize=25, markeredgewidth=3) # Eşleşmeler
            
            ax_dist.set_xlim(0, genome_size)
            ax_dist.set_yticks([])
            ax_dist.set_xlabel("Genome Position")
            st.pyplot(fig_dist)
        else:
            st.warning("No matches found.")

# --- FOOTER (İSİMLERİN YAZDIĞI SABİT ALAN) ---
# Not: Streamlit'te sabit footer biraz hileli yapılır ama CSS ile hallettik.
st.markdown("""
<div class="footer">
    Bioinformatics Algorithms Final Project | Students: Büşra Çakmak & Sena Nur Güngez
</div>
""", unsafe_allow_html=True)