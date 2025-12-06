import requests

BASE_URL = "http://127.0.0.1:18439"  # nếu bạn đổi port thì sửa lại
CREATE_URL = f"{BASE_URL}/api/v3/profiles/create"

# Nếu bản GPM của bạn yêu cầu API key thì dùng header Authorization,
# còn không cần thì bỏ dòng đó đi.
API_KEY = "YOUR_API_KEY"  # thay bằng key nếu có, không có thì có thể bỏ hẳn biến này

# headers = {
#     "Content-Type": "application/json",
#     # "Authorization": f"Bearer {API_KEY}",  # cần thì mở comment
# }

payload = {
    "profile_name": "Reg acc sep",
    "group_name": "All",
    "browser_core": "chromium",
    "browser_name": "Chrome",
    "browser_version": "139.0.7258.139",
    "is_random_browser_version": False,
    "raw_proxy": "",               # IP:Port:User:Pass hoặc tm://API_KEY|True,False ...
    "startup_urls": "",            # "https://google.com,https://facebook.com"
    "is_masked_font": True,
    "is_noise_canvas": False,
    "is_noise_webgl": False,
    "is_noise_client_rect": False,
    "is_noise_audio_context": True,
    "is_random_screen": False,
    "is_masked_webgl_data": True,
    "is_masked_media_device": True,
    "is_random_os": False,
    "os": "Windows 11",
    "webrtc_mode": 2,              # 1: Off, 2: Base on IP
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/139.0.0.0 Safari/537.36"
}

response = requests.post(CREATE_URL, json=payload, timeout=30)

print("Status:", response.status_code)
print("Raw response:", response.text)

# Nếu muốn lấy id profile:
try:
    data = response.json()
    if data.get("success"):
        print("Tạo thành công, profile_id:", data["data"]["id"])
    else:
        print("Tạo thất bại, message:", data.get("message"))
except Exception as e:
    print("Lỗi parse JSON:", e)
