import urllib.request
import os

def download_genome(url, filename, name):
    print(f"⏳ Downloading {name}...")
    try:
        # Fetch data from URL
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        
        # Parse FASTA format (Skip header, join lines)
        lines = data.split('\n')
        # Skip the first line (header starting with >) and clean newlines
        genome_data = ''.join(lines[1:]).replace('\n', '').upper()
        
        # Data Cleaning: Keep only valid nucleotides (A, C, G, T)
        clean_data = ''.join([c for c in genome_data if c in 'ACGT'])
        
        # Save to file
        with open(filename, 'w') as f:
            f.write(clean_data)
            
        print(f"✅ SUCCESS: {filename} saved! ({len(clean_data):,} bp)")
        
    except Exception as e:
        print(f"❌ ERROR: Could not download {name}. Reason: {e}")

if __name__ == "__main__":
    print("--- 🧬 BioPattern Data Downloader ---")
    
    # 1. SARS-CoV-2 (Covid-19) - Wuhan-Hu-1 Reference Genome
    covid_url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1798174254&extrafeat=null&conwithfeat=on&hide-cdd=on"
    download_genome(covid_url, "covid19.txt", "SARS-CoV-2 (Covid-19)")
    
    # 2. E. coli K-12 (Bacteria) - MG1655 Reference Genome
    ecoli_url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=556503834&extrafeat=null&conwithfeat=on&hide-cdd=on"
    download_genome(ecoli_url, "ecoli.txt", "E. coli K-12 (Bacteria)")
    
    print("\n🎉 All datasets are ready! You can now run 'streamlit run app.py'.")