#!/usr/bin/env python3
"""
IndoT5 Hybrid Paraphraser Web Application
Startup script for the web interface
"""

import os
import sys
import subprocess
import importlib.util
import socket
import signal

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'torch',
        'transformers',
        'sentence_transformers',
        'numpy',
        'sklearn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Beberapa dependency belum terinstall:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Silakan install dependency terlebih dahulu:")
        print("   pip install -r requirements-neural.txt")
        print("\n   Atau install Flask saja jika yang lain sudah ada:")
        print("   pip install flask")
        return False
    
    return True

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'data/sinonim_extended.json',
        'data/transformation_rules.json',
        'data/stopwords_id.txt'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Beberapa file data tidak ditemukan:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n💡 Pastikan file data tersedia sebelum menjalankan aplikasi")
        return False
    
    return True

def is_port_available(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        sock.close()
        return True
    except OSError:
        return False

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return None

def kill_process_on_port(port):
    """Kill process using the specified port"""
    try:
        # Use lsof to find the process
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"   🔸 Menghentikan proses PID {pid} yang menggunakan port {port}")
                except ProcessLookupError:
                    pass
            import time
            time.sleep(1)
            return True
        return False
    except Exception as e:
        print(f"   ⚠️  Gagal menghentikan proses: {e}")
        return False

def main():
    """Main function to start the web application"""
    print("🚀 IndoT5 Hybrid Paraphraser Web Application")
    print("=" * 50)
    
    # Check current directory
    if not os.path.exists('app.py'):
        print("❌ File app.py tidak ditemukan!")
        print("💡 Pastikan Anda menjalankan script ini dari direktori project")
        sys.exit(1)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check data files
    print("📄 Checking data files...")
    if not check_data_files():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("\n🌐 Starting web server...")
    
    # Check and handle port availability
    default_port = 5000
    port = default_port
    
    if not is_port_available(default_port):
        print(f"⚠️  Port {default_port} sedang digunakan")
        print("🔄 Mencoba menghentikan proses yang menggunakan port tersebut...")
        
        if kill_process_on_port(default_port):
            if is_port_available(default_port):
                print(f"✅ Port {default_port} sekarang tersedia")
            else:
                print(f"⚠️  Port {default_port} masih tidak tersedia, mencari port lain...")
                port = find_available_port(default_port + 1)
                if port:
                    print(f"✅ Menggunakan port alternatif: {port}")
                else:
                    print("❌ Tidak dapat menemukan port yang tersedia")
                    sys.exit(1)
        else:
            print(f"⚠️  Gagal menghentikan proses, mencari port lain...")
            port = find_available_port(default_port + 1)
            if port:
                print(f"✅ Menggunakan port alternatif: {port}")
            else:
                print("❌ Tidak dapat menemukan port yang tersedia")
                sys.exit(1)
    
    print(f"📍 Server akan berjalan di: http://localhost:{port}")
    print("⏹️  Tekan Ctrl+C untuk menghentikan server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app, initialize_paraphraser
        
        print("🔧 Initializing IndoT5 Hybrid Paraphraser...")
        initialize_paraphraser()
        
        print("✅ Paraphraser initialized successfully!")
        print("🌐 Web server is starting...")
        print("")
        print(f"📱 Buka browser dan akses: http://localhost:{port}")
        print("🎯 Atau klik link di atas untuk mengakses interface")
        print("")
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Server dihentikan oleh user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error menjalankan server: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Pastikan semua dependency terinstall")
        print("   2. Pastikan file data tersedia")
        print("   3. Coba jalankan ulang script ini")
        print(f"   4. Atau coba port manual: python app.py")
        sys.exit(1)

if __name__ == '__main__':
    main() 
