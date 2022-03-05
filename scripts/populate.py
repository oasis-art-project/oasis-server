import requests
import json
import sys
import os
import csv
import argparse
import mimetypes
from datetime import *
import dateutil.parser
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
        "phone": row[4],
        "homepage": row[5],
        "instagram": row[6],
        "youtube": row[7],
        "role": row[8],
        "showChat": row[9] == 'TRUE',        
        "bio": row[10],
        "tags": row[11],
        "confirmed": True
    }

def host_json(id, user):
    return {
        "tags": user["tags"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "bio": user["bio"],
        "phone": user["phone"],
        "homepage": user["homepage"],
        "instagram": user["instagram"],
        "youtube": user["youtube"],
    }

def place_json(row, host):
    return {
        "host": host,
        "name": row[1],
        "address": row[2],
        "description": row[3],
        "homepage": row[4],
        "instagram": row[5],
        "facebook": row[6],
        "matterport_link": row[7],
        "tags": row[8]
    }

def artwork_json(row, artist):
    year = None
    if row[6]:
        year = int(row[6])
    return {
        "artist": artist,
        "name": row[1],
        "description": row[2],
        "medium": row[3],
        "size": row[4],
        "duration": row[5],
        "year": year,
        "link": row[7],
        "tags": row[8]
    }

def event_json(place, artists, artworks, row):
    return {
        "place": place,
        "artists": artists,
        "artworks": artworks,
        "name": row[3],
        "description": row[4],
        "alias": row[5],
        "link": row[6],
        "hubs_link": row[7],
        "gather_link": row[8],
        "youtube_link": row[9],
        "startTime": row[10],
        "endTime": row[11],
        "tags": row[12]
    }

def upload_image(bdir, fn, rkind, rid, user):
    upload_images_from_list(bdir, [fn], rkind, rid, user)

def upload_images_from_folder(bdir, rkind, rid, user):
    # The user that owns the images needs to login
    user_data = make_data_request({'email': user['email'], 'password': user['password']})
    r = requests.post(server_url + '/api/login/', data=user_data)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    host_header = auth_header(host_token)

    image_files = []
    all_files = [f for f in listdir(bdir) if isfile(join(bdir, f))]
    for fn in all_files:
        full_path = join(bdir, fn)
        mtype = mimetypes.guess_type(full_path)[0]
        if not mtype: continue
        image_files += [(fn, open(full_path, 'rb'))]
    r = requests.post(server_url + '/api/media/'+ str(rid) + '?resource-kind=' + rkind, files=image_files, headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for item in j:
        if item == "images":
            imgs = json.loads(j[item])
            for fn in imgs:
                print("  Uploaded image:", fn, "=>", imgs[fn]["url"])

    r = requests.delete(server_url + '/api/login/', headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

def upload_images_from_list(bdir, fnlist, rkind, rid, user):
    # The user that owns the images needs to login
    user_data = make_data_request({'email': user['email'], 'password': user['password']})
    r = requests.post(server_url + '/api/login/', data=user_data)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    host_header = auth_header(host_token)

    image_files = []
    all_files = [f for f in fnlist if isfile(join(bdir, f))]
    for fn in all_files:
        full_path = join(bdir, fn)
        mtype = mimetypes.guess_type(full_path)[0]
        if not mtype: continue
        image_files += [(fn, open(full_path, 'rb'))]
    r = requests.post(server_url + '/api/media/'+ str(rid) + '?resource-kind=' + rkind, files=image_files, headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for item in j:
        if item == "images":
            imgs = json.loads(j[item])
            for fn in imgs:
                print("  Uploaded image:", fn, "=>", imgs[fn]["url"])

    r = requests.delete(server_url + '/api/login/', headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

# Parsing command line arguments
parser = argparse.ArgumentParser(description='Upload dummy data to OASIS server.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
parser.add_argument('-a', '--admin', action='store', default='Admin Oasis', help='admin username')
parser.add_argument('-f', '--folder', action='store', default='dummy_data', help='set base data folder')
parser.add_argument('-s', '--step', action='store', default=0, type=int, help='set starting step of db population (0-8)')
parser.add_argument('-d', '--debug', action='store_true', help='set if data is for debug purposes (it normalizes event dates)')

args = parser.parse_args()

server_url = args.url
admin_name = args.admin

data_dir = os.path.abspath(args.folder)
step = args.step

mimetypes.init()

print("1 - Populating users...")
in_csv = join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_extra = {}
for row in reader:
    email = row[0].strip()
    password = row[1].strip()
    user_extra[(row[2] + ' ' + row[3]).strip()] = {'email': email, 'password': password}
    raw_user_data = user_json(row)

    if step <= 1:
        print("Creating user", row[2], row[3], "...")
        user_data = make_data_request(raw_user_data)
        r = requests.post(server_url + '/api/user/', data=user_data)
        if r.status_code == 409:
            print("  User already exists")
            continue
            
        if r.status_code != 201:                
            raise Exception(r.status_code, r.content)

        uid = r.json()["id"]
        print("  Created user with id", uid)

print("2 - Uploading user images...")
user_dict = {}
r = requests.get(server_url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    fullName = (user['firstName'] + ' ' + user['lastName']).strip()
    if not fullName == admin_name:
        user['email'] = user_extra[fullName]['email']
        user['password'] = user_extra[fullName]['password']
    user_dict[fullName] = user
    uid = user['id']
    role = user['role']
    if role == 1: continue
    if role == 2:
        base_path = data_dir + "/images/users/hosts/" + user['email']
    elif role == 3:
        base_path = data_dir + "/images/users/artists/" + user['email']
    if step <= 2:
        print("Uploading images for user", user["firstName"], user["lastName"])
        upload_images_from_folder(base_path, "user", uid, user)

print("3 - Populating artworks...")
in_csv = join(data_dir, "artwork_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
artwork_images = {}
for row in reader:
    user = user_dict[row[0]]
    if step <= 3:
        print("Creating artwork", row[1], "...")

        # First the host user needs to login so we have the token to use in place creation
        print("  Logging user", row[0])        
        user_data = make_data_request({'email': user['email'], 'password': user['password']})
        r = requests.post(server_url + '/api/login/', data=user_data)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        host_header = auth_header(host_token)

        artist = {"id": user_dict[row[0].strip()]['id']}

        raw_artwork_data = artwork_json(row, artist)
        p = make_data_request(raw_artwork_data)
        r = requests.post(server_url + '/api/artwork/', data=p, headers=host_header)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        pid = r.json()["id"]
        artwork_images[pid] = row[9].split(";")

        print("  Created artwork with id", pid)

        # Logout
        r = requests.delete(server_url + '/api/login/', headers=host_header)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
            
        print("  Logged out succesfully")

print("4 - Uploading artwork images...")
artwork_dict = {}
r = requests.get(server_url + '/api/artwork/')
if r.status_code != 200:
    raise Exception(r.status_code)
artworks = r.json()['artworks']
artworks.sort(key=lambda k: int(k.get('id', 0))) # Sorting by id because they might not be in original order
counts = {}
for artwork in artworks:
    pid = artwork['id']
    name = artwork['name'].strip()
    if not name: name = 'Untitled'
    artist = artwork['artist']
    fname = (artist['firstName'] + ' ' + artist['lastName']).strip()
    if fname in counts:
        count = counts[fname]
        count += 1
    else:
        count = 1
    counts[fname] = count
    key = name
    if name == 'Untitled':         
        key = fname + ':' + str(count)
    artwork_dict[key] = artwork
    if step <= 4:
        user = user_dict[fname]
        base_path = data_dir + "/images/artworks/" + user["email"]
        images = artwork_images[pid]
        print("Uploading images for artwork", artwork["name"])
        upload_images_from_list(base_path, images, "artwork", pid, user)

#print(artwork_dict)

print("5 - Populating places...")
in_csv = join(data_dir, "place_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
for row in reader:
    user = user_dict[row[0]]
    if step <= 5:
        print("Creating place", row[1], "...")    

        # First the host user needs to login so we have the token to use in place creation
        print("  Logging user", row[0])    
        user_data = make_data_request({'email': user['email'], 'password': user['password']})
        r = requests.post(server_url + '/api/login/', data=user_data)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        host_header = auth_header(host_token)

        raw_place_data = place_json(row, host_json(row[0], user))
        p = make_data_request(raw_place_data)
        r = requests.post(server_url + '/api/place/', data=p, headers=host_header)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        pid = r.json()["id"]
        print("  Created place with id", pid)

        # Logout
        r = requests.delete(server_url + '/api/login/', headers=host_header)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
            
        print("  Logged out succesfully")

print("6 - Uploading place images...")
place_dict = {}
r = requests.get(server_url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    place_dict[place['name']] = place
    if step <= 6:
        pid = place['id']
        host = place['host']
        user = user_dict[(host['firstName'] + ' ' + host['lastName']).strip()]
        base_path = data_dir + "/images/places/" + place["name"]
        print("Uploading images for place", place["name"])
        upload_images_from_folder(base_path, "place", pid, user)

print("7 - Populating events...")
in_csv = join(data_dir, "event_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
event_extra = {}

rows = []
first_date = None
date_format = '%Y-%m-%dT%H:%M:%S'
for row in reader:
    start_date = datetime.strptime(row[10], date_format)
    end_date = datetime.strptime(row[11], date_format)
    row[10] = start_date
    row[11] = end_date
    if not first_date: first_date = start_date
    if start_date < first_date:
        first_date = start_date
    rows.append(row)    

if args.debug:
    NOW = datetime.now()
    diff = NOW - first_date

for row in rows:
    event_extra[row[3]] = {'image': row[13]}

    if args.debug:
        # Normalizing dates using today as reference
        start_date = row[10] + diff
        end_date = row[11] + diff
    else:
        start_date = row[10]
        end_date = row[11]

    row[10] = start_date.strftime(date_format)
    row[11] = end_date.strftime(date_format)

    place = {"id": place_dict[row[0]]['id']}
    if row[1]:
        artists = [{"id":user_dict[name.strip()]['id']} for name in row[1].split(';')]
    else:
        artists = []
    if row[2]:
        artworks = [{"id":artwork_dict[name.strip()]['id']} for name in row[2].split(';')]
    else:
        artworks = []
    host = place_dict[row[0]]['host']
    hostFullName = (host['firstName'] + ' ' + host['lastName']).strip()
    hostEmail = user_dict[hostFullName]['email']
    hostPassword = user_dict[hostFullName]['password']

    if step <= 7:
        print("Creating event", row[3], "...")

        # First the host user needs to login so we have the token to use in place creation
        print("  Logging host", hostFullName)        
        user_data = make_data_request({'email': hostEmail, 'password': hostPassword})
        r = requests.post(server_url + '/api/login/', data=user_data)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        host_header = auth_header(host_token)   

        raw_event_data = event_json(place, artists, artworks, row)
        user_data = make_data_request(raw_event_data)

        r = requests.post(server_url + '/api/event/', data=user_data, headers=host_header)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        eid = r.json()["id"]
        print("  Created event with id", eid)

        # Logout
        r = requests.delete(server_url + '/api/login/', headers=host_header)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
            
        print("  Logged out succesfully")

print("8 - Uploading event images...")
events_dict = {}
r = requests.get(server_url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    if not event['name'] in event_extra: continue
    if step <= 8:
        eid = event['id']
        host = event['place']['host']
        user = user_dict[(host['firstName'] + ' ' + host['lastName']).strip()]
        fn = event_extra[event['name']]['image']
        print("Uploading images for event", event["name"])
        upload_image(data_dir + "/images/events", fn, "event", eid, user)
