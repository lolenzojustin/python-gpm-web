import sys
import json
import requests
import threading
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont


# ============================
# FASTAPI SERVER
# ============================

demo = FastAPI()

class Data(BaseModel):
    mail: str
    password: str
    dateofbirth: str


@demo.post("/create-mail/{email}")
def create_mail(email: str):
    url = "https://api.internal.temp-mail.io/api/v3/email/new"

    payload = json.dumps({
        "name": email,
        "domain": "bltiwd.com"
    })

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://temp-mail.io',
        'referer': 'https://temp-mail.io/',
        'user-agent': 'Mozilla/5.0'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()


# ============================
# THREAD_1: chạy FastAPI
# ============================

def start_fastapi_thread():
    print("➡️ Thread_1 (API) đang chạy...")
    uvicorn.run(demo, host="127.0.0.1", port=8000)



# ============================
# PYQT5 UI
# ============================

API_URL = "http://127.0.0.1:8000/create-mail/"

class MainUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tool Create Mail API - PyQt5")
        self.setGeometry(500, 200, 500, 400)

        layout = QVBoxLayout()

        label = QLabel("Nhập Email:")
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)

        self.email_input = QLineEdit()
        self.email_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.email_input)

        btn = QPushButton("TẠO MAIL")
        btn.setFont(QFont("Arial", 12))
        btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        btn.clicked.connect(self.call_create_mail)
        layout.addWidget(btn)

        result_label = QLabel("Kết quả API:")
        result_label.setFont(QFont("Arial", 12))
        layout.addWidget(result_label)

        self.result_box = QTextEdit()
        self.result_box.setFont(QFont("Arial", 10))
        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def call_create_mail(self):
        email = self.email_input.text().strip()

        if email == "":
            QMessageBox.critical(self, "Lỗi", "Vui lòng nhập email!")
            return

        # try–except 1: DÙNG ĐỂ GHI EMAIL VÀO FILE, NẾU FILE BỊ KHÓA / KHÔNG GHI ĐƯỢC THÌ BÁO LỖI
        try:
            with open("sample.txt", "a", encoding="utf-8") as f:
                f.write(email + "\n")
        except Exception as e:
            # Nếu có lỗi khi ghi file, hiển thị popup
            QMessageBox.critical(self, "Lỗi File", f"Không ghi được status.txt\n{str(e)}")

        # try–except 2: DÙNG ĐỂ GỌI API, NẾU API LỖI / MẤT MẠNG / TIMEOUT THÌ BÁO LỖI
        try:
            response = requests.post(API_URL + email)

            if response.status_code != 200:
                QMessageBox.critical(self, "Lỗi API", f"Status: {response.status_code}")
                return

            data = response.json()
            self.result_box.setText(json.dumps(data, indent=4, ensure_ascii=False))

        except Exception as e:
            # Nếu có lỗi khi gọi API → hiển thị popup lỗi
            QMessageBox.critical(self, "Lỗi", str(e))



# ============================
# CHẠY ỨNG DỤNG
# ============================

if __name__ == "__main__":

    # --------------------------------
    # 🚀 Thread_1: Chạy FastAPI server
    # --------------------------------
    #  APi sẽ được tạo trên http://127.0.0.1:8000 ngay sau khi khởi động tool
    Thread_1 = threading.Thread(target=start_fastapi_thread, daemon=True)
    Thread_1.start()

    # --------------------------------
    # 🎨 Thread_2: Chạy UI PyQt5
    # --------------------------------
    print("➡️ Thread_2 (UI) đang chạy...")

    Thread_2 = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(Thread_2.exec_())
