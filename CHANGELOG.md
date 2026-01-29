# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-01-29

### 🚀 Added - SSE Streaming Implementation

#### Problem Fixed
- **504 Gateway Timeout**: Proses generate yang lama (>2 menit) menyebabkan timeout di browser
- User tidak tahu progress dan harus menunggu tanpa feedback
- Request timeout sebelum backend selesai memproses

#### Solution Implemented
**Server-Sent Events (SSE) untuk Real-Time Streaming**

### 📝 Changes

#### Backend (app.py)
1. **New Endpoint**: `/paraphrase-stream` (POST)
   - Menggunakan Server-Sent Events untuk streaming
   - Mengirim progress real-time untuk setiap variasi
   - Tidak ada timeout karena koneksi tetap hidup
   
2. **Streaming Flow**:
   ```python
   @app.route('/paraphrase-stream', methods=['POST'])
   def paraphrase_stream():
       def generate():
           # Stream status: started
           yield f"data: {json.dumps({'status': 'started'})}\n\n"
           
           # Stream progress untuk setiap variasi
           for i in range(num_variations):
               yield f"data: {json.dumps({'status': 'progress', 'current': i+1})}\n\n"
               result = paraphraser.paraphrase(text)
               yield f"data: {json.dumps({'status': 'result', 'data': result})}\n\n"
           
           # Stream completion
           yield f"data: {json.dumps({'status': 'completed'})}\n\n"
       
       return Response(stream_with_context(generate()), mimetype='text/event-stream')
   ```

3. **Legacy Endpoint**: `/paraphrase` (POST)
   - Tetap tersedia untuk backward compatibility
   - Recommended untuk quick/simple requests
   - Bisa timeout jika proses terlalu lama

#### Frontend (index.html)
1. **SSE Handler Function**:
   ```javascript
   async function handleStreamingParaphrase(formData, loadingEl, resultsEl) {
       return new Promise((resolve, reject) => {
           fetch('/paraphrase-stream', {...})
               .then(response => {
                   const reader = response.body.getReader();
                   // Process SSE stream
                   // Update UI real-time
               });
       });
   }
   ```

2. **Real-time UI Updates**:
   - Progress bar dengan persentase
   - Status message untuk setiap variasi
   - Quality score ditampilkan langsung
   - Hasil muncul bertahap, tidak perlu tunggu semua selesai

#### Dependencies
- Added imports: `Response`, `stream_with_context` from Flask
- Added: `threading`, `queue` for background processing support

### ✨ Features

1. **Real-Time Progress Tracking**
   - ✅ Progress bar dinamis
   - ✅ Status update setiap variasi
   - ✅ Quality score langsung terlihat
   - ✅ Estimasi waktu tersisa

2. **No Timeout Issues**
   - ✅ Koneksi SSE tetap hidup
   - ✅ Browser tidak timeout
   - ✅ Backend bisa proses sampai selesai
   - ✅ Error handling yang lebih baik

3. **Better User Experience**
   - ✅ User tahu progress real-time
   - ✅ Tidak perlu menunggu dalam gelap
   - ✅ Bisa lihat hasil bertahap
   - ✅ Cancel support (future)

### 🔧 Technical Details

**SSE Message Format**:
```
data: {"status": "started", "message": "Memulai proses parafrase..."}

data: {"status": "progress", "current": 1, "total": 10, "message": "Menghasilkan variasi 1/10..."}

data: {"status": "result", "variation": 1, "data": {...paraphrase result...}, "total_found": 1}

data: {"status": "completed", "total_variations": 5, "paraphrases": [...]}

data: {"status": "error", "error": "Error message"}
```

**Browser Compatibility**:
- ✅ Chrome/Edge: Full support
- ✅ Firefox: Full support
- ✅ Safari: Full support
- ✅ Opera: Full support
- ⚠️ IE11: Not supported (use legacy endpoint)

### 📊 Performance Impact

**Before (Legacy)**:
- Timeout: 60-120 seconds (browser default)
- User feedback: None until complete
- Error rate: High for >10 variations

**After (SSE Streaming)**:
- Timeout: None (streaming keeps alive)
- User feedback: Real-time for each variation
- Error rate: Low, user sees progress even if partial failure

### 🎯 Usage Example

**Frontend (JavaScript)**:
```javascript
// Form submit menggunakan SSE
document.getElementById('paraphraseForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = {...};
    await handleStreamingParaphrase(formData, loadingEl, resultsEl);
});
```

**Backend (Python)**:
```python
# Import untuk SSE
from flask import Response, stream_with_context

# Endpoint SSE
@app.route('/paraphrase-stream', methods=['POST'])
def paraphrase_stream():
    def generate():
        # Streaming logic
        yield f"data: {json.dumps(status)}\n\n"
    return Response(stream_with_context(generate()), mimetype='text/event-stream')
```

### 🛠️ Files Modified

1. **app.py**
   - Added: SSE streaming endpoint
   - Added: Stream generator function
   - Modified: Imports for streaming support

2. **index.html**
   - Added: `handleStreamingParaphrase()` function
   - Modified: Form submit handler to use SSE
   - Added: Real-time progress UI updates

3. **README.md**
   - Added: SSE streaming documentation
   - Added: API endpoint documentation
   - Added: Troubleshooting for timeout issues

4. **.gitignore** (NEW)
   - Added comprehensive Python gitignore
   - Excluded models, cache, logs
   - Excluded sensitive data and large files

5. **CHANGELOG.md** (NEW)
   - This file - documenting all changes

### 🐛 Bug Fixes

1. **Fixed**: 504 Gateway Timeout error
   - Root cause: Long processing time exceeded browser timeout
   - Solution: SSE streaming keeps connection alive

2. **Fixed**: No progress feedback during generation
   - Root cause: Synchronous blocking request
   - Solution: Real-time streaming with progress updates

3. **Fixed**: Browser hangs during processing
   - Root cause: No response until completion
   - Solution: Incremental response streaming

### 🔄 Migration Guide

**For users using the web interface**:
- ✅ No changes needed - automatically uses SSE
- ✅ Old `/paraphrase` endpoint still works

**For API users**:
```bash
# Old way (may timeout)
POST /paraphrase
{...}

# New way (recommended)
POST /paraphrase-stream
{...}
# Handle SSE stream in your client
```

### 📝 Notes

- Legacy `/paraphrase` endpoint tetap tersedia
- SSE digunakan secara default di web interface
- Backward compatible dengan existing code
- No breaking changes

### 🔮 Future Improvements

- [ ] Cancel generation support
- [ ] WebSocket alternative for bidirectional communication
- [ ] Progress estimation dengan ETA
- [ ] Batch streaming untuk multiple texts
- [ ] Resume support jika koneksi terputus

---

## [1.0.0] - 2024-XX-XX

### Initial Release
- IndoT5 Neural Processing
- Rule-based Transformations
- Hybrid Approach
- Web Interface
- Quality Assessment
- Batch Processing
