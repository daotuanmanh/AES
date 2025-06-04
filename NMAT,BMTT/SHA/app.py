from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Gọi client.py để gửi file
    subprocess.run(['python', 'client.py', filepath])
    return '✅ File đã được gửi thành công!'

if __name__ == '__main__':
    app.run(debug=True)
