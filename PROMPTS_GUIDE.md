# 📝 Panduan Prompt untuk Menghasilkan Hasil Penelitian

## 🎯 Tujuan
Dokumen ini berisi prompt yang bisa digunakan untuk **menghasilkan hasil penelitian lengkap** (seperti yang ada di folder `hasil/`) dari project IndoT5 Hybrid Paraphraser untuk keperluan skripsi/penelitian.

---

## 🔬 PROMPT UTAMA: Menghasilkan Hasil Penelitian Lengkap

### Prompt untuk Eksekusi Lengkap
```
Saya ingin melakukan pengujian hasil dari program IndoT5 Hybrid Paraphraser 
lalu simpan dalam folder 'hasil' karena ini adalah hasil penelitian.

Jalankan:
1. Single experiment dengan berbagai metode (hybrid, neural, rule-based)
2. Batch testing dengan 10-20 kalimat sample
3. Quality analysis dan comparison report
4. Generate output dalam format JSON dan CSV
5. Buat laporan HTML seperti Bab 4 skripsi dengan screenshot placeholders

Dataset sample:
[Berikan 10-20 kalimat dalam bahasa Indonesia yang relevan dengan domain penelitian]

Simpan semua hasil di folder 'hasil/' dengan struktur:
- experiments/
- batch_results/
- quality_analysis/
- comparison_reports/
- screenshots/
```

### Contoh Prompt Spesifik
```
Saya ingin melakukan pengujian sistem parafrase IndoT5 Hybrid untuk penelitian skripsi.

Dataset (20 kalimat dari domain pendidikan):
1. "Pendidikan merupakan kunci utama untuk membangun masa depan yang cerah."
2. "Teknologi informasi berkembang sangat pesat di era digital ini."
3. "Penelitian ini bertujuan untuk menganalisis pengaruh metode pembelajaran."
4. "Sistem pembelajaran online memberikan fleksibilitas bagi mahasiswa."
5. "Kualitas pendidikan di Indonesia masih perlu ditingkatkan."
6. "Guru memiliki peran penting dalam proses belajar mengajar."
7. "Kurikulum harus disesuaikan dengan perkembangan zaman."
8. "Evaluasi pembelajaran dilakukan secara berkala setiap semester."
9. "Mahasiswa aktif berpartisipasi dalam kegiatan akademik."
10. "Literasi digital sangat penting di era modern ini."
[... tambahkan 10 kalimat lagi]

Jalankan pengujian dengan:
- Metode: Hybrid, Neural, Rule-based (bandingkan)
- Generate 3 variasi per kalimat
- Hitung metrics: quality score, semantic similarity, lexical diversity
- Simpan hasil dalam format JSON dan CSV
- Buat laporan HTML lengkap dengan screenshot placeholders

Output yang diinginkan:
✅ File JSON per-experiment
✅ Batch results dengan comparison
✅ Quality analysis report
✅ CSV untuk analisis SPSS/Excel
✅ HTML report (Bab 4 skripsi style)
```

---

## 1️⃣ PROMPT: Single Experiment Testing

### Format Prompt
```
Jalankan single experiment dengan kalimat:
"{KALIMAT_TEST}"

Gunakan metode: {hybrid/neural/rule-based}

Output yang diinginkan:
- Original text
- Paraphrased text
- Quality metrics (quality_score, semantic_similarity, lexical_diversity, fluency)
- Processing time
- Transformations applied
- Simpan ke: hasil/experiments/experiment_TIMESTAMP.json
```

### Contoh Eksekusi
```python
python -c "
from engines.indot5_hybrid_engine import IndoT5HybridParaphraser
import json
from datetime import datetime

paraphraser = IndoT5HybridParaphraser()

text = 'Pendidikan merupakan kunci utama untuk membangun masa depan yang cerah.'
result = paraphraser.paraphrase(text, method='hybrid')

output = {
    'timestamp': datetime.now().isoformat(),
    'original': result.original_text,
    'paraphrased': result.paraphrased_text,
    'method': result.method_used,
    'quality_score': result.quality_score,
    'semantic_similarity': result.semantic_similarity,
    'lexical_diversity': result.lexical_diversity,
    'fluency_score': result.fluency_score,
    'processing_time': result.processing_time,
    'transformations': result.transformations_applied
}

with open('hasil/experiments/experiment_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print('✅ Single experiment saved!')
"
```

---

## 2️⃣ PROMPT: Batch Testing (10-20 Kalimat)

### Format Prompt
```
Jalankan batch testing untuk dataset berikut:

[DATASET 10-20 KALIMAT]

Untuk setiap kalimat:
1. Parafrase menggunakan metode hybrid
2. Generate 3 variasi
3. Hitung quality metrics
4. Catat processing time

Simpan hasil ke:
- hasil/batch_results/batch_hybrid_TIMESTAMP.json
```

