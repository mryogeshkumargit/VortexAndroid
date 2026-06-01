#!/usr/bin/env python3
"""
File Transfer Server - Fixed Version
- Cross-platform path handling (no more "uploadsCustomer" errors)
- Modern path handling with pathlib
- cgi deprecation warning suppressed
"""

import http.server
import socketserver
import os
import socket
from pathlib import Path
import qrcode
import threading
import urllib.parse
import json
import warnings

# Suppress cgi deprecation warning (safe until Python 3.13)
warnings.filterwarnings("ignore", category=DeprecationWarning)

PORT = 8000
API_PORT = 8001
APK_FILE = "app-debug.apk"
API_FOLDER = "CustomAPIs"
UPLOAD_FOLDER = "uploads"
SHARE_FOLDER = ""


class APKHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_web_ui().encode())

        elif self.path == "/api/files":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            files = self.list_files()
            self.wfile.write(json.dumps(files).encode())

        elif self.path.startswith("/download/"):
            self.serve_download()

        elif self.path == "/latest.apk":
            self.serve_apk()

        else:
            super().do_GET()

    def serve_download(self):
        try:
            raw_path = self.path[10:]
            filepath = urllib.parse.unquote(raw_path)
            filepath = filepath.replace('\\', os.sep).replace('/', os.sep)
            filepath = os.path.normpath(filepath)

            print(f"[DEBUG] Download request: {filepath}")

            if os.path.exists(filepath) and os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                filename = os.path.basename(filepath)

                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.send_header('Content-Length', str(file_size))
                self.end_headers()

                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
                print(f"[OK] Served file: {filepath}")
            else:
                print(f"[404] File not found: {filepath}")
                self.send_error(404, "File not found")
        except Exception as e:
            print(f"[ERROR] Download failed: {e}")
            self.send_error(500, str(e))

    def serve_apk(self):
        apk_paths = [
            APK_FILE,
            f"app/build/outputs/apk/debug/{APK_FILE}",
            f"New Make/{APK_FILE}"
        ]
        apk_file = next((p for p in apk_paths if os.path.exists(p)), None)

        if apk_file:
            try:
                file_size = os.path.getsize(apk_file)
                self.send_response(200)
                self.send_header('Content-Type', 'application/vnd.android.package-archive')
                self.send_header('Content-Length', str(file_size))
                self.send_header('Content-Disposition', f'attachment; filename="{APK_FILE}"')
                self.end_headers()
                with open(apk_file, 'rb') as f:
                    self.wfile.write(f.read())
                print(f"[OK] Served APK: {apk_file}")
            except Exception as e:
                self.send_error(500, f"Error serving APK: {e}")
        else:
            self.send_error(404, "APK file not found")

    def do_POST(self):
        if self.path == "/upload":
            self.handle_upload()
        else:
            self.send_error(404)

    def handle_upload(self):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        content_type = self.headers.get('Content-Type', '')

        if 'multipart/form-data' not in content_type:
            self.send_error(400, "Invalid content type")
            return

        try:
            import cgi
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST'})
            fileitem = form['file']

            if fileitem.filename:
                safe_name = os.path.basename(fileitem.filename)
                filepath = os.path.join(UPLOAD_FOLDER, safe_name)

                with open(filepath, 'wb') as f:
                    f.write(fileitem.file.read())

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'filename': safe_name,
                    'path': filepath.replace('\\', '/')
                }).encode())
                print(f"[UPLOAD] Saved: {filepath}")
            else:
                self.send_error(400, "No file uploaded")
        except Exception as e:
            print(f"[UPLOAD ERROR] {e}")
            self.send_error(500, str(e))

    def list_files(self):
        files = []

        # Uploads folder
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                p = Path(UPLOAD_FOLDER) / filename
                if p.is_file():
                    try:
                        size = p.stat().st_size
                        files.append({
                            'path': p.as_posix(),      # Always forward slashes
                            'name': f"📤 {filename}",
                            'size': size
                        })
                    except Exception:
                        pass

        # Share folder (optional)
        if SHARE_FOLDER and os.path.exists(SHARE_FOLDER):
            for filename in os.listdir(SHARE_FOLDER):
                p = Path(SHARE_FOLDER) / filename
                if p.is_file():
                    try:
                        size = p.stat().st_size
                        files.append({
                            'path': p.as_posix(),
                            'name': f"📁 {filename}",
                            'size': size
                        })
                    except Exception:
                        pass

        return files

    def get_web_ui(self):
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Transfer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        .card { background: white; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); padding: 30px; margin-bottom: 20px; }
        h1 { color: #333; margin-bottom: 10px; font-size: 28px; text-align: center; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-size: 14px; }
        .section-title { color: #667eea; font-size: 18px; margin-bottom: 15px; font-weight: 600; }
        .upload-area { border: 3px dashed #667eea; border-radius: 12px; padding: 50px 20px; text-align: center; background: #f8f9ff; cursor: pointer; transition: all 0.3s; }
        .upload-area:hover { border-color: #764ba2; background: #f0f2ff; transform: scale(1.02); }
        .upload-area.dragover { border-color: #764ba2; background: #e8ebff; transform: scale(1.05); }
        .upload-icon { font-size: 48px; margin-bottom: 10px; }
        .upload-text { color: #667eea; font-size: 16px; font-weight: 500; }
        .upload-hint { color: #999; font-size: 13px; margin-top: 8px; }
        input[type="file"] { display: none; }
        .file-list { list-style: none; max-height: 400px; overflow-y: auto; }
        .file-item { padding: 15px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; gap: 12px; transition: background 0.2s; }
        .file-item:hover { background: #f8f9ff; }
        .file-item:last-child { border-bottom: none; }
        .file-icon { font-size: 24px; }
        .file-info { flex: 1; }
        .file-name { color: #333; font-weight: 500; display: block; margin-bottom: 4px; word-break: break-word; }
        .file-size { color: #999; font-size: 13px; }
        .download-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 500; transition: transform 0.2s; }
        .download-btn:hover { transform: scale(1.05); }
        .refresh-btn { background: white; color: #667eea; border: 2px solid #667eea; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 500; width: 100%; margin-bottom: 15px; transition: all 0.2s; }
        .refresh-btn:hover { background: #667eea; color: white; }
        .status { padding: 15px; border-radius: 8px; margin-top: 15px; display: none; font-weight: 500; }
        .status.success { background: #d4edda; color: #155724; display: block; }
        .status.error { background: #f8d7da; color: #721c24; display: block; }
        .loading { text-align: center; padding: 30px; color: #999; }
        .empty-state { text-align: center; padding: 40px 20px; color: #999; }
        .empty-icon { font-size: 48px; margin-bottom: 10px; opacity: 0.5; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>📱 File Transfer</h1>
            <p class="subtitle">Transfer files between devices on the same network</p>
            
            <div class="section-title">📤 Send Files to Computer</div>
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">☁️</div>
                <div class="upload-text">Tap or Drop Files Here</div>
                <div class="upload-hint">Select files from your device</div>
                <input type="file" id="fileInput" multiple>
            </div>
            <div class="status" id="uploadStatus"></div>
        </div>
        
        <div class="card">
            <div class="section-title">📥 Receive Files from Computer</div>
            <button class="refresh-btn" onclick="loadFiles()">🔄 Refresh Files</button>
            <div class="loading" id="loading">Loading...</div>
            <ul class="file-list" id="fileList"></ul>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const uploadStatus = document.getElementById('uploadStatus');
        const fileList = document.getElementById('fileList');
        const loading = document.getElementById('loading');
        
        uploadArea.onclick = () => fileInput.click();
        uploadArea.ondragover = (e) => { e.preventDefault(); uploadArea.classList.add('dragover'); };
        uploadArea.ondragleave = () => uploadArea.classList.remove('dragover');
        uploadArea.ondrop = (e) => { e.preventDefault(); uploadArea.classList.remove('dragover'); handleFiles(e.dataTransfer.files); };
        fileInput.onchange = (e) => handleFiles(e.target.files);
        
        function handleFiles(files) {
            Array.from(files).forEach(file => uploadFile(file));
        }
        
        function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            showStatus('⏳ Uploading ' + file.name + '...', 'success');
            
            fetch('/upload', { method: 'POST', body: formData })
                .then(r => r.json())
                .then(data => {
                    showStatus('✅ Uploaded: ' + data.filename, 'success');
                    loadFiles();
                })
                .catch(() => showStatus('❌ Upload failed', 'error'));
        }
        
        function showStatus(msg, type) {
            uploadStatus.textContent = msg;
            uploadStatus.className = 'status ' + type;
            setTimeout(() => uploadStatus.style.display = 'none', 3000);
        }
        
        function loadFiles() {
            loading.style.display = 'block';
            fileList.innerHTML = '';
            fetch('/api/files')
                .then(r => r.json())
                .then(files => {
                    loading.style.display = 'none';
                    if (files.length === 0) {
                        fileList.innerHTML = '<div class="empty-state"><div class="empty-icon">📂</div><div>No files available</div></div>';
                    } else {
                        fileList.innerHTML = files.map(f => `
                            <li class="file-item">
                                <div class="file-icon">${f.name.startsWith('📤') ? '📤' : '📁'}</div>
                                <div class="file-info">
                                    <span class="file-name">${f.name.replace('📤 ', '').replace('📁 ', '')}</span>
                                    <span class="file-size">${formatSize(f.size)}</span>
                                </div>
                                <button class="download-btn" onclick="downloadFile('${f.path}')">⬇️ Get</button>
                            </li>
                        `).join('');
                    }
                })
                .catch(() => { loading.style.display = 'none'; fileList.innerHTML = '<div class="empty-state">❌ Error loading files</div>'; });
        }
        
        function downloadFile(path) {
            window.location.href = '/download/' + encodeURIComponent(path);
        }
        
        function formatSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / 1048576).toFixed(1) + ' MB';
        }
        
        loadFiles();
    </script>
</body>
</html>'''


class JSONHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=API_FOLDER, **kwargs)

    def do_GET(self):
        if self.path == '/list':
            self.send_list_response()
        else:
            super().do_GET()

    def send_list_response(self):
        try:
            json_files = []
            if os.path.exists(API_FOLDER):
                json_files = [f for f in os.listdir(API_FOLDER) if f.endswith('.json')]
            response = {"files": json_files}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self.send_error(500, f"Error listing files: {str(e)}")

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def main():
    print(f"Starting File Transfer Server on port {PORT}")
    print(f"Looking for APK: {APK_FILE}")

    apk_paths = [APK_FILE, f"app/build/outputs/apk/debug/{APK_FILE}", f"New Make/{APK_FILE}"]
    found_apk = next((p for p in apk_paths if os.path.exists(p)), None)

    if found_apk:
        size = os.path.getsize(found_apk)
        print(f"Found APK: {found_apk} ({size} bytes)")
    else:
        print("Warning: APK file not found.")

    local_ip = get_local_ip()
    web_url = f"http://{local_ip}:{PORT}"
    apk_url = f"http://{local_ip}:{PORT}/latest.apk"

    print(f"\n{'='*50}")
    print(f"Web UI: {web_url}")
    print(f"APK Download: {apk_url}")
    print(f"{'='*50}")

    qr = qrcode.QRCode()
    qr.add_data(web_url)
    qr.print_ascii(invert=True)

    print(f"\nScan QR code or visit: {web_url}")

    api_url = f"http://{local_ip}:{API_PORT}"
    print(f"\n{'='*50}")
    print(f"JSON API server: {api_url}")
    print(f"{'='*50}")

    qr_api = qrcode.QRCode()
    qr_api.add_data(api_url)
    qr_api.print_ascii(invert=True)

    print(f"\nScan QR code or visit: {api_url}")
    print(f"Serving JSON files from: {API_FOLDER}" if os.path.exists(API_FOLDER) else f"Warning: {API_FOLDER} not found")
    print("Press Ctrl+C to stop\n")

    try:
        api_server = socketserver.TCPServer(("", API_PORT), JSONHandler)
        api_thread = threading.Thread(target=api_server.serve_forever, daemon=True)
        api_thread.start()

        with socketserver.TCPServer(("", PORT), APKHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        api_server.shutdown()


if __name__ == "__main__":
    main()