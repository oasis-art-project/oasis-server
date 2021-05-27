import requests
import json

def make_data_request(data):
    request = {"request": json.dumps(data)}
    return request

def auth_header(token):
    return {
        'Authorization': 'Bearer {}'.format(token)
    }

def user_json():
    return {
        "firstName": "Juan",
        "lastName": "Perez",
        "phone": "6172720341",
        "homepage": "www.google.com",
        "instagram": "juanperez",
        "youtube": "",
        "role": 2,
        "showChat": True,
        "bio": "Cool person",
        "tags": "art",
        "confirmed": True
    }

server_url = 'http://127.0.0.1:5000'

email = 'narria01@icloud.com'
passw = '==09~killed~TEXAS~house~96=='

user_data = make_data_request({'email': email, 'password': passw})
r = requests.post(server_url + '/api/login/', data=user_data)
if r.status_code != 200:
  raise Exception(r.status_code, r.content)
host_token = r.json()['token']
host_header = auth_header(host_token)

new_user_data = user_data = make_data_request(user_json())
r = requests.put(server_url + '/api/user/', data=new_user_data, headers=host_header)

if r.status_code != 200:
    raise Exception(r.status_code, r.content)

r = requests.delete(server_url + '/api/login/', headers=host_header)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)            
print("  Logged out succesfully")
