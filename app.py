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
    .block-container { padding-top: 3rem !important; padding-bottom: 4rem !important; }
    @keyframes gradient-move {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .header-box {
        background: linear-gradient(-45deg, #0984e3, #6c5ce7, #ff7675, #00b894);
        background-size: 400% 400%; animation: gradient-move 7s ease infinite;
        padding: 30px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 25px; border-bottom: 6px solid #dfe6e9;
    }
    .header-title { font-size: 3rem; font-weight: 900; margin-bottom: 5px; text-shadow: 2px 2px 5px rgba(0,0,0,0.4); }
    .header-subtitle { font-size: 1.1rem; font-weight: 300; opacity: 0.95; margin-bottom: 15px; letter-spacing: 1px; }
    .header-team {
        font-size: 1rem; font-weight: 700; background-color: rgba(255, 255, 255, 0.25);
        padding: 8px 30px; border-radius: 50px; display: inline-block;
        backdrop-filter: blur(5px); box-shadow: 0 5px 15px rgba(0,0,0,0.15); border: 1px solid rgba(255, 255, 255, 0.4);
    }
    .genome-box {
        background-color: #f8f9fa; color: #2d3436; padding: 10px; border-radius: 12px; border: 2px solid #e9ecef;
        height: 250px; overflow-y: auto; word-wrap: break-word; font-family: 'Courier New', monospace; font-size: 13px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.03);
    }
    .indices-box {
        background-color: #ffffff; color: #2d3436; padding: 10px; border-radius: 10px; border: 2px solid #b2bec3;
        height: 100px; overflow-y: auto; word-wrap: break-word; font-family: 'Consolas', monospace; font-size: 12px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
    }
    div.stButton > button {
        width: 100%; border-radius: 12px; border: none; font-weight: 800; padding: 12px;
        transition: all 0.3s ease; height: 100%; text-transform: uppercase; letter-spacing: 0.5px; font-size: 14px;
    }
    div[data-testid="stMetric"] {
        background-color: white; padding: 10px; border-radius: 12px;
        border-left: 6px solid #0984e3; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    div[role="radiogroup"] label {
        background-color: white !important; padding: 10px; border-radius: 10px; border: 2px solid #dfe6e9; 
        flex-grow: 1; text-align: center; font-weight: 700; color: #636e72; transition: all 0.3s ease;
    }
    div[role="radiogroup"] label:nth-of-type(1)[data-checked="true"] { background: linear-gradient(135deg, #ff9f43, #d35400) !important; color: white !important; border: none !important; }
    div[role="radiogroup"] label:nth-of-type(2)[data-checked="true"] { background: linear-gradient(135deg, #0984e3, #2980b9) !important; color: white !important; border: none !important; }
    div[role="radiogroup"] label:nth-of-type(3)[data-checked="true"] { background: linear-gradient(135deg, #ff7675, #d63031) !important; color: white !important; border: none !important; }
    div[role="radiogroup"] label:nth-of-type(4)[data-checked="true"] { background: linear-gradient(135deg, #2ecc71, #27ae60) !important; color: white !important; border: none !important; }
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
# 4. SESSION STATE & HELPERS
# ==========================================
if 'results' not in st.session_state: st.session_state['results'] = {}
if 'matches_found' not in st.session_state: st.session_state['matches_found'] = []
if 'analysis_done' not in st.session_state: st.session_state['analysis_done'] = False
if 'synthetic_genome' not in st.session_state: st.session_state['synthetic_genome'] = ""

@st.cache_data
def load_genome_file(filename):
    if not os.path.exists(filename): return None
    with open(filename, "r") as f: return f.read().strip()

def validate_dna_sequence(sequence: str) -> str:
    if not sequence: return ""
    valid_chars = set("ATCGN")
    clean_seq = sequence.upper().replace("\n", "").replace("\r", "").replace(" ", "")
    if not set(clean_seq).issubset(valid_chars):
        invalid = list(set(clean_seq) - valid_chars)
        raise ValueError(f"Invalid characters found: {invalid}. Only A, T, C, G, N are allowed.")
    return clean_seq

# ==========================================
# 5. SIDEBAR CONFIGURATION
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
        st.sidebar.warning("⚠️ Large Dataset! Naive/RK/SA limited.")
        pattern_default = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCT"
    else: st.sidebar.error("⚠️ File missing! Run setup.py")

st.sidebar.subheader("🔍 Target Pattern")
pattern = st.sidebar.text_input("Enter DNA Sequence", pattern_default)

try:
    if genome_data: genome_data = validate_dna_sequence(genome_data)
    if pattern: pattern = validate_dna_sequence(pattern)
except ValueError as e:
    st.sidebar.error(f"🚨 VALIDATION ERROR: {e}"); st.stop()
except Exception as e:
    st.sidebar.error(f"⚠️ ERROR: {e}"); st.stop()

# ==========================================
# 6. MAIN DASHBOARD
# ==========================================
if genome_data:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🔬 Genome Viewer")
        limit = 5000
        disp = genome_data[:limit] + ("..." if len(genome_data) > limit else "")
        st.markdown(f'<div class="genome-box">{disp}</div>', unsafe_allow_html=True)
    with col2:
        st.subheader("📊 Statistics")
        gc = (genome_data.count('G') + genome_data.count('C')) / len(genome_data) * 100
        m1, m2 = st.columns(2)
        m1.metric("Total Size", f"{len(genome_data)/1000:.1f}k bp")
        m2.metric("GC Content", f"{gc:.1f}%")
        st.metric("Pattern Length", f"{len(pattern)} chars")
        
        btn_col1, btn_col2 = st.columns([2, 1])
        with btn_col1: start_btn = st.button("🚀 START BENCHMARK", type="primary", use_container_width=True)
        with btn_col2: 
            if st.button("🔄 RESET", type="secondary", use_container_width=True):
                st.session_state['analysis_done'] = False; st.session_state['results'] = {}; st.rerun()

    # ==========================================
    # 7. ALGORITHM ENGINE
    # ==========================================
    if start_btn:
        st.toast('🧬 Processing Genome Algorithms...', icon='⏳')
        with st.spinner("Calculating..."):
            time.sleep(0.5) 
            st.session_state['analysis_done'] = True 
            progress_bar = st.progress(0)
            temp_results = {}
            temp_matches = [] 
            
            # Algoritmalar Listesi
            algos = [("Naive Search", naive_search), ("Rabin-Karp", rabin_karp_search), ("KMP Search", kmp_search), ("Boyer-Moore", boyer_moore_search)]
            step = 0
            
            for name, func in algos:
                # 1. BÜYÜK DOSYA KORUMASI (Naive & Rabin-Karp)
                if len(genome_data) > 1000000 and name in ["Naive Search", "Rabin-Karp"]:
                    temp_results[name] = {'time': -1, 'matches': -1, 'memory': 0} # -1: Skipped
                else:
                    t0 = time.time(); m = func(pattern, genome_data); dur = time.time()-t0
                    temp_results[name] = {'time': dur, 'matches': len(m), 'memory': sys.getsizeof(m)}
                    if name == "Boyer-Moore": temp_matches = m
                step += 15; progress_bar.progress(step)
            
            # 2. SUFFIX ARRAY KORUMASI (Bellek Taşmasını Önler)
            if len(genome_data) < 100000:
                t0 = time.time()
                sa = build_suffix_array(genome_data)
                t1 = time.time()
                m_sa = suffix_array_search(pattern, genome_data, sa)
                temp_results['Suffix Array'] = {'time': time.time()-t1, 'matches': len(m_sa), 'memory': sys.getsizeof(sa)}
            else:
                temp_results['Suffix Array'] = {'time': -1, 'matches': -1, 'memory': 0} # -1: Skipped
            
            progress_bar.progress(85)
            
            # 3. BLOOM FILTER (Her zaman çalışır)
            bf = build_bloom_filter(genome_data, len(pattern)); t0 = time.time(); bf.check(pattern)
            temp_results['Bloom Filter'] = {'time': time.time()-t0, 'matches': "N/A", 'memory': sys.getsizeof(bf.bit_array)}
            
            progress_bar.progress(100)
            st.session_state['results'] = temp_results; st.session_state['matches_found'] = temp_matches
        st.toast('✅ Analysis Complete!', icon='🎉')

    # ==========================================
    # 8. RESULTS DISPLAY
    # ==========================================
    if st.session_state['analysis_done']:
        st.markdown("### ⚡ Analysis Results")
        results = st.session_state['results']
        matches_found = st.session_state['matches_found']

        selected_view = st.radio("Select View", ["⏱️ Performance", "📍 Match Locations", "🔥 Heatmap", "📄 Report"], horizontal=True, label_visibility="collapsed")
        st.write("")

        if selected_view == "⏱️ Performance":
            st.info("💡 Comparison of execution time (Lower is better). Skipped algorithms are not shown.")
            # FİLTRE DÜZELTİLDİ: 0.00s olan Bloom Filter görünsün diye '>= 0' yaptık. -1 olanlar gizlenir.
            valid_res = {k:v for k,v in results.items() if v['time'] >= 0}
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(valid_res.keys(), [x['time'] for x in valid_res.values()], color=['#ff7675', '#fdcb6e', '#ffeaa7', '#00b894', '#0984e3', '#6c5ce7'])
            ax.set_ylabel("Time (seconds)"); ax.set_title("Algorithm Speed Benchmark"); st.pyplot(fig)

        elif selected_view == "📍 Match Locations":
            st.markdown("#### 🧬 Genome Barcode Visualization")
            if matches_found and len(matches_found) > 0:
                st.success(f"Pattern found {len(matches_found)} times!")
                fig, ax = plt.subplots(figsize=(12, 2))
                ax.eventplot(matches_found, orientation='horizontal', colors='#0984e3', linewidths=1.5)
                ax.set_xlim(0, len(genome_data)); ax.set_xlabel("Position (bp)"); ax.set_yticks([])
                ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['left'].set_visible(False)
                st.pyplot(fig)
                st.markdown("**Index Positions:**"); st.markdown(f'<div class="indices-box">{str(matches_found)}</div>', unsafe_allow_html=True)
            else: st.error("No matches found or algorithm doesn't provide indices.")

        elif selected_view == "🔥 Heatmap": 
            st.markdown("#### Pattern Density Visualization")
            if matches_found and len(matches_found) > 0:
                fig, ax = plt.subplots(figsize=(12, 3))
                ax.hist(matches_found, bins=150, color='#e17055', alpha=0.7)
                ax.set_xlim(0, len(genome_data)); ax.set_xlabel("Genome Position"); ax.set_ylabel("Frequency"); st.pyplot(fig)
            else: st.warning("⚠️ No matches found.")

        elif selected_view == "📄 Report":
            # -1 olan süreleri "Skipped" olarak tabloda göster
            display_data = []
            for k, v in results.items():
                t_str = f"{v['time']:.6f}" if v['time'] >= 0 else "Skipped (Large Data)"
                display_data.append({"Algorithm": k, "Time (s)": t_str, "Matches": str(v['matches']), "Memory (Bytes)": v['memory']})
            
            df = pd.DataFrame(display_data)
            st.table(df)
            col_d1, col_d2 = st.columns(2)
            with col_d1: st.download_button("📥 CSV Report", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
            with col_d2: 
                if matches_found: st.download_button("📥 Indices TXT", ",".join(map(str, matches_found)), "indices.txt", "text/plain")