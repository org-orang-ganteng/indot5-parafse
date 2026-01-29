# 🚀 Quick Start Guide - SSE Streaming

## Masalah yang Diperbaiki

### ❌ Sebelumnya (Timeout Issue)
```
User Submit Form → Server process 2+ menit → Browser timeout 504 ❌
```
- Browser timeout setelah 60-120 detik
- Tidak ada feedback progress
- Backend sebenarnya berhasil, tapi browser sudah timeout

### ✅ Sekarang (SSE Streaming)
```
User Submit Form → Server stream progress → Browser terima real-time ✅
```
- Tidak ada timeout
- Progress bar real-time
- Quality score setiap variasi
- Hasil muncul bertahap

---

## 📝 Perubahan yang Ditambahkan

### 1. File Baru
- **`.gitignore`** - Untuk membatasi file yang di-push ke Git
- **`CHANGELOG.md`** - Dokumentasi semua perubahan
- **`QUICK_START_SSE.md`** - Guide ini

### 2. File yang Dimodifikasi

#### `app.py`
```python
# ➕ Added: Import untuk SSE
from flask import Response, stream_with_context

# ➕ Added: Endpoint SSE baru
@app.route('/paraphrase-stream', methods=['POST'])
def paraphrase_stream():
    """Handle paraphrasing dengan SSE streaming"""
    def generate():
        # Stream progress real-time
        yield f"data: {json.dumps({...})}\n\n"
    return Response(stream_with_context(generate()), 
                   mimetype='text/event-stream')

# ✓ Existing: Endpoint lama tetap ada
@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    # Legacy endpoint, still works
    ...
```

#### `index.html`
```javascript
// ➕ Added: Fungsi handler SSE
async function handleStreamingParaphrase(formData, loadingEl, resultsEl) {
    return new Promise((resolve, reject) => {
        fetch('/paraphrase-stream', {...})
            .then(response => {
                const reader = response.body.getReader();
                // Process SSE stream
                // Update UI real-time ✨
            });
    });
}

// ✏️ Modified: Form submit menggunakan SSE
document.getElementById('paraphraseForm').addEventListener('submit', async function(e) {
    // Automatically uses SSE streaming now
    await handleStreamingParaphrase(formData, loading, results);
});
```

#### `README.md`
- ➕ Dokumentasi SSE streaming
- ➕ API endpoint documentation
- ➕ Troubleshooting timeout issues
- ➕ Technical implementation details

---

## 🎯 Cara Menggunakan

### Web Interface (Automatic)
1. Jalankan aplikasi:
   ```bash
   python run_web_app.py
   ```

2. Buka browser: `http://localhost:5000`

3. Masukkan teks dan klik "Parafrase Teks"

4. ✨ **Otomatis menggunakan SSE!** Anda akan lihat:
   - Progress bar bergerak
   - Status setiap variasi
   - Quality score real-time
   - Hasil muncul bertahap

### API Usage (Manual)

#### Python Example
```python
import requests
import json

def paraphrase_with_sse(text, num_variations=5):
    url = 'http://localhost:5000/paraphrase-stream'
    data = {
        'text': text,
        'method': 'hybrid',
        'num_variations': num_variations,
        'min_quality': 70
    }
    
    response = requests.post(url, json=data, stream=True)
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = json.loads(line[6:])
                
                if data['status'] == 'progress':
                    print(f"Progress: {data['current']}/{data['total']}")
                elif data['status'] == 'result':
                    print(f"Found variation: {data['data']['quality_score']}")
                elif data['status'] == 'completed':
                    print(f"Done! Total: {data['total_variations']}")
                    return data['paraphrases']

# Usage
text = "Sistem parafrase bahasa Indonesia dengan teknologi AI"
results = paraphrase_with_sse(text, num_variations=10)
```

