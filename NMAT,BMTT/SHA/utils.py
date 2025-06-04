import hashlib

def sha256_checksum(file_path):
    """
    Tính toán mã băm SHA-256 cho một file.
    Trả về chuỗi hex (64 ký tự).
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()
