# from Ui_UI import Ui_MainWindow
import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
from random import randint
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import urllib.request, json
import requests
import threading
import os
import sys
import random
import string
import re
import datetime
import shutil
import uiautomator2 as uc
from adbutils import adb

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 822)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setObjectName("startBtn")
        self.verticalLayout.addWidget(self.startBtn)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name device"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Email"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Mật khẩu"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Tháng Sinh Nhật"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Trạng thái"))
        self.startBtn.setText(_translate("MainWindow", "Bắt Đầu"))


class MultiThread(QThread):
    record = pyqtSignal(object, object, object, object, object, object)
    def __init__(self, index, namedevice, acc_information):
        super().__init__()
        self.index = index
        self.namedevice = namedevice
        self.acc_information = acc_information
    
    def run(self):
        device = uc.connect(self.namedevice)
        self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Sẵn sàng")
        self.CreateAcc(device)
        self.Logout()
    
    def CreateAcc(self, device):
        try:
            device.app_start("com.instagram.android")
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Mở App Instagram")
            try:
                device.xpath('//*[@text="Create new account"]').click()
            except:
                device.xpath('//*[@text="Get started"]').click()
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Create New Account")
            device.xpath('//*[@text="Sign up with email"]').click()
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Sign Up with Email")
            device.xpath('//*[@text="Email"]').click()
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Get Temp Mail")
            url = "https://api.tempmail.lol/v2/inbox/create"

            payload = json.dumps({
            "domain": None,
            "captcha": None
            })
            headers = {
            'sec-ch-ua-platform': '"Windows"',
            'Referer': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?0'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            email = response.json()["address"]
            token = response.json()["token"]
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Nhập Email")
            device.send_keys(email)
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Next")
            device.xpath('//*[@text="Next"]').click()
            # request để lấy code và nhập vào
            isNotGetCode = True
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Bắt đầu Get Code Mail")
            while(isNotGetCode):
                url = "https://api.tempmail.lol/v2/inbox?token="+token

                payload = {}
                headers = {
                'sec-ch-ua-platform': '"Windows"',
                'Referer': '',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'sec-ch-ua-mobile': '?0'
                }

                response = requests.request("GET", url, headers=headers, data=payload)
                if response.status_code == 200:
                    result = response.json()
                    emails = result.get("emails", [])
                    
                    if emails and len(emails) > 0:
                        # Get the latest email
                        latest_email = emails[0]
                        email_body = latest_email.get("body", "")
                        email_subject = latest_email.get("subject", "")
                        
                        print(f"📧 Found email - Subject: {email_subject}")
                        
                        # Extract 6-digit code from email body
                        pattern = r"\d{6}"
                        codes = re.findall(pattern, email_body)
                        # ["948943", "434589"]
                        if codes:
                            verification_code = codes[0]
                            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Nhập code Mail")
                            device.send_keys(verification_code)
                            isNotGetCode = False
                time.sleep(1)
            countCheckCreatePass = 0
            isTaoLoi = False
            while(countCheckCreatePass < 10):
                if device(text="Create a password").exists:
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Nhập Password")
                    device.send_keys("Zxcv123123.")
                    device.xpath('//*[@text="Next"]').click()
                    countCheckCreatePass = 10
                else:
                    countCheckCreatePass += 1
                    if countCheckCreatePass == 10:
                        isTaoLoi = True
                time.sleep(1)
            try:
                self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Nhập Not Now")
                device.xpath('//*[@text="Not now"]').click(timeout=5)
            except:
                print("Không")
                self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Button 1")
            device.xpath('//*[@resource-id="android:id/button1"]').click()
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Next")
            device.xpath('//*[@text="Next"]').click()
            time.sleep(0.5)
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Next")
            device.xpath('//*[@text="Next"]').click()
            countCheckOldYou = 0
            while(countCheckOldYou < 10):
                if device(text='How old are you?').exists:
                    countCheckOldYou = 10
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Nhập Birthday")
                    device.send_keys("20")
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Next")
                    device.xpath('//*[@text="Next"]').click()
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Button 2")
                    device.xpath('//*[@resource-id="android:id/button2"]').click()
                else:
                    countCheckOldYou += 1
                    if countCheckOldYou == 10:
                        isTaoLoi = True
                time.sleep(1)
            countCheckYourName = 0
            while(countCheckYourName < 10):
                if device(text="What's your name?").exists:
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Nhập Name")
                    device.send_keys("Hoang Linh")
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Next")
                    device.xpath('//*[@text="Next"]').click()
                    countCheckYourName = 10
                else:
                    countCheckYourName += 1
                    if countCheckYourName == 10:
                        isTaoLoi = True
                time.sleep(1)

            countCheckCreateUserName = 0
            while(countCheckCreateUserName < 10):
                if device(text='Create a username').exists:
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Create Username")
                    device.xpath('//*[@text="Next"]').click()
                    self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Click Agree")
                    device.xpath('//*[@text="I agree"]').click()
                    countCheckCreateUserName = 10
                else:
                    countCheckCreateUserName += 1
                    if countCheckCreateUserName == 10:
                        isTaoLoi = True
                time.sleep(1)    

            if isTaoLoi == True:
                self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Tạo lỗi")
                print("Lỗi")
            else:
                self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Tạo thành công")
                print("Tạo thành công")
        except:
            self.record.emit(self.index, self.namedevice, self.acc_information["email"], self.acc_information["password"], self.acc_information["month_birthday"], "Tạo lỗi")
            print("Lỗi")
    
    def Logout(self):
        print("Log out")
    
    def stop(self):
        self.terminate()

class Manager(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.threads = []
        self.startBtn.clicked.connect(self.startThread)

    def startThread(self):
        # email = self.line_edit.text()
        email = "demotestapi"
        url = f"http://127.0.0.1:8000/create-mail/{email}"

        payload = {}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.json())
        # device_list = []
        # acc_information_list = [
        #     {
        #         "email": "vavooasivc1@gmail.com",
        #         "password": "12341234",
        #         "month_birthday": "Dec"
        #     },
        #     {
        #         "email": "vavooasivc2@gmail.com",
        #         "password": "12341234",
        #         "month_birthday": "Jan"
        #     },
        #     {
        #         "email": "vavooasivc3@gmail.com",
        #         "password": "12341234",
        #         "month_birthday": "Feb"
        #     },{
        #         "email": "vavooasivc4@gmail.com",
        #         "password": "12341234",
        #         "month_birthday": "May"
        #     }
        # ]
        # for d in adb.device_list():
        #     print(d.serial) # print device serial
        #     device_list.append(d.serial)
        # self.tableWidget.setRowCount(len(device_list))
        # for i in range(0, len(device_list)):
        #     thread = MultiThread(index=i,namedevice=device_list[i],acc_information=acc_information_list[i]) # khởi tạo 1 thread với Data Type là class MultiThread
        #     thread.record.connect(self.write_data) # chỉ là lệnh để connect tới UI để update thông tin lên UI
        #     self.threads.append(thread) # Thêm thread mới tạo vào trong mảng threads tổng để quản lý 
        #     thread.start() # Bắt đầu chạy thread vừa tạo.
        #     time.sleep(2)

    def stopThread(self):
        for i in range(0, len(self.threads)):
            self.threads[i].stop()
        self.threads = []

    def write_data(self, i, device, email, password, month_birthday, status):
        self.tableWidget.setItem(i, 0, QTableWidgetItem(str(device)))
        self.tableWidget.setItem(i, 1, QTableWidgetItem(str(email)))
        self.tableWidget.setItem(i, 2, QTableWidgetItem(str(password)))
        self.tableWidget.setItem(i, 3, QTableWidgetItem(str(month_birthday)))
        self.tableWidget.setItem(i, 4, QTableWidgetItem(str(status)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Manager()
    window.show()
    sys.exit(app.exec_())