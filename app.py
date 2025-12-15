import streamlit as st
import time
import random
import sys
import matplotlib.pyplot as plt
import pandas as pd
import os

# Import algorithms
from algorithms import (
    naive_search, 
    rabin_karp_search, 
    kmp_search, 
    boyer_moore_search, 
    build_suffix_array, suffix_array_search, 
    build_bloom_filter
)

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="BioPattern Pro", page_icon="🧬", layout="wide")

# ==========================================
# 2. ADVANCED CSS STYLING
# ==========================================
st.markdown("""
    <style>
    /* --- LAYOUT FIXES (COMPACT) --- */
    .block-container {
        padding-top: 3rem !important; /* Minimum top padding */
        padding-bottom: 4rem !important;
    }
    
    /* --- ANIMATED HEADER --- */
    @keyframes gradient-move {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .header-box {
        background: linear-gradient(-45deg, #0984e3, #6c5ce7, #ff7675, #00b894);
        background-size: 400% 400%;
        animation: gradient-move 7s ease infinite;
        padding: 30px; /* Reduced padding */
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px; /* Tighter margin */
        border-bottom: 6px solid #dfe6e9;
    }
    .header-title { 
        font-size: 3rem; /* Slightly smaller title */
        font-weight: 900; 
        margin-bottom: 5px; 
        text-shadow: 2px 2px 5px rgba(0,0,0,0.4); 
    }
    .header-subtitle { 
        font-size: 1.1rem; 
        font-weight: 300; 
        opacity: 0.95; 
        margin-bottom: 15px; 
        letter-spacing: 1px;
    }
    .header-team {
        font-size: 1rem;
        font-weight: 700;
        background-color: rgba(255, 255, 255, 0.25);
        padding: 8px 30px;
        border-radius: 50px;
        display: inline-block;
        backdrop-filter: blur(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }

    /* --- DATA VISUALIZATION BOXES (COMPACT) --- */
    .genome-box {
        background-color: #f8f9fa; color: #2d3436; padding: 10px;
        border-radius: 12px; border: 2px solid #e9ecef;
        height: 250px; /* EVEN SMALLER HEIGHT */
        overflow-y: auto; word-wrap: break-word; 
        font-family: 'Courier New', monospace; font-size: 13px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.03);
    }
    .indices-box {
        background-color: #ffffff; color: #2d3436; padding: 10px;
        border-radius: 10px; border: 2px solid #b2bec3;
        height: 100px; overflow-y: auto; word-wrap: break-word;
        font-family: 'Consolas', monospace; font-size: 12px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
    }

    /* --- BUTTONS & METRICS --- */
    div.stButton > button {
        width: 100%; border-radius: 12px; border: none; font-weight: 800; padding: 12px; /* Smaller padding */
        transition: all 0.3s ease; height: 100%; text-transform: uppercase; letter-spacing: 0.5px; font-size: 14px;
    }
    div[data-testid="stMetric"] {
        background-color: white; padding: 10px; border-radius: 12px;
        border-left: 6px solid #0984e3; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* --- COLORFUL TABS CONFIGURATION --- */
    div[role="radiogroup"] { display: flex; flex-direction: row; gap: 10px; padding: 5px 0; }
    div[role="radiogroup"] label {
        background-color: white !important; padding: 10px; border-radius: 10px; border: 2px solid #dfe6e9; 
        flex-grow: 1; text-align: center; font-weight: 700; color: #636e72; transition: all 0.3s ease;
        display: flex; justify-content: center; align-items: center;
    }
    div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p { font-size: 14px; margin: 0; }

    /* 1. PERFORMANCE (ORANGE) */
    div[role="radiogroup"] label:nth-of-type(1) { border-color: #ff9f43 !important; color: #e67e22 !important; }
    div[role="radiogroup"] label:nth-of-type(1):hover { background-color: #fff0e6 !important; transform: translateY(-3px); }
    div[role="radiogroup"] label:nth-of-type(1)[data-checked="true"] {
        background: linear-gradient(135deg, #ff9f43, #d35400) !important; color: white !important; border: none !important;
    }

    /* 2. LOCATIONS (BLUE) */
    div[role="radiogroup"] label:nth-of-type(2) { border-color: #54a0ff !important; color: #0984e3 !important; }
    div[role="radiogroup"] label:nth-of-type(2):hover { background-color: #e6f2ff !important; transform: translateY(-3px); }
    div[role="radiogroup"] label:nth-of-type(2)[data-checked="true"] {
        background: linear-gradient(135deg, #0984e3, #2980b9) !important; color: white !important; border: none !important;
    }

    /* 3. HEATMAP (RED) */
    div[role="radiogroup"] label:nth-of-type(3) { border-color: #ff6b6b !important; color: #ee5253 !important; }
    div[role="radiogroup"] label:nth-of-type(3):hover { background-color: #ffe6e6 !important; transform: translateY(-3px); }
    div[role="radiogroup"] label:nth-of-type(3)[data-checked="true"] {
        background: linear-gradient(135deg, #ff7675, #d63031) !important; color: white !important; border: none !important;
    }

    /* 4. REPORT (GREEN) */
    div[role="radiogroup"] label:nth-of-type(4) { border-color: #1dd1a1 !important; color: #10ac84 !important; }
    div[role="radiogroup"] label:nth-of-type(4):hover { background-color: #e6fffa !important; transform: translateY(-3px); }
    div[role="radiogroup"] label:nth-of-type(4)[data-checked="true"] {
        background: linear-gradient(135deg, #2ecc71, #27ae60) !important; color: white !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. HEADER SECTION
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🧬 BioPattern Pro</div>
        <div class="header-subtitle">High-Performance Genome Sequencing & Algorithm Analysis</div>
        <div class="header-team">🚀 Developed By: Büşra Çakmak & Sena Nur Güngez</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. SESSION STATE MANAGEMENT
# ==========================================
if 'results' not in st.session_state: st.session_state['results'] = {}
if 'matches_found' not in st.session_state: st.session_state['matches_found'] = []
if 'analysis_done' not in st.session_state: st.session_state['analysis_done'] = False
if 'synthetic_genome' not in st.session_state: st.session_state['synthetic_genome'] = ""

# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================
@st.cache_data
def load_genome_file(filename):
    if not os.path.exists(filename): return None
    with open(filename, "r") as f: return f.read().strip()
def validate_dna_sequence(sequence: str) -> str:
    """
    Cleans the DNA data (removes whitespace, makes uppercase) and checks for invalid characters.
    Raises ValueError if characters other than A, T, C, G, N are found.
    """
    if not sequence: 
        return ""
        
    valid_chars = set("ATCGN") # A, T, C, G (DNA bases) and N (Unknown base)
    
    # Clean up: Remove newlines, carriage returns, and spaces; convert to uppercase
    clean_seq = sequence.upper().replace("\n", "").replace("\r", "").replace(" ", "")
    
    # Check for invalid characters using set comparison
    if not set(clean_seq).issubset(valid_chars):
        invalid = list(set(clean_seq) - valid_chars)
        # Raise a specific error that the except block will catch
        raise ValueError(f"Invalid characters found: {invalid}. Only A, T, C, G, N are allowed.")
    
    return clean_seq
# ==========================================
# 6. SIDEBAR CONFIGURATION
# ==========================================
st.sidebar.header("⚙️ Configuration")
data_source = st.sidebar.radio("📂 Select Data Source", ("Synthetic DNA", "SARS-CoV-2 (Virus)", "E. coli K-12 (Bacteria)"))

genome_data = ""
pattern_default = "ACGT"

if "Synthetic" in data_source:
    genome_size = st.sidebar.slider("📏 Genome Size (bp)", 5000, 200000, 50000, 5000)
    if len(st.session_state['synthetic_genome']) != genome_size:
        st.session_state['synthetic_genome'] = ''.join(random.choice('ACGT') for _ in range(genome_size))
    genome_data = st.session_state['synthetic_genome']
    st.sidebar.success(f"Generated {genome_size} bp")
    pattern_default = "ACGTAC"
elif "SARS-CoV-2" in data_source:
    loaded = load_genome_file("covid19.txt")
    if loaded: 
        genome_data = loaded
        st.sidebar.success(f"Loaded Covid-19 ({len(genome_data):,} bp)")
        pattern_default = "ATTAAAGGTT"
    else: st.sidebar.error("⚠️ File missing! Run setup.py")
elif "E. coli" in data_source:
    loaded = load_genome_file("ecoli.txt")
    if loaded:
        genome_data = loaded
        st.sidebar.success(f"Loaded E. coli ({len(genome_data):,} bp)")
        st.sidebar.warning("⚠️ Large Dataset! Naive/RK skipped.")
        pattern_default = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCT"
    else: st.sidebar.error("⚠️ File missing! Run setup.py")

st.sidebar.subheader("🔍 Target Pattern")
pattern = st.sidebar.text_input("Enter DNA Sequence", pattern_default)
try:
    # 1. Validate and clean the main genome data
    if genome_data:
        genome_data = validate_dna_sequence(genome_data)
        
    # 2. Validate and clean the search pattern
    if pattern:
        pattern = validate_dna_sequence(pattern)

except ValueError as e:
    # Catch validation errors (e.g., forbidden characters)
    st.sidebar.error(f"🚨 VALIDATION ERROR: {e}")
    # Stop the execution of the main dashboard below
    st.stop() 
except Exception as e:
    # Catch any other unexpected loading or cleaning errors
    st.sidebar.error(f"⚠️ AN UNEXPECTED ERROR OCCURRED: {e}")
    st.stop()
# ==========================================
# 7. MAIN DASHBOARD LAYOUT (COMPACT)
# ==========================================
if genome_data:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🔬 Genome Viewer")
        limit = 5000
        disp = genome_data[:limit] + ("..." if len(genome_data) > limit else "")
        st.markdown(f'<div class="genome-box">{disp}</div>', unsafe_allow_html=True)
    with col2:
        # Statistics and Buttons in the SAME column block for compactness
        st.subheader("📊 Statistics")
        gc = (genome_data.count('G') + genome_data.count('C')) / len(genome_data) * 100
        
        m1, m2 = st.columns(2)
        m1.metric("Total Size", f"{len(genome_data)/1000:.1f}k bp")
        m2.metric("GC Content", f"{gc:.1f}%")
        st.metric("Pattern Length", f"{len(pattern)} chars")
        
        # BUTTONS ARE NOW HERE - CLOSER TO TOP
        btn_col1, btn_col2 = st.columns([2, 1])
        with btn_col1:
            start_btn = st.button("🚀 START BENCHMARK", type="primary", use_container_width=True)
        with btn_col2:
            reset_btn = st.button("🔄 RESET", type="secondary", use_container_width=True)
            if reset_btn:
                st.session_state['analysis_done'] = False
                st.session_state['results'] = {}
                st.rerun()

    # ==========================================
    # 8. ALGORITHM EXECUTION ENGINE
    # ==========================================
    if start_btn:
        st.toast('🧬 Processing Genome Algorithms...', icon='⏳')
        with st.spinner("Calculating..."):
            time.sleep(0.5) 
            st.session_state['analysis_done'] = True 
            progress_bar = st.progress(0)
            temp_results = {}
            temp_matches = [] 
            algos = [("Naive Search", naive_search), ("Rabin-Karp", rabin_karp_search), ("KMP Search", kmp_search), ("Boyer-Moore", boyer_moore_search)]
            step = 0
            for name, func in algos:
                if len(genome_data) > 1000000 and name in ["Naive Search", "Rabin-Karp"]:
                    temp_results[name] = {'time': 0, 'matches': -1, 'memory': 0}
                else:
                    t0 = time.time(); m = func(pattern, genome_data); dur = time.time()-t0
                    temp_results[name] = {'time': dur, 'matches': len(m), 'memory': sys.getsizeof(m)}
                    if name == "Boyer-Moore": temp_matches = m
                step += 15; progress_bar.progress(step)
            t0 = time.time(); sa = build_suffix_array(genome_data); t1 = time.time(); m_sa = suffix_array_search(pattern, genome_data, sa)
            temp_results['Suffix Array'] = {'time': time.time()-t1, 'matches': len(m_sa), 'memory': sys.getsizeof(sa)}; progress_bar.progress(85)
            bf = build_bloom_filter(genome_data, len(pattern)); t0 = time.time(); bf.check(pattern)
            temp_results['Bloom Filter'] = {'time': time.time()-t0, 'matches': "N/A", 'memory': sys.getsizeof(bf.bit_array)}; progress_bar.progress(100)
            st.session_state['results'] = temp_results; st.session_state['matches_found'] = temp_matches
        st.toast('✅ Analysis Complete!', icon='🎉')

    # ==========================================
    # 9. RESULTS DISPLAY SECTION
    # ==========================================
    if st.session_state['analysis_done']:
        st.markdown("### ⚡ Analysis Results")
        results = st.session_state['results']
        matches_found = st.session_state['matches_found']

        selected_view = st.radio("Select View", ["⏱️ Performance", "📍 Match Locations", "🔥 Heatmap", "📄 Report"], horizontal=True, label_visibility="collapsed")
        st.write("")

        if selected_view == "⏱️ Performance":
            st.info("💡 Comparison of execution time (Lower is better).")
            valid_res = {k:v for k,v in results.items() if v['time'] > 0}
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(valid_res.keys(), [x['time'] for x in valid_res.values()], color=['#ff7675', '#fdcb6e', '#ffeaa7', '#00b894', '#0984e3', '#6c5ce7'])
            ax.set_ylabel("Time (seconds)"); ax.set_title("Algorithm Speed Benchmark"); st.pyplot(fig)

        elif selected_view == "📍 Match Locations":
            st.markdown("#### 🧬 Genome Barcode Visualization")
            if matches_found and len(matches_found) > 0:
                st.success(f"Pattern found {len(matches_found)} times!")
                fig, ax = plt.subplots(figsize=(12, 2))
                ax.eventplot(matches_found, orientation='horizontal', colors='#0984e3', linewidths=1.5)
                ax.set_xlim(0, len(genome_data)); ax.set_xlabel("Position (bp)"); ax.set_yticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['left'].set_visible(False)
                st.pyplot(fig)
                st.markdown("**Index Positions:**"); st.markdown(f'<div class="indices-box">{str(matches_found)}</div>', unsafe_allow_html=True)
            else: st.error("No matches found.")

        elif selected_view == "🔥 Heatmap": 
            st.markdown("#### Pattern Density Visualization")
            if matches_found and len(matches_found) > 0:
                fig, ax = plt.subplots(figsize=(12, 3))
                ax.hist(matches_found, bins=150, color='#e17055', alpha=0.7)
                ax.set_xlim(0, len(genome_data)); ax.set_xlabel("Genome Position"); ax.set_ylabel("Frequency"); st.pyplot(fig)
            else: st.warning("⚠️ No matches found.")

        elif selected_view == "📄 Report":
            df = pd.DataFrame([{"Algorithm": k, "Time (s)": f"{v['time']:.6f}", "Matches": str(v['matches']), "Memory (Bytes)": v['memory']} for k,v in results.items()])
            st.table(df)
            col_d1, col_d2 = st.columns(2)
            with col_d1: st.download_button("📥 CSV Report", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
            with col_d2: 
                if matches_found: st.download_button("📥 Indices TXT", ",".join(map(str, matches_found)), "indices.txt", "text/plain")