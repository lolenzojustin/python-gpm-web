import ipaddress
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor
import tls_client

class DeviceScanner(QThread):
    finished = pyqtSignal(list)

    def __init__(self, iphost):
        super().__init__()
        self.network = ipaddress.ip_network(f"{iphost}.0/24", strict=False)
        self.iphost = iphost
        self.ipaddress = []

    def getDataIP(self):
        # ⚠️ Thay dải mạng theo router nhà bạn (ví dụ: 192.168.1.0/24 hoặc 192.168.0.0/24)
    
        print("🔍 Đang quét mạng WiFi...")
        alive_hosts = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            for result in executor.map(self.ping, self.network.hosts()):
                if result:
                    alive_hosts.append(result)
        print("\n📡 Danh sách IP online:")
        print(alive_hosts)
        self.ipaddress = alive_hosts
        

    def ping(self, ip):
        ip_str = str(ip)
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "200", ip_str],   # Windows
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return ip_str
        return None

    def run(self):
        self.getDataIP()
        devices = []
        for i in self.ipaddress:
            try:
                session = tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True)
                url = f"http://{i}:8080"
                response = session.get(url, timeout_seconds=3)
                print(response.text)
                if f'd.autotouch.net' in response.text:
                    devices.append(f"{i}")
            except:
                pass
        self.finished.emit(devices)