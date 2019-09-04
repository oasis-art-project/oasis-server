import requests
import json
import os
import csv

def make_data_request(data):
    request = {"request": json.dumps(data)}
    return request

def auth_header(token):
    return {
        'Authorization': 'Bearer {}'.format(token)
    }

def delete_image(rid, rkind, fn, user):
    # The user that owns the images needs to login
    d = make_data_request({'email': user['email'], 'password': user['password']})
    r = requests.post(url + '/api/login/', data=d)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    h = auth_header(host_token)

    r = requests.delete(url + '/api/media/' + str(rid) + '?resource-kind=' + rkind + '&file-name=' + fn, headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code)
    print("  deleted", fn)
         
    r = requests.delete(url + '/api/login/', headers=h)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content) 

use_local_server = False

if use_local_server:
    # Local server
    url = 'http://127.0.0.1:5000'
else:
    # Staging server
    url = 'https://server-oasis.herokuapp.com/'

adminFullName = 'Admin Oasis'
data_dir = "./dummy_data/"

# Need to get the email and password from the csv, the server will not return this information :-)
in_csv = os.path.join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_dict = {}
for row in reader:
    email = row[0]
    password = row[1]
    user_dict[row[2] + ' ' + row[3]] = {'email': email, 'password':password}

r = requests.get(url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']

for user in users:
    fullName = user['firstName'] + ' ' + user['lastName']
    if fullName == adminFullName: continue
    extra = user_dict[fullName]
    user['email'] = extra['email']
    user['password'] = extra['password']
    user_dict[fullName] = user
    uid = user['id']
    role = user['role']
    if role == 1: continue
    print("Images for user", user['firstName'], user["lastName"])
    r = requests.get(url + '/api/media/' + str(uid) +'?resource-kind=user')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json() 
    for img in j["images"]: 
        delete_image(uid, "user", os.path.split(img)[1], user)

r = requests.get(url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    pid = place['id']
    host = place['host']
    user = user_dict[host['firstName'] + ' ' + host['lastName']]
    print("Images for place", place['name'])
    r = requests.get(url + '/api/media/' + str(pid) +'?resource-kind=place')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for img in j["images"]:
        delete_image(pid, "place", os.path.split(img)[1], user)

r = requests.get(url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    eid = event['id']
    host = event['place']['host']
    user = user_dict[host['firstName'] + ' ' + host['lastName']]    
    print("Images for event", event['name'])
    r = requests.get(url + '/api/media/' + str(eid) +'?resource-kind=event')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json() 
    for img in j["images"]: 
        delete_image(eid, "event", os.path.split(img)[1], user)