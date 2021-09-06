import requests
import json
import sys
import os
import csv
import argparse
import mimetypes
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
    if row[5]:
        year = int(row[5])
    return {
        "artist": artist,
        "name": row[1],
        "description": row[2],
        "medium": row[3],
        "size": row[4],
        "year": year,
        "link": row[6],
        "tags": row[7]
    }

def event_json(place, artists, artworks, row):
    return {
        "place": place,
        "artists": artists,
        "artworks": artworks,
        "name": row[3],
        "description": row[4],
        "link": row[5],
        "hubs_link": row[6],
        "startTime": row[7],
        "endTime": row[8],
        "tags": row[9],
        "id": row[11]
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
parser.add_argument('-d', '--debug', action='store_true', help='set if data is for debug purposes (it normalizes event dates)')

args = parser.parse_args()

server_url = args.url
admin_name = args.admin

data_dir = join(sys.path[0], args.folder)

mimetypes.init()

# Loading the users, need password and email
in_csv = join(data_dir, "event_artists.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_extra = {}
for row in reader:
    email = row[0].strip()
    password = row[1].strip()
    fullName = (row[2] + ' ' + row[3]).strip()
    user_extra[fullName] = {'email': email, 'password': password, 'id': None}

# Adding the hosts
in_csv = join(data_dir, "event_hosts.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
for row in reader:
    email = row[0].strip()
    password = row[1].strip()
    fullName = (row[2] + ' ' + row[3]).strip()
    user_extra[fullName] = {'email': email, 'password': password, 'id': None}

user_dict = {}
r = requests.get(server_url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    fullName = (user['firstName'] + ' ' + user['lastName']).strip()
    if fullName in user_extra:
        user['email'] = user_extra[fullName]['email']
        user['password'] = user_extra[fullName]['password']    
        user_dict[fullName] = user

# Loading artworks
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
    fullName = (artist['firstName'] + ' ' + artist['lastName']).strip()
    
    if not fullName in user_extra.keys():
        continue

    if fullName in counts:
        count = counts[fullName]
        count += 1
    else:
        count = 1
    counts[fullName] = count
    key = name
    if name == 'Untitled':         
        key = fullName + ':' + str(count)
    artwork_dict[key] = artwork

# Loading all places
place_dict = {}
r = requests.get(server_url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    place_dict[place['name']] = place

print("Editing events...")
in_csv = join(data_dir, "event_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
event_extra = {}

rows = []
first_date = None
date_format = '%Y-%m-%dT%H:%M:%S'
for row in reader:
    start_date = datetime.strptime(row[7], date_format)
    end_date = datetime.strptime(row[8], date_format)
    row[7] = start_date
    row[8] = end_date
    if not first_date: first_date = start_date
    if start_date < first_date:
        first_date = start_date
    rows.append(row)    

if args.debug:
    NOW = datetime.now()
    diff = NOW - first_date

for row in rows:
    event_extra[row[3]] = {'image': row[10]}

    if args.debug:
        # Normalizing dates using today as reference
        start_date = row[7] + diff
        end_date = row[8] + diff
    else:
        start_date = row[7]
        end_date = row[8]

    row[7] = start_date.strftime(date_format)
    row[8] = end_date.strftime(date_format)

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
    user = user_extra[hostFullName]

    print("Editing event", row[3], "...")

    # First the host user needs to login so we have the token to use in place creation
    print("  Logging host", hostFullName)        
    user_data = make_data_request({'email': hostEmail, 'password': hostPassword})
    r = requests.post(server_url + '/api/login/', data=user_data)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    host_header = auth_header(host_token)

    raw_event_data = event_json(place, artists, artworks, row)
    event_data = make_data_request(raw_event_data)
    r = requests.put(server_url + '/api/event/', data=event_data, headers=host_header)

    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    pid = row[11]
    images = row[10].split(";")
    if images:
        print("  Uploading new images")
        base_path = data_dir + "/images/events"
        upload_images_from_list(base_path, images, "event", pid, user)

    # Logout
    r = requests.delete(server_url + '/api/login/', headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)    
            
    print("  Logged out succesfully")
