import requests
import json
import mimetypes
import os
from os.path import join, abspath
import jwt

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
        "lastName": "AAA",
        "phone": "6172720341",
        "homepage": "www.google.com",
        "instagram": "juanperez",
        "youtube": "",
        "role": 3,
        "showChat": True,
        "bio": "Cool person",
        "tags": "art",
        "confirmed": True
    }

server_url = 'http://127.0.0.1:5000'

email = 'narria01@icloud.com'
passw = '==09~killed~TEXAS~house~96=='
path = './scripts/new_data/def_images/'
fn = 'profile.png'

mimetypes.init()

user_data = make_data_request({'email': email, 'password': passw})
r = requests.post(server_url + '/api/login/', data=user_data)
if r.status_code != 200:
  raise Exception(r.status_code, r.content)
host_token = r.json()['token']
host_header = auth_header(host_token)
print("Logged in succesfully")

raw_user_data = make_data_request(user_json())
new_user_data = make_data_request(raw_user_data)
r = requests.put(server_url + '/api/user/', data=new_user_data, headers=host_header)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)

print("Updated user succesfully")

r = requests.delete(server_url + '/api/login/', headers=host_header)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)
print("Logged out succesfully")

# Updating user profile image
r = requests.post(server_url + '/api/login/', data=user_data)
if r.status_code != 200:
  raise Exception(r.status_code, r.content)
host_token = r.json()['token']
host_header = auth_header(host_token)
print("Logged in succesfully")

decoded_token = jwt.decode(host_token, verify=False)
rid = decoded_token['identity']
rkind = "user"

full_path = abspath(join(path, fn))
mtype = mimetypes.guess_type(full_path)[0]
image_files = [('images', (fn, open(full_path, 'rb'), mtype))]
r = requests.post(server_url + '/api/media/'+ str(rid) + '?resource-kind=' + rkind, files=image_files, headers=host_header)
if r.status_code != 200:
    raise Exception(r.status_code)
j = r.json()
for item in j:
    if item == "images":
        imgs = json.loads(j[item])
        for fn in imgs:
            print("  Uploaded image:", fn, "=>", imgs[fn]["url"])

r = requests.delete(server_url + '/api/login/', headers=host_header)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)            
print("Logged out succesfully")