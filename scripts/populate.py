import requests

user_data = {"email": "vincent@oasis.art",
             "password": "art",
             "firstName": "Vincent",
             "lastName": "Van Gogh",
             "twitter": "laOrejaDeVanGogh",
             "flickr": "laNarizDeVanGogh",
             "instagram": "elOjoDeVanGogh",
             "role": 2
            }

r = requests.post('http://127.0.0.1:5000/api/user/', data = user_data)

print(r.status_code)

if r.status_code != 201:
    # This means something went wrong.
    raise Exception(r.status_code)

print("Request was succesful!")
print("Got the following:")
for item in r.json():
    print(item)