### Contoh Eksekusi
```python
python run_research_test.py --mode batch --dataset data/research_input.txt --method hybrid --output hasil/batch_results/
```

### Output yang Diharapkan
```json
{
  "timestamp": "2026-01-14T10:30:00",
  "method": "hybrid",
  "total_sentences": 20,
  "success_count": 20,
  "success_rate": 100.0,
  "average_quality": 68.75,
  "average_semantic_similarity": 0.89,
  "average_processing_time": 2.34,
  "results": [
    {
      "sentence_id": 1,
      "original": "...",
      "variations": ["...", "...", "..."],
      "quality_scores": [68.5, 71.2, 65.8],
      "semantic_similarities": [0.91, 0.88, 0.93]
    }
  ]
}
```

---

## 3️⃣ PROMPT: Quality Analysis & Statistics

### Format Prompt
```
Lakukan analisis kualitas lengkap untuk batch results yang sudah ada.

Analisis yang dibutuhkan:
1. Distribusi quality score (min, max, mean, std)
2. Distribusi semantic similarity
3. Distribusi lexical diversity
4. Processing time statistics
5. Success rate
6. Best/worst performing sentences

Simpan hasil ke:
- hasil/quality_analysis/quality_report_TIMESTAMP.json
- hasil/quality_analysis/results_hybrid_TIMESTAMP.csv (untuk SPSS/Excel)
```

### Contoh Eksekusi
```python
python run_research_test.py --mode quality-analysis --input hasil/batch_results/batch_hybrid_*.json --output hasil/quality_analysis/
```

### Output CSV untuk SPSS
```csv
sentence_id,method,original_length,paraphrased_length,quality_score,semantic_similarity,lexical_diversity,fluency_score,processing_time,success
1,hybrid,65,68,68.50,0.91,0.45,0.88,2.3,True
2,hybrid,72,75,71.20,0.88,0.52,0.85,2.5,True
3,hybrid,58,61,65.80,0.93,0.38,0.91,2.1,True
...
```

---

## 4️⃣ PROMPT: Method Comparison (Hybrid vs Neural vs Rule-based)

### Format Prompt
```
Bandingkan 3 metode parafrase untuk semua kalimat dalam dataset:

Dataset: [DATASET]

Metode yang dibandingkan:
1. Hybrid (Neural + Rule-based)
2. Neural (IndoT5 only)
3. Rule-based (Transformasi only)

Untuk setiap metode, hitung:
- Average quality score
- Average semantic similarity
- Average lexical diversity
- Average processing time
- Success rate

Simpan comparison report ke:
- hasil/comparison_reports/comparison_TIMESTAMP.json
```

### Contoh Eksekusi
```python
python run_research_test.py --mode comparison --dataset data/research_input.txt --output hasil/comparison_reports/
```

### Output Comparison JSON
```json
{
  "timestamp": "2026-01-14T11:00:00",
  "dataset_size": 20,
  "methods": {
    "hybrid": {
      "avg_quality_score": 68.75,
      "avg_semantic_similarity": 0.89,
      "avg_lexical_diversity": 0.45,
      "avg_processing_time": 2.34,
      "success_rate": 100.0,
      "strengths": ["Konsisten", "Kualitas tinggi", "Seimbang"],
      "weaknesses": ["Processing time lebih lama"]
    },
    "neural": {
      "avg_quality_score": 55.23,
      "avg_semantic_similarity": 0.76,
      "avg_lexical_diversity": 0.58,
      "avg_processing_time": 1.89,
      "success_rate": 95.0,
      "strengths": ["Variasi tinggi", "Cepat"],
      "weaknesses": ["Kualitas tidak konsisten", "Semantic similarity rendah"]
    },
    "rule-based": {
      "avg_quality_score": 72.10,
      "avg_semantic_similarity": 0.95,
      "avg_lexical_diversity": 0.35,
      "avg_processing_time": 0.45,
      "success_rate": 100.0,
      "strengths": ["Akurat", "Cepat", "Konsisten"],
      "weaknesses": ["Variasi terbatas"]
    }
  },
  "recommendation": "Hybrid method memberikan hasil terbaik dengan keseimbangan quality, semantic similarity, dan variasi."
}
```

---

## 5️⃣ PROMPT: Generate Laporan HTML (Bab 4 Skripsi)

