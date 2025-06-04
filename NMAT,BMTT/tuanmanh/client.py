import socket
import hashlib
import os
import sys

def calculate_sha256(data):
    return hashlib.sha256(data).hexdigest()

def send_file(file_path):
    host = '127.0.0.1'
    port = 5001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        file_name = os.path.basename(file_path)
        s.send(file_name.encode())

        with open(file_path, 'rb') as f:
            data = f.read()
            s.sendall(data)

        # Gửi dấu kết thúc file
        s.sendall(b'__END_FILE__')

        # Gửi SHA-256
        sha256 = calculate_sha256(data)
        s.send(sha256.encode())

        print(f"[CLIENT] Đã gửi '{file_name}' và SHA256.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Cách dùng: python client.py <file_path>")
    else:
        send_file(sys.argv[1])
