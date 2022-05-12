import requests
import json
import os
import argparse

def make_data_request(data):
    request = {"request": json.dumps(data)}
    return request

def auth_header(token):
    return {
        'Authorization': 'Bearer {}'.format(token)
    }

def try_post(path, data=None, files=None, headers=None):
    count = 0
    while count < 3:
        try:
            r = requests.post(path, data=data, files=files, headers=headers)
            return r
        except:
            time.sleep(10 ** (count + 1)) 
            count += 1 

parser = argparse.ArgumentParser(description='Deletes all data in the DB.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
parser.add_argument('-e', '--email', action='store', default='admin@oasis.com', help='admin email')
parser.add_argument('-p', '--password', action='store', default='adminOasis', help='admin password')

args = parser.parse_args()

server_url = args.url
admin_email = args.email
admin_passowrd = args.password

# Need to login as admin to delete users
print("Logging in as admin")
d = make_data_request({'email': admin_email, 'password': admin_passowrd})
# r = requests.post(server_url + '/api/login/', data=d)
r = try_post(server_url + '/api/login/', data=d)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)
host_token = r.json()['token']
h = auth_header(host_token)

# Deleting all events
r = requests.get(server_url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    eid = event['id']

    d = {"id": eid}
    r = requests.delete(server_url + '/api/event/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted event", event['name'])

# Deleting all artworks
r = requests.get(server_url + '/api/artwork/')
if r.status_code != 200:
    raise Exception(r.status_code)
artworks = r.json()['artworks']
for artwork in artworks:
    aid = artwork['id']

    d = {"id": aid}
    r = requests.delete(server_url + '/api/artwork/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted artwork", artwork['name'])

# Deleting all places
r = requests.get(server_url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    pid = place['id']

    d = {"id": pid}
    r = requests.delete(server_url + '/api/place/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted place", place['name'])

# Deleting all users
r = requests.get(server_url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    uid = user['id']
    role = user['role']
    if role == 1: continue
    
    d = {"id": uid}
    r = requests.delete(server_url + '/api/user/', data=d, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    print("  Deleted user", user['firstName'], user['lastName'])

# Logout
r = requests.delete(server_url + '/api/login/', headers=h)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)    
       
print("Admin logged out succesfully")