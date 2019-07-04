import requests

resp = requests.get('http://127.0.0.1:5000/api/user')

if resp.status_code != 200:
    # This means something went wrong.
    raise Exception(resp.status_code)

print("Request was succesful!")
print("Got the following:")
for item in resp.json():
    print(item)