# BioPattern-Pro

🧬 High-performance bioinformatics tool for DNA sequence pattern matching and algorithm benchmarking (Naive, KMP, Boyer-Moore, Rabin-Karp, Suffix Arrays, Bloom Filter) on large genomic datasets.

---

![GitHub top language](https://img.shields.io/github/languages/top/yourusername/BIOPATTERN-PRO?color=blue)
![GitHub commit activity](https://img.shields.io/badge/Commits-Split%20Authorship-success)
![GitHub contributors](https://img.shields.io/github/contributors/yourusername/BIOPATTERN-PRO)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📖 Overview

**BioPattern-Pro** is an interactive Streamlit-based dashboard designed for **comparative analysis and visualization** of pattern matching algorithms on large-scale DNA sequences. 

The project provides comprehensive benchmarking of classical string matching algorithms (Naive, KMP, Boyer-Moore, Rabin-Karp) alongside advanced data structures (Suffix Arrays, Bloom Filters) on real genomic datasets, including *E. coli* K-12 and SARS-CoV-2 genomes.

This tool bridges theoretical algorithm knowledge with practical bioinformatics applications, offering researchers and students a platform to:
- Compare algorithm performance metrics (execution time, memory usage)
- Visualize pattern distribution across genomes
- Analyze motif discovery efficiency on biological data

---

## 🚀 Key Features

### ⚡ Multi-Algorithm Benchmarking
Compare the performance of six pattern matching algorithms:
- **Naive (Brute Force)** - Baseline algorithm
- **Rabin-Karp** - Hash-based matching
- **Knuth-Morris-Pratt (KMP)** - Prefix function optimization
- **Boyer-Moore** - Right-to-left scanning with heuristics
- **Suffix Array** - Index-based search structure
- **Bloom Filter** - Probabilistic data structure for pattern checking

### 📊 Advanced Visualization Suite
- **Genome Barcode**: Visual mapping of pattern occurrences across the genome
- **Pattern Density Heatmap**: Distribution analysis of motif density along genomic coordinates
- **Performance Comparison Charts**: Interactive bar charts and line plots for algorithm runtime and memory analysis
- **Statistical Summary Tables**: Comprehensive metrics for each algorithm

### 🧬 Large-Scale Data Support
- Process synthetic DNA sequences up to **200,000 base pairs**
- Support for real genomic datasets:
  - *Escherichia coli* K-12 genome (~4.6 Mb) - `ecoli.txt`
  - SARS-CoV-2 reference genome (~30 Kb) - `covid19.txt`
- Efficient memory management for large-scale analysis

### 🎨 Interactive User Interface
- Built with **Streamlit** for real-time data input and visualization
- Intuitive parameter controls for algorithm selection and pattern specification
- Responsive design with custom CSS styling
- Export functionality for results and visualizations

---

## 🛠️ Project Architecture & Team Contributions

This project follows a modular software engineering approach with clear separation of responsibilities:

| Component | Technologies | Responsible Team Member |
|:----------|:-------------|:------------------------|
| **Backend & Algorithm Implementation** | Python, NumPy, Algorithm Implementations (KMP, Boyer-Moore, Suffix Array, Bloom Filter) | **Büşra Çakmak** |
| **Frontend & Data Visualization** | Streamlit, Matplotlib, Pandas, CSS Styling, UI/UX Design | **Sena Nur Güngez** |
| **Joint Development** | Testing Framework, Benchmarking System, Documentation | **Both Contributors** |

---

## 📦 Installation & Setup

Follow these steps to run BioPattern-Pro locally on your machine.

### Prerequisites

- **Python 3.9+** installed on your system
- **pip** package manager
- **Git** for repository cloning

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/BIOPATTERN-PRO.git
cd BIOPATTERN-PRO
```

### 2. Create Virtual Environment

It is recommended to use a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 💻 Usage Guide

### Basic Workflow

1. **Select Data Source**: Choose between synthetic DNA generation or use provided genomic files (`ecoli.txt`, `covid19.txt`)
2. **Configure Parameters**: 
   - Set sequence length (for synthetic data)
   - Input target pattern to search
   - Select algorithms for comparison
3. **Run Analysis**: Execute the benchmark suite using `run_benchmark.py`
4. **Explore Results**:
   - View execution time and memory usage statistics
   - Analyze genome barcode visualization
   - Examine pattern density heatmaps
   - Export results for further analysis

### Example Use Case

**Searching for a promoter motif in *E. coli* genome:**

```python
# Input parameters
Pattern: "TATAAT"  # Pribnow box consensus sequence
Genome: ecoli.txt
Algorithms: KMP, Boyer-Moore, Suffix Array

# Expected output
- Number of matches found
- Execution time comparison
- Genomic location visualization
- Performance metrics table
```

---

## 📂 Project Structure

```
BIOPATTERN-PRO/
│
├── venv/                     # Virtual environment (ignored in git)
├── .gitignore               # Git ignore configuration
│
├── algorithms.py            # Core algorithm implementations
│                            # (Naive, KMP, Boyer-Moore, Rabin-Karp,
│                            #  Suffix Array, Bloom Filter)
│
├── app.py                   # Main Streamlit application
├── main.py                  # Command-line interface
├── setup.py                 # Package setup configuration
│
├── run_benchmark.py         # Benchmark execution script
├── tests.py                 # Unit tests for algorithms
├── visualization.py         # Plotting and charting functions
│
├── ecoli.txt                # E. coli K-12 genome dataset
├── covid19.txt              # SARS-CoV-2 genome dataset
├── text.txt                 # Additional test sequences
│
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation (this file)
```

---

## 📊 Performance Benchmarks

Experimental results on SARS-CoV-2 genome (29,903 bp) searching for pattern "ATTAA" (5 bp):

| Algorithm | Time (s) | Memory (Bytes) | Matches Found |
|:----------|----------:|---------------:|--------------:|
| Naive Search | 0.005121 | 568 | 60 |
| Rabin-Karp | 0.010948 | 568 | 60 |
| KMP Search | 0.006792 | 568 | 60 |
| Boyer-Moore | 0.003556 | 568 | 60 |
| Suffix Array | 0.000229 | 239,288 | 60 |
| Bloom Filter | 0.000011 | 1,600,056 | N/A (probabilistic) |

**Key Observations:**
- **Fastest Algorithm:** Bloom Filter (0.000011s) - 465x faster than Naive
- **Most Memory Efficient:** Naive, Rabin-Karp, KMP, Boyer-Moore (568 bytes)
- **Best Overall:** Boyer-Moore offers excellent balance (0.003556s, 568 bytes)
- **Trade-off:** Suffix Array and Bloom Filter sacrifice memory for speed

*Note: Results obtained on SARS-CoV-2 dataset (covid19.txt). Performance may vary based on genome size, pattern characteristics, and hardware specifications.*

---

## 🧪 Testing

Run the test suite to verify algorithm correctness:

```bash
python tests.py
```

Or use the benchmark script for comprehensive performance testing:

```bash
python run_benchmark.py
```

---

## 🚀 Running the Application

### Option 1: Streamlit Dashboard (Recommended)
```bash
streamlit run app.py
```

### Option 2: Command-Line Interface
```bash
python main.py --genome ecoli.txt --pattern ATCGATCG --algorithm kmp
```

### Option 3: Benchmark Mode
```bash
python run_benchmark.py --genome ecoli.txt --pattern TATAAT --all-algorithms
```

---

## 📚 References

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

2. Gusfield, D. (1997). *Algorithms on Strings, Trees, and Sequences: Computer Science and Computational Biology*. Cambridge University Press.

3. Knuth, D. E., Morris, J. H., & Pratt, V. R. (1977). Fast pattern matching in strings. *SIAM Journal on Computing*, 6(2), 323-350.

4. Boyer, R. S., & Moore, J. S. (1977). A fast string searching algorithm. *Communications of the ACM*, 20(10), 762-772.

5. NCBI GenBank Database. (2025). Retrieved from https://www.ncbi.nlm.nih.gov/genbank/

---

## 👥 Authors

This project was developed as part of the **Bioinformatics Algorithms** course at **Konya Food and Agriculture University**.

**Team Members:**

- **Büşra Çakmak** - Backend Development & Algorithm Implementation  
  GitHub: [@bckmk](https://github.com/bckmk)  
  Email: Busra.Cakmak@ogr.gidatarim.edu.tr

- **Sena Nur Güngez** - Frontend Development & Data Visualization  
  GitHub: [@senanurg](https://github.com/senanurg)  
  Email: Sena.Gungez@ogr.gidatarim.edu.tr

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Course Instructor: [Instructor Name]
- Konya Food and Agriculture University, Department of [Department Name]
- NCBI for providing publicly accessible genomic datasets

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please reach out via:
- GitHub Issues: [Create an Issue](https://github.com/yourusername/BIOPATTERN-PRO/issues)
- Email: Busra.Cakmak@ogr.gidatarim.edu.tr or Sena.Gungez@ogr.gidatarim.edu.tr

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**



