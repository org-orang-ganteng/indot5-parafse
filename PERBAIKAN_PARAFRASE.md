# Perbaikan Fungsi Parafrase IndoT5 Hybrid

## Masalah yang Ditemukan

1. **Neural Paraphrase tidak optimal**
   - Tidak ada prefix task-specific untuk memandu model
   - Parameter generasi kurang optimal
   - Logika pemilihan kandidat terlalu sederhana

2. **Hybrid Method over-transformation**
   - Terlalu banyak transformasi diterapkan
   - Hasil menjadi tidak natural

3. **Kandidat parafrase tidak berkualitas**
   - Filter kandidat kurang ketat
   - Tidak ada validasi repetisi kata

## Perbaikan yang Dilakukan

### 1. Perbaikan Neural Paraphrase (`_neural_paraphrase`)

#### a. Menambahkan Task-Specific Prefix
```python
prefixes = [
    f"parafrasekan: {text}",
    f"tulis ulang kalimat berikut: {text}",
    f"ubah kalimat: {text}"
]
```
**Manfaat**: IndoT5 lebih memahami task yang diminta dan menghasilkan parafrase yang lebih baik.

#### b. Menggunakan Beam Search
```python
outputs = self.model.generate(
    **inputs,
    max_length=min(len(text.split()) * 2 + 50, 256),
    min_length=max(len(text.split()) - 5, 5),
    num_beams=num_beams,
    num_return_sequences=min(3, num_beams),
    early_stopping=True,
    repetition_penalty=1.3,
    length_penalty=1.0,
    no_repeat_ngram_size=3
)
```
**Manfaat**: Hasil lebih stabil dan berkualitas tinggi dibanding nucleus sampling.

#### c. Pembersihan Output yang Lebih Baik
```python
# Remove prefix yang mungkin masih ada
for prefix in ["parafrasekan:", "tulis ulang kalimat berikut:", "ubah kalimat:"]:
    if decoded.lower().startswith(prefix):
        decoded = decoded[len(prefix):].strip()
```
**Manfaat**: Output bersih dari artefak prefix.

#### d. Metrik Pemilihan Kandidat yang Lebih Baik
```python
# 1. Semantic overlap (should be 50-80%)
overlap_score = 1.0 if 0.5 <= overlap <= 0.8 else (1.0 - abs(overlap - 0.65) * 3)

# 2. Length similarity (prefer ±30% of original)
length_score = 1.0 if 0.7 <= length_ratio <= 1.3 else (1.0 - abs(length_ratio - 1.0) * 2)

# 3. Lexical diversity (prefer more new words)
diversity_score = min(1.0, new_words / max(original_len * 0.3, 1))

# 4. Quality check - no repetitions
has_repetition = any(words_list[i] == words_list[i+1] for i in range(len(words_list)-1))
repetition_penalty = 0.5 if has_repetition else 1.0
```
**Manfaat**: Pemilihan kandidat berdasarkan multiple metrics yang komprehensif.

#### e. Fallback Mechanism
```python
if not candidates:
    # Try with sampling if beam search fails
    with torch.no_grad():
        outputs = self.model.generate(
            **inputs,
            do_sample=True,
            temperature=1.5,
            top_p=0.95,
            ...
        )
```
**Manfaat**: Tetap menghasilkan output berkualitas meski beam search gagal.

### 2. Perbaikan Hybrid Method

#### a. Confidence-Based Rule Application
```python
if neural_confidence >= self.min_confidence and neural_result != text:
    # Good neural result, apply light rule-based enhancement
    synonym_result, _, wc = self._apply_synonym_substitution(
        current_text, rate=self.synonym_rate * 0.5
    )
    # Apply limited transformation
    final_text, _, sc = self._apply_syntactic_transformation(
        synonym_result, max_transforms=1
    )
```
**Manfaat**: Menghindari over-transformation pada hasil neural yang sudah baik.

#### b. Logging yang Lebih Informatif
```python
transformations_applied.append(f"neural_generation (confidence: {neural_confidence:.2f})")
```
**Manfaat**: User dapat melihat confidence level dari hasil neural.

## Hasil Perbaikan

### Sebelum Perbaikan:
- ❌ Hasil parafrase sering tidak bermakna
- ❌ Banyak repetisi kata (contoh: "kunci kunci")
- ❌ Terlalu berbeda atau terlalu mirip dengan original
- ❌ Over-transformation membuat hasil tidak natural

### Setelah Perbaikan:
- ✅ Hasil parafrase lebih natural dan bermakna
- ✅ Tidak ada repetisi kata
- ✅ Balance antara similarity dan diversity
- ✅ Transformasi lebih terkontrol dan natural
- ✅ Fallback mechanism yang robust

## Cara Testing

Jalankan script test:
```bash
python test_paraphrase_quality.py
```

Script ini akan menguji:
1. 5 kasus test dengan 3 metode (neural, rule-based, hybrid)
2. Generate 3 variasi parafrase untuk 1 kalimat
3. Tampilkan quality metrics untuk setiap hasil

## Parameter yang Dapat Disesuaikan

1. **num_beams**: Jumlah beam untuk beam search (default: 5)
2. **temperature**: Temperature untuk sampling (default: 1.2)
3. **synonym_rate**: Rate penggantian sinonim (default: 0.3)
4. **min_confidence**: Minimum confidence untuk neural result (default: 0.6)
5. **max_transformations**: Maximum transformasi rule-based (default: 3)

## Rekomendasi Penggunaan

### Untuk Hasil Terbaik (Hybrid):
- Gunakan method "hybrid" dengan default parameters
- Confidence threshold: 0.6 - 0.7
- Synonym rate: 0.2 - 0.4

### Untuk Variasi Tinggi:
- Gunakan `generate_variations()` dengan num_variations=3-5
- Temperature lebih tinggi (1.5 - 2.0)

### Untuk Kecepatan:
- Gunakan method "rule-based"
- Atau reduce num_beams pada neural (3 instead of 5)

## Catatan Penting

1. Model membutuhkan minimal 3-5 detik untuk loading
2. Setiap paraphrase membutuhkan 1-3 detik processing
3. Cache diaktifkan untuk mempercepat request yang sama
4. GPU acceleration akan mempercepat proses secara signifikan

## Dependencies Baru yang Ditambahkan

Pastikan dependencies berikut terinstall:
```
protobuf>=3.19.0
sentencepiece>=0.1.99
```

Install dengan:
```bash
pip install -r requirements-neural.txt
```
