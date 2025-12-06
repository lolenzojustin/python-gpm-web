import requests
import json

url = "https://api.gologin.com/browser/v2"

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OTExZWI4OTY1MDVmNjI4N2M5YTkzZjUiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2OTExZWJjNmVkM2E0MGUwMWYzYzc4MjEifQ.F-f6GDM91ZljGhg1z8Q8mmz2JtE731Q8FPjwH5KYyAI',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers)
print(response.json()["profiles"][0]["id"])
idprofile1 = response.json()["profiles"][0]["id"]
# import requests
# import json

url = "http://localhost:36912/browser/start-profile"

payload = json.dumps({
  "profileId": idprofile1,
  "sync": True
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json()["wsUrl"])

