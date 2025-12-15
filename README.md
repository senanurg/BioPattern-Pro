# BioPattern-Pro
🧬 High-performance bioinformatics tool for genome sequencing and algorithm benchmarking (KMP, Boyer-Moore, Suffix Arrays) on large DNA datasets.


# 🧬 BioPattern Pro: Yüksek Performanslı Biyoinformatik Analiz Aracı

![GitHub top language](https://img.shields.io/github/languages/top/KullaniciAdiniz/BIOPATTERN-PRO?color=blue)
![GitHub commit activity](https://img.shields.io/badge/Commits-Split%20Authorship-success)
![GitHub contributors](https://img.shields.io/github/contributors/KullaniciAdiniz/BIOPATTERN-PRO)

BioPattern Pro, büyük ölçekli DNA dizileri üzerinde **Desen Eşleştirme Algoritmalarını** kıyaslamak ve görselleştirmek için tasarlanmış etkileşimli bir Streamlit panosudur.

Proje, hem klasik string eşleştirme algoritmalarının (KMP, Boyer-Moore) performansını hem de Biyoinformatikteki uygulama alanlarını (örneğin, SARS-CoV-2 ve E. coli genomları) derinlemesine incelemektedir.

## 🚀 Temel Özellikler

* **Çoklu Algoritma Kıyaslaması:** Naive, Rabin-Karp, KMP, Boyer-Moore, Suffix Array ve Bloom Filter gibi algoritmaların yürütme süresi (Time) ve bellek (Memory) metrikleri ile karşılaştırılması.
* **Büyük Veri Desteği:** 200k bp'ye kadar sentetik DNA ve gerçekçi genom (E. coli K-12) verilerini işleyebilme yeteneği.
* **İleri Görselleştirme:**
    * **Genome Barcode:** Bulunan motiflerin genom üzerindeki konumlarının haritalanması.
    * **Pattern Density Heatmap:** Desen yoğunluğunun genom boyunca dağılım grafiği.
    * **Performans Grafiği:** Algoritma hızlarının görsel olarak kıyaslanması.
* **İnteraktif Arayüz:** Streamlit ile oluşturulmuş, anlık veri girişi ve sonuç gösterimi sunan kullanıcı dostu tasarım.

## 🛠️ Proje Yapısı ve Ekip Katkısı

Bu proje, güçlü bir mühendislik yapısı kullanılarak geliştirilmiş ve katkılar yazılım alanlarına göre ayrılmıştır:

| Alan | Kullanılan Teknolojiler | Sorumlu Ekip Üyesi |
| :--- | :--- | :--- |
| **Backend & Core Logic** | Python, KMP, Boyer-Moore, Suffix Array, Bloom Filter Implementasyonları | **Büşra Çakmak** |
| **Frontend & Visualization**| Streamlit, Matplotlib, Pandas, CSS Styling, UI/UX | **Sena Nur Güngez** |

## 📦 Kurulum ve Çalıştırma

Projenin yerel bilgisayarınızda çalışması için aşağıdaki adımları izleyin.

### Ön Koşullar

Bilgisayarınızda Python 3.9+ kurulu olmalıdır.

### 1. Depoyu Klonlama

Terminalde aşağıdaki komutu kullanarak projeyi GitHub'dan indirin:

```bash
git clone [https://github.com/KullaniciAdiniz/BIOPATTERN-PRO.git](https://github.com/KullaniciAdiniz/BIOPATTERN-PRO.git)
cd BIOPATTERN-PRO
````

### 2\. Sanal Ortam Oluşturma ve Kütüphane Kurulumu

Projenin bağımlılıklarını izole etmek için bir sanal ortam oluşturun ve `requirements.txt` dosyasındaki kütüphaneleri kurun:

```bash
# Sanal ortamı oluştur
python -m venv venv

# Sanal ortamı aktif et (Windows)
.\venv\Scripts\activate 
# Sanal ortamı aktif et (Mac/Linux)
# source venv/bin/activate 

# Gerekli kütüphaneleri kur
pip install -r requirements.txt
```

### 3\. Uygulamayı Başlatma

Sanal ortam aktifken, uygulamayı Streamlit ile çalıştırın:

```bash
streamlit run app.py
```

Uygulama otomatik olarak web tarayıcınızda açılacaktır.

-----

### 👥 Proje Yazarları

Bu proje, Biyoinformatik Proje Dersi kapsamında iki kişilik bir ekip çalışmasıyla tamamlanmıştır:

  * **Büşra Çakmak** - [https://github.com/bckmk]
  * **Sena Nur Güngez** - [https://github.com/senanurg]

<!-- end list -->

```
```