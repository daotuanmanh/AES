import os
from typing import Optional, cast
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import hashlib

app = Flask(__name__)
CORS(app)  # Cho phép frontend gọi API (cross-origin)

# Thư mục lưu file upload
UPLOAD_FOLDER: str = os.path.join(os.path.dirname(__file__), 'received_files')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dictionary lưu trữ filename và hash SHA256 tương ứng
received_files: dict[str, str] = {}

def sha256_checksum(filepath: str, block_size: int = 65536) -> str:
    """
    Tính toán mã băm SHA-256 cho file tại đường dẫn filepath.
    """
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

@app.route('/upload', methods=['POST'])
def upload() -> Response:
    """
    API nhận file upload qua POST, lưu file, tính SHA-256 và trả về hash đó.
    """
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    filename: Optional[str] = file.filename
    if not filename:
        return "No selected file", 400

    filename = cast(str, filename)  # giúp Pylance hiểu chắc chắn là str
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Lưu file vào thư mục upload
    file.save(filepath)

    # Tính hash SHA-256
    file_hash = sha256_checksum(filepath)
    received_files[filename] = file_hash

    # Trả về hash file (dạng plain text)
    return file_hash, 200

@app.route('/files', methods=['GET'])
def list_files() -> Response:
    """
    API trả về danh sách file đã upload kèm hash SHA-256.
    """
    return jsonify(received_files)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename: str) -> Response:
    """
    API download file theo filename.
    """
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    # Chạy server Flask trên mọi IP, port 5000
    app.run(host='0.0.0.0', port=5000)
