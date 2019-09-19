import requests
import json
import os
import csv
import mimetypes
import imghdr
from os import listdir, makedirs
from os.path import isfile, join, exists, expanduser
from shutil import copy
from PIL import Image

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
        "bio": row[9],
        "tags": row[10]
    }

def host_json(id, user):
    return {
        # "id": int(id),
        "tags": user["tags"],
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
        "description": row[3],
        "tags": row[4]
    }

def event_json(place, artists, row):
    return {
        "place": place,
        "artists": artists,
        "name": row[2],
        "description": row[3],
        "startTime": row[4],
        "endTime": row[5],
        "tags": row[6]
    }

def copy_image(bdir, fn, rkind, rid, ddir):
    copy_image_list([join(bdir, fn)], rkind, rid, ddir)

def copy_images(bdir, rkind, rid, ddir):
    all_files = []
    for f in listdir(bdir):
        path = join(bdir, f)
        if not isfile(path) or not imghdr.what(path): continue
        all_files += [path]
    copy_image_list(all_files, rkind, rid, ddir)

def copy_image_list(lst, rkind, rid, ddir):
    dpath = join(expanduser(ddir), rkind, str(rid))
    if not exists(dpath):
        makedirs(dpath)    
    dst_name = ''
    if rkind == 'user':
        dst_name = "profile"
    elif rkind == 'place':
        dst_name = "place"
    elif rkind == 'event':
        dst_name = "event"
    elif rkind == 'artworks':
        dst_name = "artwork"
    for fn in lst:
        image_type = imghdr.what(fn)
        if image_type and image_type != 'jpeg':
            print("  Converting", fn, "to jpeg")
            tmp_path = expanduser("~/Temp")

             # Convert the image
            src_img = Image.open(fn)
            rgb_img = src_img.convert('RGB')
            conv_fn = join(tmp_path, dst_name + ".jpg")
            rgb_img.save(conv_fn)
            fn = conv_fn

        copy(fn, join(dpath, dst_name + ".jpg"))

def upload_image(bdir, fn, rkind, rid, user):
    # The user that owns the images needs to login
    user_data = make_data_request({'email': user['email'], 'password': user['password']})
    r = requests.post(url + '/api/login/', data=user_data)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    host_header = auth_header(host_token)

    full_path = join(bdir, fn)
    mtype = mimetypes.guess_type(full_path)[0]
    if not mtype: return
    image_files = [('images', (fn, open(full_path, 'rb'), mtype))]
    r = requests.post(url + '/api/media/' + str(rid) + '?resource-kind=' + rkind, files=image_files, headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for item in j:
        if item == "images":
            imgs = json.loads(j[item])
            for fn in imgs:
                print("  Uploaded image:", fn, "=>", imgs[fn]["url"])

    r = requests.delete(url + '/api/login/', headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)                    

def upload_images(bdir, rkind, rid, user):
    # The user that owns the images needs to login
    user_data = make_data_request({'email': user['email'], 'password': user['password']})
    r = requests.post(url + '/api/login/', data=user_data)
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
        image_files += [('images', (fn, open(full_path, 'rb'), mtype))]
    r = requests.post(url + '/api/media/'+ str(rid) + '?resource-kind=' + rkind, files=image_files, headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for item in j:
        if item == "images":
            imgs = json.loads(j[item])
            for fn in imgs:
                print("  Uploaded image:", fn, "=>", imgs[fn]["url"])

    r = requests.delete(url + '/api/login/', headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)  

use_local_server = True
save_images_locally = True

load_users = True
load_places = True
load_events = True
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
local_images_dir = '~/code/oasis/webapp/public/imgs/'

mimetypes.init()

if load_users: print("Loading users...")
in_csv = join(data_dir, "user_list.csv")
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
        user_data = make_data_request(raw_user_data)
        r = requests.post(url + '/api/user/', data=user_data)
        if r.status_code == 400:
            print("  User already exists")
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
        if save_images_locally:
            print("Copying images for user", user["firstName"], user["lastName"])
            copy_images(base_path, "user", uid, local_images_dir)
        else:
            print("Uploading images for user", user["firstName"], user["lastName"])
            upload_images(base_path, "user", uid, user)

if load_places: 
    print("Loading places...")
    in_csv = join(data_dir, "place_list.csv")
    reader = csv.reader(open(in_csv, 'r'), dialect='excel')
    header = next(reader)
    for row in reader:
        print("Creating place", row[1], "...")
        print("  Logging user", row[0])

        user = user_dict[row[0]]

        # First the host user needs to login so we have the token to use in place creation
        user_data = make_data_request({'email': user['email'], 'password': user['password']})
        r = requests.post(url + '/api/login/', data=user_data)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        host_header = auth_header(host_token)

        raw_place_data = place_json(row, host_json(row[0], user))
        p = make_data_request(raw_place_data)
        r = requests.post(url + '/api/place/', data=p, headers=host_header)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        pid = r.json()["id"]
        print("  Created place with id", pid)

        # Logout
        r = requests.delete(url + '/api/login/', headers=host_header)
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
        host = place['host']
        user = user_dict[host['firstName'] + ' ' + host['lastName']]
        base_path = data_dir + "/images/places/" + place["name"]
        if save_images_locally:
            print("Copying images for place", place["name"])
            copy_images(base_path, "user", uid, local_images_dir)
        else:
            print("Uploading images for place", place["name"])
            upload_images(base_path, "place", pid, user)

if load_events: print("Loading events...")
in_csv = join(data_dir, "event_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)    
event_extra = {}
for row in reader:
    event_extra[row[2]] = {'image': row[7]}
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
        user_data = make_data_request({'email': hostEmail, 'password': hostPassword})
        r = requests.post(url + '/api/login/', data=user_data)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        host_header = auth_header(host_token)   

        raw_event_data = event_json(place, artists, row)
        user_data = make_data_request(raw_event_data)

        r = requests.post(url + '/api/event/', data=user_data, headers=host_header)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        eid = r.json()["id"]
        print("  Created event with id", eid)

        # Logout
        r = requests.delete(url + '/api/login/', headers=host_header)
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
        host = event['place']['host']
        user = user_dict[host['firstName'] + ' ' + host['lastName']]        
        fn = event_extra[event['name']]['image']
        if save_images_locally:
            print("Uploading images for event", event["name"])
            copy_image(data_dir + "/images/events", fn, "event", eid, local_images_dir)
        else:        
            print("Uploading images for event", event["name"])
            upload_image(data_dir + "/images/events", fn, "event", eid, user)

if load_artworks:
    print("Loading artworks...")