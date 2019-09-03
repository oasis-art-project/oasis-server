import requests
import json
import os

def make_data_request(data):
    request = {"request": json.dumps(data)}
    return request

def auth_header(token):
    return {
        'Authorization': 'Bearer {}'.format(token)
    }

use_local_server = True

if use_local_server:
    # Local server
    url = 'http://127.0.0.1:5000'
else:
    # Staging server
    url = 'https://server-oasis.herokuapp.com/'

# Need to login as admin to delete users
print("Logging in as admin")
d = make_data_request({'email': 'admin@oasis.com', 'password': 'adminOasis'})
r = requests.post(url + '/api/login/', data=d)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)
host_token = r.json()['token']
h = auth_header(host_token)

# Deleting all events
r = requests.get(url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    eid = event['id']

    d = {"id": eid}
    r = requests.delete(url + '/api/event/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted event", event['name'])

# Deleting all artworks
r = requests.get(url + '/api/artwork/')
if r.status_code != 200:
    raise Exception(r.status_code)
artworks = r.json()['artworks']
for artwork in artworks:
    aid = artwork['id']

    d = {"id": aid}
    r = requests.delete(url + '/api/artwork/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted artwork", artwork['name'])

# Deleting all places
r = requests.get(url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    pid = place['id']

    d = {"id": pid}
    r = requests.delete(url + '/api/place/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted place", place['name'])

# Deleting all users
r = requests.get(url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    uid = user['id']
    role = user['role']
    if role == 1: continue
    
    d = {"id": uid}
    r = requests.delete(url + '/api/user/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted user", user['firstName'], user['lastName'])

# Logout
r = requests.delete(url + '/api/login/', headers=h)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)    
       
print("Admin logged out succesfully")