### Format Prompt
```
Buatkan laporan HTML lengkap untuk Bab 4 Hasil Penelitian dengan struktur:

4.1 Gambaran Umum Sistem
4.2 Hasil Pengujian
   - Screenshot web interface
   - Screenshot terminal testing
4.3 Hasil Parafrase per Metode
   - Tabel hasil hybrid
   - Tabel hasil neural
   - Tabel hasil rule-based
4.4 Analisis Metrik Kualitas
   - Quality score distribution
   - Semantic similarity analysis
   - Lexical diversity analysis
4.5 Perbandingan Metode
   - Tabel comparison
   - Grafik perbandingan
4.6 Struktur Output
   - JSON format
   - CSV format
4.7 Pembahasan
4.8 Ringkasan Hasil

Include:
- Screenshot placeholders (11 screenshots)
- Tabel dengan data real dari hasil testing
- Grafik/chart untuk visualisasi
- Styling profesional (CSS)

Simpan ke: hasil/BAB_4_HASIL_PENELITIAN.html
```

### Screenshot yang Diperlukan
```
1. Screenshot halaman utama web interface
2. Screenshot form input teks
3. Screenshot hasil parafrase (3 variasi)
4. Screenshot konfigurasi sistem (config.json)
5. Screenshot terminal batch testing
6. Screenshot file batch_results JSON
7. Screenshot quality_analysis JSON
8. Screenshot comparison_reports JSON
9. Screenshot folder struktur hasil/
10. Screenshot CSV file di Excel
11. Screenshot log eksperimen
```

---

## 6️⃣ PROMPT: Complete Research Pipeline

---

## 6️⃣ PROMPT: Complete Research Pipeline

### Master Prompt (All-in-One)
```
Jalankan pipeline penelitian lengkap untuk project IndoT5 Hybrid Paraphraser:

STEP 1: Persiapan Dataset
- Buat file data/research_input.txt dengan 20 kalimat sample
- Domain: [pendidikan/teknologi/umum]

STEP 2: Single Experiment
- Test 1 kalimat dengan 3 metode
- Simpan ke hasil/experiments/

STEP 3: Batch Testing
- Test semua 20 kalimat dengan metode hybrid
- Generate 3 variasi per kalimat
- Simpan ke hasil/batch_results/

STEP 4: Quality Analysis
- Analisis distribusi metrics
- Generate CSV untuk SPSS
- Simpan ke hasil/quality_analysis/

STEP 5: Method Comparison
- Bandingkan hybrid vs neural vs rule-based
- Simpan ke hasil/comparison_reports/

STEP 6: Generate Laporan HTML
- Buat Bab 4 Hasil Penelitian
- Include screenshot placeholders
- Simpan ke hasil/BAB_4_HASIL_PENELITIAN.html

STEP 7: Screenshot Collection
- Ambil 11 screenshot sesuai panduan
- Simpan ke hasil/screenshots/

Output akhir:
✅ hasil/experiments/*.json
✅ hasil/batch_results/*.json
✅ hasil/quality_analysis/*.json + *.csv
✅ hasil/comparison_reports/*.json
✅ hasil/BAB_4_HASIL_PENELITIAN.html
✅ hasil/screenshots/*.png
```

### Eksekusi via Script
```bash
# Jalankan complete research pipeline
python run_research_test.py --mode complete --dataset-size 20 --domain pendidikan

# Output:
# ✅ Dataset created: data/research_input.txt (20 kalimat)
# ✅ Single experiment: hasil/experiments/experiment_20260114_103000.json
# ✅ Batch testing: hasil/batch_results/batch_hybrid_20260114_103500.json
# ✅ Quality analysis: hasil/quality_analysis/quality_report_20260114_104000.json
# ✅ Method comparison: hasil/comparison_reports/comparison_20260114_104500.json
# ✅ HTML report: hasil/BAB_4_HASIL_PENELITIAN.html
# 
# 📸 Sekarang ambil 11 screenshot sesuai panduan di laporan HTML
```

---

## 7️⃣ Dataset Sample Templates

### Template 1: Domain Pendidikan
```
1. Pendidikan merupakan kunci utama untuk membangun masa depan yang cerah.
2. Teknologi informasi berkembang sangat pesat di era digital ini.
3. Penelitian ini bertujuan untuk menganalisis pengaruh metode pembelajaran.
4. Sistem pembelajaran online memberikan fleksibilitas bagi mahasiswa.
5. Kualitas pendidikan di Indonesia masih perlu ditingkatkan.
6. Guru memiliki peran penting dalam proses belajar mengajar.
7. Kurikulum harus disesuaikan dengan perkembangan zaman.
8. Evaluasi pembelajaran dilakukan secara berkala setiap semester.
9. Mahasiswa aktif berpartisipasi dalam kegiatan akademik.
10. Literasi digital sangat penting di era modern ini.
11. Metode pembelajaran inovatif meningkatkan motivasi belajar siswa.
12. Pendidikan karakter harus ditanamkan sejak dini.
13. Infrastruktur pendidikan perlu mendapat perhatian khusus.
14. Kompetensi guru harus terus ditingkatkan melalui pelatihan.
15. Akses pendidikan yang merata menjadi tantangan utama.
16. Media pembelajaran interaktif membantu pemahaman siswa.
17. Kolaborasi antar institusi pendidikan sangat diperlukan.
18. Riset dan pengembangan menjadi bagian penting dalam pendidikan.
19. Standar nasional pendidikan harus terus diperbarui.
20. Partisipasi orang tua berpengaruh terhadap prestasi anak.
```

