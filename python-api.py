from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel, conlist
import requests
import json
demo = FastAPI()

@demo.get("/welcome")
def read_root():
    return {"Hello": "World"}

@demo.post("/helloworld")
def helloworld():
    return {"status": "success"}

@demo.post("/calculate/{a}")
def calculate(a: int):
    total = a + 3
    return {"result": total}

class Data(BaseModel):
    mail: str
    password: str
    dateofbirth: str

@demo.post("/upload-data")
def upload_data(data: Data):
    if not data.mail:
        print(data.mail)
    if not data.password:
        print(data.password)
    if not data.dateofbirth:
        print(data.dateofbirth)
    if data.mail == "" or data.password == "" or data.dateofbirth == "":
        return {"result": "Fail"}
    return {"result": "success"}

@demo.post("/create-mail/{email}")
def create_mail(email: str):
    url = "https://api.internal.temp-mail.io/api/v3/email/new"

    payload = json.dumps({
    "name": email,
    "domain": "bltiwd.com"
    })
    headers = {
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'application-name': 'web',
    'application-version': '4.0.0',
    'content-type': 'application/json',
    'origin': 'https://temp-mail.io',
    'priority': 'u=1, i',
    'referer': 'https://temp-mail.io/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-cors-header': 'iaWg3pchvFx48fY'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    return response.json()

@demo.post("/create-data")
def create_data(data: Data):
    if not data.mail:
        print(data.mail)
    if not data.password:
        print(data.password)
    if not data.dateofbirth:
        print(data.dateofbirth)
    if data.mail == "" or data.password == "" or data.dateofbirth == "":
        return {"result": "Fail"}
    with open("sample.txt", "a") as f:
        f.write(f"{data.mail}|{data.password}|{data.dateofbirth}")
    return {"result": "success",
            "mail": data.mail,
            "password": data.password,
            "dateofbirth": data.dateofbirth}