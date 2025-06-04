import os
from tkinter import *
from tkinter import filedialog, messagebox
from Crypto.Cipher import DES

# Hàm thêm padding
def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

# Mã hóa file
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    padded_text = pad(plaintext.decode('utf-8'))
    encrypted_text = cipher.encrypt(padded_text.encode('utf-8'))
    output_file = file_path + '.enc'
    with open(output_file, 'wb') as f:
        f.write(encrypted_text)
    return output_file

# Giải mã file
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        encrypted_text = f.read()
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    decrypted_text = cipher.decrypt(encrypted_text).decode('utf-8').rstrip(' ')
    output_file = file_path + '.dec.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    return output_file

# Giao diện chính
class DESApp:
    def __init__(self, master):
        self.master = master
        master.title("DES File Encrypt/Decrypt")
        master.geometry("500x300")

        self.file_path = ""
        self.output_file = ""

        self.label = Label(master, text="Chọn file:")
        self.label.pack()

        self.browse_button = Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.key_label = Label(master, text="Nhập khóa (8 ký tự):")
        self.key_label.pack()

        self.key_entry = Entry(master, width=30, show="*")
        self.key_entry.pack()

        self.encrypt_button = Button(master, text="Mã hóa", command=self.encrypt)
        self.encrypt_button.pack()

        self.decrypt_button = Button(master, text="Giải mã", command=self.decrypt)
        self.decrypt_button.pack()

        self.download_button = Button(master, text="Download kết quả", command=self.download_file)
        self.download_button.pack()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        messagebox.showinfo("Thông báo", f"Đã chọn file: {self.file_path}")

    def encrypt(self):
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Lỗi", "Khóa phải có đúng 8 ký tự!")
            return
        if not self.file_path:
            messagebox.showerror("Lỗi", "Chưa chọn file!")
            return
        self.output_file = encrypt_file(self.file_path, key)
        messagebox.showinfo("Thành công", f"Đã mã hóa: {self.output_file}")

    def decrypt(self):
        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror("Lỗi", "Khóa phải có đúng 8 ký tự!")
            return
        if not self.file_path:
            messagebox.showerror("Lỗi", "Chưa chọn file!")
            return
        self.output_file = decrypt_file(self.file_path, key)
        messagebox.showinfo("Thành công", f"Đã giải mã: {self.output_file}")

    def download_file(self):
        if self.output_file and os.path.exists(self.output_file):
            save_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if save_path:
                with open(self.output_file, 'rb') as f_in, open(save_path, 'wb') as f_out:
                    f_out.write(f_in.read())
                messagebox.showinfo("Thành công", f"Đã lưu file tại: {save_path}")
        else:
            messagebox.showerror("Lỗi", "Không có file kết quả để tải!")

# Khởi chạy
if __name__ == "__main__":
    root = Tk()
    app = DESApp(root)
    root.mainloop()