### Template 2: Domain Teknologi
```
1. Artificial intelligence mengubah cara kerja berbagai industri.
2. Sistem keamanan siber menjadi prioritas utama perusahaan.
3. Cloud computing menawarkan solusi penyimpanan data yang efisien.
4. Internet of Things menghubungkan perangkat secara terintegrasi.
5. Big data analytics membantu pengambilan keputusan bisnis.
6. Machine learning meningkatkan akurasi prediksi sistem.
7. Blockchain technology menjamin transparansi transaksi digital.
8. Aplikasi mobile berkembang pesat di berbagai platform.
9. Virtual reality menciptakan pengalaman immersive bagi pengguna.
10. Automation technology mengoptimalkan proses produksi.
[... tambah 10 kalimat teknologi lagi]
```

### Template 3: Domain Umum/Akademik
```
1. Berdasarkan hasil analisis data, dapat disimpulkan bahwa terdapat korelasi positif.
2. Penelitian ini menggunakan metode kualitatif dengan pendekatan studi kasus.
3. Sampel penelitian dipilih menggunakan teknik purposive sampling.
4. Instrumen penelitian telah melalui uji validitas dan reliabilitas.
5. Data dikumpulkan melalui wawancara mendalam dan observasi partisipatif.
6. Analisis data dilakukan dengan teknik triangulasi sumber.
7. Hasil penelitian menunjukkan bahwa faktor X berpengaruh signifikan terhadap Y.
8. Temuan penelitian ini sejalan dengan teori yang dikemukakan oleh Smith.
9. Keterbatasan penelitian terletak pada jumlah sampel yang terbatas.
10. Rekomendasi penelitian lebih lanjut adalah memperluas cakupan subjek penelitian.
[... tambah 10 kalimat akademik lagi]
```

---

## 8️⃣ Checklist Pengumpulan Data Penelitian

### ☑️ Pre-Testing Checklist
```
□ Install semua dependencies (transformers, torch, flask, dll)
□ Download model IndoT5-base
□ Verifikasi folder struktur (data/, hasil/, engines/)
□ Siapkan dataset 20 kalimat sesuai domain penelitian
□ Test web interface berjalan (http://localhost:5000)
□ Test terminal script berjalan (python run_research_test.py)
```

### ☑️ Testing Checklist
```
□ Jalankan single experiment (1 kalimat, 3 metode)
□ Jalankan batch testing (20 kalimat, hybrid method)
□ Generate quality analysis report
□ Generate method comparison report
□ Verifikasi semua file JSON tersimpan
□ Export CSV untuk analisis statistik
```

### ☑️ Documentation Checklist
```
□ Generate HTML report (Bab 4 skripsi)
□ Screenshot 1: Halaman utama web
□ Screenshot 2: Form input teks
□ Screenshot 3: Hasil parafrase (3 variasi)
□ Screenshot 4: Konfigurasi sistem
□ Screenshot 5: Terminal batch testing
□ Screenshot 6: File batch_results JSON
□ Screenshot 7: Quality analysis JSON
□ Screenshot 8: Comparison reports JSON
□ Screenshot 9: Folder struktur hasil/
□ Screenshot 10: CSV di Excel/SPSS
□ Screenshot 11: Log eksperimen
□ Isi placeholder screenshot di HTML report
□ Review dan finalisasi laporan
```

---

## 9️⃣ Expected Output Structure

Setelah menjalankan complete pipeline, folder `hasil/` akan berisi:

