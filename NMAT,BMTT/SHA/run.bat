@echo off
cd /d "%~dp0"

echo 🚀 Khởi động Socket Server...
start cmd /k python server.py

timeout /t 3

echo 🚀 Khởi động Flask Web App...
start cmd /k python app.py

timeout /t 5

echo 🌐 Mở trình duyệt web tại http://localhost:5000
start http://localhost:5000
