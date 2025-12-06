import requests

# url = "127.0.0.1:57609/json/version"
# 127.0.0.1:55662
# "http://127.0.0.1:57609/json/version"
url = "127.0.0.1:57609/json/version"
payload = {}
headers = {}

# Vừa call api vừa trả kết quả trả về đặt tên là response luôn
response = requests.request("GET", url, headers=headers, data=payload) 

print(response.text)


