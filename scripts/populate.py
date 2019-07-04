import requests
import json
import os

def params(request, num_files=0):
    """
    Prepares request

    :param request: string request
    :param num_files: how many files to send simultaneously (0-2)
    :return: processed json
    """
    parameters = {"request": json.dumps(request)}

    # Prepare files for sending
    if num_files > 0:
        if num_files == 1:
            files = ("profile1.jpg", )
        elif num_files == 2:
            files = ("profile1.jpg", "profile2.jpg")
        else:
            raise ValueError("Can be only 1 or 2")

        # Read files from the disk, open into File instances...
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = {"files": [open(os.path.join(dir_path, file), 'rb') for file in files]}

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
p = params(data, 1)
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
