import socket
import os
import sys
from utils import sha256_checksum

file_path = sys.argv[1]
file_name = os.path.basename(file_path)
file_size = os.path.getsize(file_path)
hash_val = sha256_checksum(file_path)

client = socket.socket()
client.connect(('localhost', 9001))

client.send(file_name.encode())
client.recv(1024)
client.send(str(file_size).encode())
client.recv(1024)
client.send(hash_val.encode())
client.recv(1024)

with open(file_path, 'rb') as f:
    while True:
        bytes_read = f.read(4096)
        if not bytes_read:
            break
        client.sendall(bytes_read)

client.close()
print("📤 Đã gửi file thành công.")
