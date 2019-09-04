import requests

use_local_server = False

if use_local_server:
    # Local server
    url = 'http://127.0.0.1:5000'
else:
    # Staging server
    url = 'https://server-oasis.herokuapp.com/'

r = requests.get(url + '/api/user/')

if r.status_code != 200:
    # This means something went wrong.
    raise Exception(r.status_code)

print("Request was succesful!")
print("Got the following:")
json = r.json()
users = r.json()['users']
for user in users:    
    print(user)