```
hasil/
├── BAB_4_HASIL_PENELITIAN.html          # Laporan HTML lengkap
├── experiments/
│   ├── experiment_20260114_103000.json  # Single experiment hybrid
│   ├── experiment_20260114_103010.json  # Single experiment neural
│   └── experiment_20260114_103020.json  # Single experiment rule-based
├── batch_results/
│   ├── batch_hybrid_20260114_103500.json      # Batch 20 kalimat - hybrid
│   ├── batch_neural_20260114_103800.json      # Batch 20 kalimat - neural
│   └── batch_rulebased_20260114_104000.json   # Batch 20 kalimat - rule-based
├── quality_analysis/
│   ├── quality_report_20260114_104200.json    # Analisis statistik
│   ├── results_hybrid_20260114_104200.csv     # Data untuk SPSS
│   ├── results_neural_20260114_104200.csv
│   └── results_rulebased_20260114_104200.csv
├── comparison_reports/
│   └── comparison_20260114_104500.json        # Perbandingan 3 metode
└── screenshots/
    ├── 01_halaman_utama.png
    ├── 02_input_form.png
    ├── 03_hasil_parafrase.png
    ├── 04_konfigurasi.png
    ├── 05_terminal_testing.png
    ├── 06_batch_results.png
    ├── 07_quality_analysis.png
    ├── 08_comparison_report.png
    ├── 09_folder_struktur.png
    ├── 10_csv_excel.png
    └── 11_log_eksperimen.png
```

---

## 🔟 Key Metrics untuk Bab 4

### Tabel Hasil Utama yang Harus Ada:

**Tabel 4.1: Hasil Pengujian Single Experiment**
| Metode | Original | Paraphrased | Quality | Semantic | Lexical | Time |
|--------|----------|-------------|---------|----------|---------|------|
| Hybrid | ... | ... | 68.5% | 0.91 | 0.45 | 2.3s |
| Neural | ... | ... | 55.2% | 0.76 | 0.58 | 1.9s |
| Rule-based | ... | ... | 72.1% | 0.95 | 0.35 | 0.5s |

**Tabel 4.2: Statistik Batch Testing (20 Kalimat)**
| Metric | Min | Max | Mean | Std Dev |
|--------|-----|-----|------|---------|
| Quality Score | 52.3 | 81.7 | 68.75 | 8.42 |
| Semantic Similarity | 0.72 | 0.98 | 0.89 | 0.07 |
| Lexical Diversity | 0.28 | 0.65 | 0.45 | 0.11 |
| Processing Time | 1.8 | 3.2 | 2.34 | 0.38 |

**Tabel 4.3: Perbandingan 3 Metode**
| Metode | Avg Quality | Avg Semantic | Success Rate | Avg Time |
|--------|-------------|--------------|--------------|----------|
| Hybrid | 68.75% | 0.89 | 100% | 2.34s |
| Neural | 55.23% | 0.76 | 95% | 1.89s |
| Rule-based | 72.10% | 0.95 | 100% | 0.45s |

---

## 1️⃣1️⃣ Prompt Template untuk Chat AI

### Untuk Copilot/ChatGPT
```
Saya sedang mengerjakan skripsi tentang sistem parafrase bahasa Indonesia 
menggunakan IndoT5 Hybrid Paraphraser.

Saya butuh hasil penelitian lengkap untuk Bab 4 dengan struktur:
1. Pengujian single experiment (3 metode)
2. Batch testing (20 kalimat)
3. Quality analysis
4. Method comparison
5. Laporan HTML

Project location: D:\devnolife\paraphrase\

Tolong bantu saya:
1. Buat dataset 20 kalimat domain [pendidikan/teknologi]
2. Jalankan testing lengkap
3. Generate semua report (JSON + CSV)
4. Buat laporan HTML Bab 4 skripsi
5. Panduan screenshot yang diperlukan

Output yang diinginkan ada di folder hasil/ dengan struktur lengkap.
```

---

## 1️⃣2️⃣ FAQ Penelitian

### Q: Berapa jumlah kalimat minimal untuk penelitian?
**A:** Minimal 20 kalimat untuk statistik yang valid. Ideal: 50-100 kalimat.

### Q: Metode mana yang terbaik untuk penelitian?
**A:** Hybrid method - memberikan keseimbangan terbaik antara quality, accuracy, dan variasi.

### Q: Bagaimana cara menganalisis hasil di SPSS?
**A:** Export CSV dari `hasil/quality_analysis/`, import ke SPSS, lakukan descriptive statistics dan correlation analysis.

### Q: Apakah perlu GPU untuk penelitian?
**A:** Tidak wajib. CPU cukup untuk dataset 20-50 kalimat. GPU mempercepat untuk dataset >100 kalimat.

### Q: Format laporan untuk skripsi?
**A:** Gunakan HTML report yang sudah di-generate, atau export ke Word/PDF sesuai format kampus.

---

## 1️⃣3️⃣ Citation & References

### Cara Sitasi Project Ini
```
[APA Style]
Paraphraser, I. H. (2026). IndoT5 Hybrid Paraphraser: Indonesian Paraphrasing System 
using Neural and Rule-based Approaches. GitHub. https://github.com/devnolife/indot5-parafse

[IEEE Style]
IndoT5 Hybrid Paraphraser, "Indonesian Paraphrasing System using Neural and 
Rule-based Approaches," 2026. [Online]. Available: https://github.com/devnolife/indot5-parafse
```

