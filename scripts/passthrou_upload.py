import os
import requests
from requests.exceptions import HTTPError

def send_request(meth, url, data, headers=None, files=None, print_prep=True):
    # Print raw request
    # https://stackoverflow.com/a/23816211
    prepped = requests.Request(meth, url, data=data, headers=headers, files=files).prepare()
    if print_prep:
        print("*****************")
        print(prepped)
        print("*****************")
    s = requests.Session()
    resp = s.send(prepped)
    return resp

data_dir = "./dummy_data/"
file_name = "profile.jpg"
full_path = os.path.join(data_dir, file_name)

print("WILL TRY TO POST THE FILE")
url = 'http://127.0.0.1:5000/api/media/2?resource-kind=user'
# f = {'files': open(full_path, 'rb')}
f = [('images', (file_name, open(full_path, 'rb'), 'image/jpg'))]
resp = requests.post(url, files=f)

if resp.status_code != 200:
    # This means something went wrong.
    raise Exception(resp.status_code)

print("Request was succesful!")
print("Got the following:")
print(resp)
json = resp.json()
print(json)
for item in json:
    print(item, json[item])
