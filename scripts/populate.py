import requests

user_data = {'email': "foobarcom",
             'password': "foo",
             'firstName': "",
             'lastName': " ",
             'twitter': "http://",
             'flickr': "http://",
             'instagram': "http://",
             'role': 6
            }

r = requests.post('http://127.0.0.1:5000/api/user', data = user_data)

print(r.status_code)

if r.status_code != 200:
    # This means something went wrong.
    raise Exception(r.status_code)

print("Request was succesful!")
print("Got the following:")
for item in r.json():
    print(item)


# r = requests.get('http://127.0.0.1:5000/api/user')

# if r.status_code != 200:
#     # This means something went wrong.
#     raise Exception(r.status_code)

# print("Request was succesful!")
# print("Got the following:")
# for item in r.json():
#     print(item)