### Model Citation
```
Wikidepia. (2023). IndoT5-base: Indonesian T5 Model. Hugging Face. 
https://huggingface.co/Wikidepia/IndoT5-base
```

---

**Terakhir Diupdate**: 14 Januari 2026
**Versi**: 2.0.0 (Research Edition)
**Penulis**: IndoT5 Hybrid Paraphraser Research Team

---

## 📞 Support

Dokumentasi lengkap: [README.md](README.md)
Contoh script: `run_research_test.py`
Contoh hasil: folder `hasil/`

---

**Terakhir Diupdate**: 14 Januari 2026
**Versi**: 2.0.0 (Research Edition)
**Author**: IndoT5 Hybrid Paraphraser Team

---

## 2️⃣ Prompt untuk Parafrase Akademik

### Format Akademik
```
Ubah kalimat akademik berikut menjadi variasi yang tetap formal:
"{TEKS_AKADEMIK}"

Persyaratan:
- Pertahankan terminologi teknis
- Gunakan struktur kalimat akademik
- Hindari perubahan makna substansial
- Metode: Hybrid
```

### Contoh Prompt Akademik
```
Ubah kalimat akademik berikut menjadi variasi yang tetap formal:
"Berdasarkan hasil analisis data, dapat disimpulkan bahwa terdapat korelasi positif antara variabel X dan variabel Y."

Gunakan metode hybrid dengan kualitas minimum 70%.
```

### Hasil yang Diharapkan
- Variasi 1: Berdasarkan analisis data, terlihat adanya hubungan positif antara variabel X dan Y
- Variasi 2: Hasil analisis menunjukkan korelasi positif antara kedua variabel tersebut
- Variasi 3: Dari hasil analisis, dapat diketahui bahwa variabel X dan Y memiliki korelasi positif

---

## 3️⃣ Prompt untuk Batch Processing (Dokumen Besar)

### Format Batch
```
Parafrasakan dokumen berikut secara keseluruhan:

[UPLOAD FILE PDF/TXT]

Pengaturan:
- Metode: Hybrid
- Processing: Per-chunk otomatis
- Kualitas minimum: 65%
- Gabungkan hasil chunk menjadi dokumen lengkap
```

### Contoh Prompt Batch
```
Parafrasakan dokumen penelitian berikut (10 halaman):
[Upload: penelitian_metode_kualitatif.pdf]

Gunakan:
- Metode: Hybrid untuk konsistensi
- Chunking otomatis (2000 karakter per chunk)
- Pertahankan struktur paragraf asli
```

### Hasil yang Diharapkan
- File terupload dan di-extract
- Dibagi menjadi N chunks
- Setiap chunk diparafrase
- Hasil digabung menjadi dokumen utuh
- Laporan kualitas per-chunk tersedia

---

## 4️⃣ Prompt untuk Comparison Testing

### Format Comparison
```
Bandingkan 3 metode parafrase untuk kalimat berikut:
"{TEKS}"

Metode yang dibandingkan:
1. Hybrid (Neural + Rule-based)
2. Neural (IndoT5 only)
3. Rule-based (Transformasi only)

Evaluasi berdasarkan:
- Quality Score
- Semantic Similarity
- Lexical Diversity
- Fluency
```

### Contoh Prompt Comparison
```
Bandingkan 3 metode untuk kalimat:
"Teknologi informasi berkembang pesat di era digital ini."

Gunakan masing-masing metode dengan pengaturan default.
Simpan hasil comparison dalam format JSON.
```

### Hasil yang Diharapkan
```json
{
  "original": "Teknologi informasi berkembang pesat di era digital ini.",
  "methods": {
    "hybrid": {
      "result": "Teknologi informasi mengalami perkembangan cepat pada era digital ini.",
      "quality_score": 68.5,
      "semantic_similarity": 0.92
    },
    "neural": {
      "result": "Teknologi berkembang sangat cepat di era modern.",
      "quality_score": 55.2,
      "semantic_similarity": 0.78
    },
    "rule-based": {
      "result": "Teknologi informasi bertumbuh pesat pada era digital ini.",
      "quality_score": 72.1,
      "semantic_similarity": 0.95
    }
  }
}
```

---

## 5️⃣ Prompt untuk Quality Analysis

### Format Quality Analysis
```
Lakukan analisis kualitas batch untuk dataset berikut:
[INPUT: 20 kalimat sample]

Analisis yang dibutuhkan:
- Distribusi quality score
- Average semantic similarity
- Lexical diversity range
- Processing time per sentence
- Success rate

Output: CSV + JSON report
```

