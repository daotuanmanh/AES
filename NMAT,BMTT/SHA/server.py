import socket
import hashlib
import os
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RECEIVED_FOLDER = 'received'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RECEIVED_FOLDER, exist_ok=True)

# Gửi file và hash tới server thông qua socket
def receive_file():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 5001))
    server_socket.listen(1)
    print("Server socket listening on port 5001...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected with {addr}")

        # Nhận tên file
        file_name = client_socket.recv(1024).decode()
        file_path = os.path.join(RECEIVED_FOLDER, file_name)

        # Nhận nội dung file
        file_data = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            file_data += chunk

        # Nhận SHA-256 hash cuối cùng
        sha256_sent = client_socket.recv(64).decode()

        # Lưu file
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Tính lại SHA-256
        sha256_hash = hashlib.sha256(file_data).hexdigest()
        if sha256_hash == sha256_sent:
            print(f"[OK] File '{file_name}' được nhận toàn vẹn.")
        else:
            print(f"[ERROR] File '{file_name}' bị lỗi, không toàn vẹn.")

        client_socket.close()

# Flask Web API
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', files=os.listdir(RECEIVED_FOLDER))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        return 'Upload thành công!'
    return 'Không có file!'

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(RECEIVED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    import threading
    t = threading.Thread(target=receive_file)
    t.start()
    app.run(debug=True, port=5000)
