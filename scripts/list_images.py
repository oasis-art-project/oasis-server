import requests
import json
import os

use_local_server = False

if use_local_server:
    # Local server
    url = 'http://127.0.0.1:5000'
else:
    # Staging server
    url = 'https://server-oasis.herokuapp.com/'

r = requests.get(url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    uid = user['id']
    role = user['role']
    if role == 1: continue
    print("Images for user", user['firstName'], user["lastName"])
    r = requests.get(url + '/api/media/' + str(uid) +'?resource-kind=user')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json() 
    for img in j["images"]: 
        print("  ", img)

r = requests.get(url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    pid = place['id']
    print("Images for place", place['name'])
    r = requests.get(url + '/api/media/' + str(pid) +'?resource-kind=place')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for img in j["images"]: 
        print("  ", img)

r = requests.get(url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    eid = event['id']
    print("Images for event", event['name'])
    r = requests.get(url + '/api/media/' + str(eid) +'?resource-kind=event')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json() 
    for img in j["images"]: 
        print("  ", img)