#### JavaScript Example
```javascript
async function paraphraseSSE(text, numVariations = 5) {
    const response = await fetch('/paraphrase-stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: text,
            method: 'hybrid',
            num_variations: numVariations,
            min_quality: 70
        })
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    const results = [];
    
    while (true) {
        const {done, value} = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                
                if (data.status === 'progress') {
                    console.log(`Progress: ${data.current}/${data.total}`);
                } else if (data.status === 'result') {
                    results.push(data.data);
                    console.log(`Quality: ${data.data.quality_score}`);
                } else if (data.status === 'completed') {
                    console.log('Completed!');
                    return data.paraphrases;
                }
            }
        }
    }
    
    return results;
}

// Usage
const text = "Sistem parafrase bahasa Indonesia dengan teknologi AI";
const results = await paraphraseSSE(text, 10);
```

---

## 📊 Perbandingan

| Fitur | Legacy (`/paraphrase`) | SSE (`/paraphrase-stream`) |
|-------|----------------------|---------------------------|
| **Timeout** | ❌ 60-120 detik | ✅ Tidak ada |
| **Progress** | ❌ Tidak ada | ✅ Real-time |
| **UI Feedback** | ❌ Loading tanpa info | ✅ Progress bar + status |
| **Quality Info** | ❌ Di akhir saja | ✅ Setiap variasi |
| **Error Handling** | ❌ Timeout diam-diam | ✅ Stream error message |
| **Cancel Support** | ❌ Tidak bisa | ✅ Bisa (future) |
| **Use Case** | Quick requests | Long processing |

---

## 🛠️ Troubleshooting

### Browser Tidak Menampilkan Progress
```bash
# Check browser console (F12)
# Pastikan tidak ada error JavaScript
# Verifikasi SSE endpoint aktif:
curl http://localhost:5000/health
```

### Server Error saat Streaming
```bash
# Check server logs
tail -f logs/indot5_hybrid.log

# Restart server
pkill -f "python app.py"
python app.py
```

### Progress Bar Tidak Update
- Clear browser cache (Ctrl+Shift+Del)
- Hard refresh (Ctrl+Shift+R)
- Check network tab (F12) untuk SSE connection

---

## 🔒 .gitignore - File yang Dibatasi

### File yang TIDAK akan di-push:
```
✅ Virtual environment (venv/, env/)
✅ Python cache (__pycache__/, *.pyc)
✅ Model files (*.pt, *.pth, models/)
✅ Log files (*.log, logs/)
✅ Sensitive data (.env, credentials.json)
✅ Large data files (*.csv, *.pdf di uploads/)
✅ IDE config (.vscode/, .idea/)
```

### File yang AKAN di-push:
```
✅ Source code (*.py, *.html, *.js)
✅ Configuration (config.py, *.json)
✅ Documentation (README.md, CHANGELOG.md)
✅ Requirements (requirements-neural.txt)
✅ Data samples (sinonim_extended.json, stopwords_id.txt)
```

### Before Git Push
```bash
# Check file yang akan di-push
git status

# Pastikan tidak ada file besar/sensitive
git add .
git status

# Push dengan aman
git commit -m "Add SSE streaming support"
git push origin main
```

---

## 🎉 Summary

### ✅ Yang Ditambahkan:
1. **SSE Streaming** - Tidak ada timeout lagi!
2. **Real-time Progress** - User tahu apa yang terjadi
3. **Better UX** - Progress bar, status, quality score
4. **Documentation** - README, CHANGELOG, Guide ini
5. **.gitignore** - Membatasi file yang di-push

### 📝 File Baru:
- `.gitignore` - Git ignore rules
- `CHANGELOG.md` - Change history
- `QUICK_START_SSE.md` - Guide ini

### 🔧 File Modified:
- `app.py` - Added SSE endpoint
- `index.html` - Added SSE handler
- `README.md` - Added SSE docs

### 🚀 Ready to Use:
```bash
python run_web_app.py
# Open http://localhost:5000
# Enjoy streaming paraphrase! 🎉
```

---

**Last Updated**: 2026-01-29  
**Version**: 1.1.0  
**Feature**: SSE Streaming Anti-Timeout
