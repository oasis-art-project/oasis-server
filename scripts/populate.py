import requests
import json
import os
import csv
import mimetypes
from os import listdir
from os.path import isfile, join

def make_data_request(data):
    request = {"request": json.dumps(data)}
    return request

def auth_header(token):
    return {
        'Authorization': 'Bearer {}'.format(token)
    }

def user_json(row):
    return {
        "email": row[0],
        "password": row[1],
        "firstName": row[2],
        "lastName": row[3],
        "twitter": row[4],
        "flickr": row[5],
        "instagram": row[6],
        "role": row[8],
        "bio": row[9]
    }

def host_json(id, user):
    return {
        # "id": int(id),
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "bio": user["bio"],        
        "twitter": user["twitter"],
        "flickr": user["flickr"],
        "instagram": user["instagram"],
    }

def place_json(row, host):
    return {
        "host": host,
        "name": row[1],
        "address": row[2],
        "description": row[3]
    }

def event_json(place, artists, name, desc, start, end):
    return {
        "place": place,
        "artists": artists,
        "name": name,
        "description": desc,
        "startTime": start,
        "endTime": end
    }

def upload_image(bdir, fn, rkind, rid):
    full_path = join(bdir, fn)
    mtype = mimetypes.guess_type(full_path)[0]
    if not mtype: return
    f = [('images', (fn, open(full_path, 'rb'), mtype))]
    r = requests.post(url + '/api/upload/' + str(rid) +'?resource-kind=' + rkind, files=f)
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for item in j:
        if item == "images":
            imgs = json.loads(j[item])
            for fn in imgs:
                print("  Uploaded image:", fn, "=>", imgs[fn]["url"])

def upload_images(bdir, rkind, rid):
    f = []
    all_files = [f for f in listdir(bdir) if isfile(join(bdir, f))]
    for fn in all_files:
        full_path = join(bdir, fn)
        mtype = mimetypes.guess_type(full_path)[0]
        if not mtype: continue
        f += [('images', (fn, open(full_path, 'rb'), mtype))]
    r = requests.post(url + '/api/upload/'+ str(rid) +'?resource-kind=' + rkind, files=f)
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for item in j:
        if item == "images":
            imgs = json.loads(j[item])
            for fn in imgs:
                print("  Uploaded image:", fn, "=>", imgs[fn]["url"])

use_local_server = True

load_users = True
load_places = True
load_events = Truee
load_artworks = False
load_images = True

if use_local_server:
    # Local server
    url = 'http://127.0.0.1:5000'
else:
    # Staging server
    url = 'https://server-oasis.herokuapp.com/'

adminFullName = 'Admin Oasis'
data_dir = "./dummy_data/"

mimetypes.init()

if load_users: print("Loading users...")
in_csv = os.path.join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_extra = {}
for row in reader:
    email = row[0]
    password = row[1]
    user_extra[row[2] + ' ' + row[3]] = {'email': email, 'password':password}
    if load_users and load_users:
        raw_user_data = user_json(row)

        print("Creating user", row[2], row[3], "...")
        d = make_data_request(raw_user_data)
        r = requests.post(url + '/api/user/', data=d)
        if r.status_code == 400:
            print("  Uer already exists")
            continue
        
        if r.status_code != 201:                
            raise Exception(r.status_code, r.content)

        uid = r.json()["id"]
        print("  Created user with id", uid)

# Retrieving all users
user_dict = {}
r = requests.get(url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    fullName = user['firstName'] + ' ' + user['lastName']
    if not fullName == adminFullName:
        user['email'] = user_extra[fullName]['email']
        user['password'] = user_extra[fullName]['password']
    user_dict[fullName] = user
    if load_users and load_images:
        uid = user['id']
        role = user['role']
        if role == 1: continue
        if role == 2:
            base_path = data_dir + "/images/users/hosts/" + user['email']
        elif role == 3:
            base_path = data_dir + "/images/users/artists/" + user['email']
        print("Uploading images for user", user["firstName"], user["lastName"])
        upload_images(base_path, "user", uid)

if load_places: 
    print("Loading places...")
    in_csv = os.path.join(data_dir, "place_list.csv")
    reader = csv.reader(open(in_csv, 'r'), dialect='excel')
    header = next(reader)
    for row in reader:
        print("Creating place", row[1], "...")
        print("  Logging user", row[0])

        user = user_dict[row[0]]

        # First the host user needs to login so we have the token to use in place creation
        d = make_data_request({'email': user['email'], 'password': user['password']})
        r = requests.post(url + '/api/login/', data=d)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        h = auth_header(host_token)

        raw_place_data = place_json(row, host_json(row[0], user))
        p = make_data_request(raw_place_data)
        r = requests.post(url + '/api/place/', data=p, headers=h)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        pid = r.json()["id"]
        print("  Created place with id", pid)

        # Logout
        r = requests.delete(url + '/api/login/', headers=h)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
        
        print("  Logged out succesfully")

# Retrieving all places
place_dict = {}
r = requests.get(url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    place_dict[place['name']] = place
    if load_places and load_images:
        pid = place['id']
        base_path = data_dir + "/images/places/" + place["name"]
        print("Uploading images for place", place["name"])
        upload_images(base_path, "place", pid)

if load_events: print("Loading events...")
in_csv = os.path.join(data_dir, "event_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)    
event_extra = {}
for row in reader:
    event_extra[row[2]] = {'image': row[6]}
    if load_events:
        print("Creating event", row[2], "...")

        place = {"id": place_dict[row[0]]['id']}
        artists = [{"id":user_dict[name.strip()]['id']} for name in row[1].split(';')]
        host = place_dict[row[0]]['host']
        hostFullName = host['firstName'] + ' ' + host['lastName']
        hostEmail = user_dict[hostFullName]['email']
        hostPassword = user_dict[hostFullName]['password']
        
        print("  Logging host", hostFullName)
        
        # First the host user needs to login so we have the token to use in place creation
        d = make_data_request({'email': hostEmail, 'password': hostPassword})
        r = requests.post(url + '/api/login/', data=d)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        h = auth_header(host_token)   

        raw_event_data = event_json(place, artists, row[2], row[3], row[4], row[5])
        d = make_data_request(raw_event_data)

        r = requests.post(url + '/api/event/', data=d, headers=h)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        eid = r.json()["id"]
        print("  Created event with id", eid)

        # Logout
        r = requests.delete(url + '/api/login/', headers=h)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
        
        print("  Logged out succesfully")

# Retrieving all events
events_dict = {}
r = requests.get(url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    if load_events and load_images:
        if not event['name'] in event_extra: continue
        eid = event['id']
        fn = event_extra[event['name']]['image']
        print("Uploading images for event", event["name"])
        upload_image(data_dir + "/images/events", fn, "event", eid)

if load_artworks:
    print("Loading artworks...")