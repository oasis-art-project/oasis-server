import requests
import json
import os

def params(request, filenames=None):
    parameters = {"request": json.dumps(request)}

    # Prepare files for sending
    if filenames:
        # Read files from the disk, open into File instances...
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = {"files": [open(os.path.join(dir_path, fn), 'rb') for fn in filenames]}

        # ... and save it in parameters json
        parameters.update(files)

    return parameters

def user_json():
    return {
        "email": "vincent@oasis.art",
        "password": "starrynight",
        "firstName": "Vincent",
        "lastName": "VanGogh",
        "twitter": "laOrejaDeVanGogh",
        "flickr": "laNarizDeVanGogh",
        "instagram": "elOjoDeVanGogh",
        "role": 2
    }

data = user_json()
p = params(data, ["./dummy_data/profile.jpg"])
print(p)

r = requests.post('http://127.0.0.1:5000/api/user/', data = p)

print(r.status_code)

if r.status_code != 201:
    # This means something went wrong.
    raise Exception(r.status_code)

print("Request was succesful!")
print("Got the following:")
for item in r.json():
    print(item)