### Contoh Prompt Quality Analysis
```
Analisis kualitas parafrase untuk 20 kalimat sample:

Dataset:
1. "Pendidikan adalah kunci masa depan."
2. "Teknologi mengubah cara kita belajar."
3. "Penelitian memerlukan metode yang tepat."
... (17 kalimat lainnya)

Gunakan metode hybrid, simpan laporan di folder hasil/quality_analysis/
```

### Hasil yang Diharapkan
```
Laporan disimpan:
- hasil/quality_analysis/quality_report_TIMESTAMP.json
- hasil/quality_analysis/results_hybrid_TIMESTAMP.csv

Ringkasan:
- Total: 20 kalimat
- Success rate: 100%
- Avg quality: 65.42%
- Avg semantic similarity: 0.88
- Avg processing time: 2.3s
```

---

## 6️⃣ Parameter Pengaturan Optimal

### Untuk Teks Pendek (< 100 kata)
```
- Metode: Hybrid
- Num variations: 3
- Min quality: 0.6
- Max length: 200
- Temperature: 1.0
```

### Untuk Teks Panjang (> 100 kata)
```
- Metode: Hybrid
- Chunking: Auto (2000 chars)
- Min quality: 0.65
- Temperature: 0.8
```

### Untuk Teks Akademik
```
- Metode: Rule-based atau Hybrid
- Min quality: 0.7
- Temperature: 0.7 (lebih konservatif)
- Preserve entities: True
```

### Untuk Variasi Kreatif
```
- Metode: Neural
- Temperature: 1.2-1.5
- Top-k sampling: 50
- Num variations: 5-10
```

---

## 7️⃣ Template Prompt untuk API/Programmatic

### Python Code Template
```python
from engines.indot5_hybrid_engine import IndoT5HybridParaphraser

# Initialize
paraphraser = IndoT5HybridParaphraser(
    model_name="Wikidepia/IndoT5-base",
    use_gpu=False,
    synonym_rate=0.3,
    min_confidence=0.7,
    quality_threshold=60.0
)

# Single paraphrase
result = paraphraser.paraphrase(
    text="Teks yang ingin diparafrase",
    method="hybrid"  # hybrid, neural, atau rule-based
)

print(f"Original: {result.original_text}")
print(f"Paraphrased: {result.paraphrased_text}")
print(f"Quality: {result.quality_score:.2f}%")
```

### Batch Processing Template
```python
# Multiple variations
results = paraphraser.generate_variations(
    text="Teks yang ingin diparafrase",
    num_variations=3,
    method="hybrid"
)

for i, result in enumerate(results, 1):
    print(f"Variasi {i}: {result.paraphrased_text}")
    print(f"Quality: {result.quality_score:.2f}%")
```

### File Upload Template
```python
from utils.file_parser import FileParser

# Parse file
parser = FileParser()
data = parser.process_file("path/to/document.pdf", chunk=True)

# Paraphrase chunks
for chunk in data['chunks']:
    result = paraphraser.paraphrase(chunk, method="hybrid")
    print(result.paraphrased_text)
```

---

## 8️⃣ Best Practices

### ✅ DO:
1. Gunakan **metode Hybrid** untuk hasil terbaik
2. Set **min_quality ≥ 60%** untuk output berkualitas
3. Gunakan **chunking otomatis** untuk dokumen > 2000 karakter
4. **Simpan hasil** dalam format JSON/CSV untuk analisis
5. **Bandingkan metode** untuk kasus tertentu

### ❌ DON'T:
1. Jangan gunakan **temperature > 1.5** (hasil tidak stabil)
2. Jangan set **num_variations > 10** (processing lambat)
3. Jangan parafrase **teks < 10 karakter** (tidak ada konteks)
4. Jangan harapkan **100% akurasi** dari neural method saja
5. Jangan lupakan **pengecekan kualitas output**

---

## 9️⃣ Contoh Use Cases Real

### Use Case 1: Parafrase Judul Penelitian
```
Input: "Analisis Pengaruh Media Sosial terhadap Perilaku Konsumen"

Prompt:
"Buat 3 variasi judul penelitian yang setara dengan:
'Analisis Pengaruh Media Sosial terhadap Perilaku Konsumen'

Pertahankan: tone akademik, makna inti
Metode: Hybrid"

Output:
1. Kajian Dampak Media Sosial pada Perilaku Konsumen
2. Studi Pengaruh Media Sosial terhadap Tingkah Laku Konsumen
3. Analisis Efek Media Sosial pada Perilaku Konsumsi
```

