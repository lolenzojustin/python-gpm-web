import requests

BASE_URL = "http://127.0.0.1:18439"   # sửa theo port GPM của bạn
profile_id = "3e719d57-4e4d-4d1f-ac94-0a5ac3e20146"            # id profile cần xoá
mode = 2                              # 1: chỉ DB, 2: xoá cả folder

url = f"{BASE_URL}/api/v3/profiles/delete/{profile_id}?mode={mode}"

response = requests.get(url)
print(response.status_code)
print(response.text)
