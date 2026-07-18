# MeatSight.AI - Analisis Klasifikasi Kesegaran Daging

Capstone Project ini merupakan tugas akhir untuk mata kuliah Kecerdasan Buatan (Fokus Studi: Computer Vision). Proyek ini menerapkan pendekatan **Transfer Learning** menggunakan arsitektur MobileNetV2 dan VGG16 untuk mengklasifikasikan tingkat kesegaran daging, serta menyajikannya dalam antarmuka web interaktif menggunakan Flask.

## Tema Proyek
**Klasifikasi Gambar (Image Classification)** - Deteksi dan klasifikasi tingkat kesegaran daging (Fresh, Half-Fresh, Spoiled). 

Alasan pemilihan tema ini adalah untuk mengeksplorasi penerapan *Computer Vision* pada komoditas pangan yang dapat membantu masyarakat awam atau industri dalam mendeteksi kelayakan konsumsi daging secara cepat dan akurat. Eksperimen ini membandingkan kinerja model modern yang efisien (MobileNetV2) dengan model klasik yang lebih berat (VGG16).

## Sumber Dataset
Dataset gambar daging diperoleh dari Kaggle. Dataset ini terbagi menjadi tiga kategori kelas utama:
- `Fresh` (Daging Segar)
- `Half-Fresh` (Daging Mulai Menurun Kualitasnya)
- `Spoiled` (Daging Busuk)

## Struktur Direktori
- `dataset/`: Berisi dataset gambar latih (`train`) dan validasi (`val`).
- `models/`: Tempat penyimpanan model hasil training (file `best_model.h5`).
- `notebooks/`: File Jupyter Notebook untuk *pipeline* pemrosesan data, pelatihan, dan evaluasi model.
- `static/`: Berisi aset statis web (CSS, JS) dan folder `uploads/` untuk gambar *testing*.
- `templates/`: Berisi antarmuka web (`index.html`).
- `app.py`: *Script* utama backend berbasis Flask.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.

## Petunjuk Cara Menjalankan Kode

### 1. Persiapan Environment
Pastikan Python 3.8+ sudah terinstal. Buka terminal dan arahkan ke direktori root proyek ini, lalu instal dependensi:
```bash
pip install -r requirements.txt
```

### 2. Pelatihan Model (Training)
Jika Anda belum memiliki file model (`best_model.h5`), Anda harus melatih modelnya terlebih dahulu:
- Jalankan melalui Jupyter Notebook dengan mengeksekusi sel pada file `notebooks/Training_dan_Evaluasi.ipynb`.
- **ATAU** jalankan melalui *command line*:
  ```bash
  python notebooks/training_pipeline.py
  ```
Pastikan dataset gambar sudah disusun rapi di sub-folder dalam `dataset/train/` dan `dataset/val/`.

### 3. Menjalankan Aplikasi Web
Untuk menjalankan antarmuka prediksi *real-time*, jalankan Flask server dengan perintah:
```bash
python app.py
```
Setelah server berjalan, buka browser dan akses alamat lokal: **`http://127.0.0.1:5000`**

Anda tinggal mengunggah (*drag & drop*) foto daging ke area yang disediakan, lalu AI akan secara otomatis memprediksi tingkat kesegarannya.