### Use Case 2: Parafrase Abstract Jurnal
```
Input: "Penelitian ini menggunakan metode kualitatif dengan pendekatan studi kasus. 
Data dikumpulkan melalui wawancara mendalam dan observasi partisipatif. 
Hasil penelitian menunjukkan bahwa faktor X berpengaruh signifikan terhadap Y."

Prompt:
"Parafrasakan abstract berikut dengan mempertahankan struktur 3 kalimat:
[TEKS]

Gunakan metode hybrid, kualitas min 70%, pertahankan istilah teknis."

Output:
"Riset ini menerapkan metode kualitatif melalui pendekatan studi kasus.
Pengumpulan data dilakukan dengan wawancara mendalam serta observasi partisipatif.
Temuan riset mengindikasikan bahwa faktor X memiliki pengaruh signifikan pada Y."
```

### Use Case 3: Parafrase Konten Website
```
Input: "Produk kami dirancang untuk memenuhi kebutuhan Anda. 
Dengan teknologi terkini dan desain modern, kami memberikan solusi terbaik."

Prompt:
"Buat 5 variasi copy website untuk:
[TEKS]

Pertahankan: tone marketing, call-to-action implisit
Metode: Hybrid dengan temperature 1.2 untuk kreativitas"

Output:
1. Produk kami diciptakan khusus untuk kebutuhan Anda...
2. Kami menghadirkan produk dengan teknologi terdepan...
3. Solusi terbaik hadir dengan desain modern kami...
4. Kebutuhan Anda adalah prioritas produk kami...
5. Teknologi canggih dan desain kontemporer untuk Anda...
```

---

## 🔟 Troubleshooting Prompts

### Masalah: Output Tidak Berubah
```
Solusi Prompt:
"Reset cache dan generate ulang dengan variasi parameter:
- Clear cache terlebih dahulu
- Gunakan temperature berbeda (1.2, 1.5)
- Gunakan metode berbeda untuk setiap variasi"
```

### Masalah: Kualitas Rendah (< 50%)
```
Solusi Prompt:
"Tingkatkan kualitas dengan:
- Metode: Hybrid (bukan neural saja)
- Min quality threshold: 0.7
- Gunakan rule-based jika neural gagal
- Perkaya sinonim database"
```

### Masalah: Makna Berubah
```
Solusi Prompt:
"Pertahankan makna dengan:
- Metode: Rule-based (lebih aman)
- Temperature: 0.7 (lebih konservatif)
- Semantic similarity threshold: 0.85+
- Review output secara manual"
```

---

## 📊 Metrics untuk Evaluasi

### Quality Score (0-100%)
- **90-100%**: Excellent - hampir sempurna
- **75-89%**: Good - berkualitas tinggi
- **60-74%**: Acceptable - cukup baik
- **< 60%**: Poor - perlu perbaikan

### Semantic Similarity (0-1.0)
- **0.90-1.0**: Sangat mirip makna
- **0.80-0.89**: Mirip dengan variasi
- **0.70-0.79**: Cukup berbeda
- **< 0.70**: Terlalu berbeda

### Lexical Diversity (0-1.0)
- **0.70-1.0**: Sangat bervariasi
- **0.50-0.69**: Cukup bervariasi
- **0.30-0.49**: Sedikit variasi
- **< 0.30**: Hampir tidak ada variasi

---

## 📁 Output Files Structure

Hasil parafrase akan disimpan dengan struktur:

```
hasil/
├── experiments/           # Hasil per-experiment
│   └── experiment_TIMESTAMP.json
├── batch_results/        # Hasil batch processing
│   └── batch_hybrid_TIMESTAMP.json
├── quality_analysis/     # Laporan analisis kualitas
│   ├── quality_report_TIMESTAMP.json
│   └── results_hybrid_TIMESTAMP.csv
├── comparison_reports/   # Perbandingan metode
│   └── comparison_TIMESTAMP.json
└── screenshots/          # Screenshot untuk dokumentasi
```

---

## 🎓 Advanced Tips

### Tip 1: Custom Synonym Database
Tambahkan sinonim spesifik domain Anda di `data/sinonim_extended.json`

### Tip 2: Custom Transformation Rules
Edit rules di `data/transformation_rules.json` untuk transformasi khusus

### Tip 3: Batch Processing Optimization
Untuk dokumen besar (>100 halaman), gunakan chunking 1500-2000 karakter

### Tip 4: API Integration
Integrasikan dengan REST API di `http://localhost:5000/paraphrase`

### Tip 5: Multi-Language Support
Untuk teks campuran EN-ID, proses per-kalimat dengan deteksi bahasa

---

## 📞 Referensi

- **Dokumentasi Lengkap**: [README.md](README.md)
- **API Documentation**: `http://localhost:5000/health`
- **Example Scripts**: `examples/indot5_hybrid_example.py`
- **Test Suite**: `tests/test_indot5_hybrid.py`

---

**Terakhir Diupdate**: 14 Januari 2026
**Versi**: 1.0.0
**Penulis**: IndoT5 Hybrid Paraphraser Team
