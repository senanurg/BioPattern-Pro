import urllib.request
import os

def download_genome(url, filename, name):
    print(f"⏳ {name} indiriliyor...")
    try:
        # Veriyi internetten çek
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        
        # FASTA başlığını (ilk satırı) at ve satır sonlarını temizle
        lines = data.split('\n')
        # İlk satır genelde ">NC_00..." gibi bir başlıktır, onu almıyoruz
        genome_data = ''.join(lines[1:]).replace('\n', '').upper()
        
        # Sadece A, C, G, T harflerini tut (Temizlik)
        clean_data = ''.join([c for c in genome_data if c in 'ACGT'])
        
        # Dosyaya kaydet
        with open(filename, 'w') as f:
            f.write(clean_data)
            
        print(f"✅ BAŞARILI: {filename} kaydedildi! ({len(clean_data):,} bp)")
        
    except Exception as e:
        print(f"❌ HATA: {name} indirilemedi. Sebep: {e}")

if __name__ == "__main__":
    print("--- 🧬 BioPattern Veri İndirme Aracı ---")
    
    # 1. SARS-CoV-2 (Covid-19) - Wuhan-Hu-1 Referans Genomu
    covid_url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1798174254&extrafeat=null&conwithfeat=on&hide-cdd=on"
    download_genome(covid_url, "covid19.txt", "SARS-CoV-2 (Covid-19)")
    
    # 2. E. coli K-12 (Bakteri) - MG1655 Referans Genomu
    ecoli_url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=556503834&extrafeat=null&conwithfeat=on&hide-cdd=on"
    download_genome(ecoli_url, "ecoli.txt", "E. coli K-12 (Bakteri)")
    
    print("\n🎉 Tüm veriler hazır! Şimdi 'streamlit run app.py' diyebilirsin.")