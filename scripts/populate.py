import requests
import json
import sys
import os
import csv
import argparse
import mimetypes
import imghdr
import uuid
from datetime import *
import dateutil.parser
from os import listdir, makedirs
from os.path import isfile, join, exists, expanduser
from shutil import copy, rmtree
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

def artwork_json(row, artist):
    return {
        "artist": artist,
        "name": row[1],
        "description": row[2],
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
    copy_images([join(bdir, fn)], rkind, rid, ddir)

def copy_images_from_folder(bdir, rkind, rid, ddir):
    all_files = []
    for f in listdir(bdir):
        path = join(bdir, f)
        if not isfile(path) or not imghdr.what(path): continue
        all_files += [path]
    copy_images(all_files, rkind, rid, ddir)

def copy_images_from_list(bdir, fnlist, rkind, rid, ddir):
    all_files = []
    for f in fnlist:
        path = join(bdir, f)
        if not isfile(path) or not imghdr.what(path): continue
        all_files += [path]
    copy_images(all_files, rkind, rid, ddir)

def copy_images(lst, rkind, rid, ddir):
    dpath = join(expanduser(ddir), rkind + 's', str(rid))
    if not exists(dpath):
        makedirs(dpath)    

    for fn in lst:
        dst_name = ''
        make_unique = False
        if rkind == 'user':
            dst_name = "profile"
        elif rkind == 'place':
            dst_name = "place"
            make_unique = True
        elif rkind == 'event':
            dst_name = "event"
        elif rkind == 'artwork':
            dst_name = "artwork"
            make_unique = True

        image_type = imghdr.what(fn)
        tmp_path = None
        if image_type and image_type != 'jpeg':
            print("  Converting", fn, "to jpeg")
            sub_folder = str(uuid.uuid4())
            tmp_path = join(expanduser(temp_dir), sub_folder)
            os.makedirs(tmp_path)

             # Convert the image
            src_img = Image.open(fn)
            rgb_img = src_img.convert('RGB')
            conv_fn = join(tmp_path, dst_name + ".jpg")
            rgb_img.save(conv_fn)
            fn = conv_fn

        if make_unique:
            dst_name = create_unique_filename(dpath, dst_name)

        destfn = join(dpath, dst_name + ".jpg")
        print("  ", fn, "to", destfn)        
        copy(fn, destfn)

        if tmp_path:
            try:
                rmtree(tmp_path)
            except OSError as e:
                print ("Error: %s - %s." % (e.filename, e.strerror))

def create_unique_filename(filepath, filename):
    lst = listdir(filepath)

    parts = filename.split('.')
    if not parts: 
        return filename
    name0 = parts[0].lower()

    count = 0
    for fn in lst:
        bname = os.path.basename(fn)
        parts = bname.split('.')
        if parts:
            name = parts[0].lower()
            name = name.rsplit("-")[0]
            if name == name0:
                count += 1

    res = name0 + "-" + str(count)

    return res

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
        image_files += [('images', (fn, open(full_path, 'rb'), mtype))]
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
        image_files += [('images', (fn, open(full_path, 'rb'), mtype))]
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
parser.add_argument('-t', '--temp', action='store', default='~/Temp', help='temporary folder')
parser.add_argument('-i', '--images', action='store', default='~/code/oasis/webapp/public/imgs/', help='local images folder')
parser.add_argument('-a', '--admin', action='store', default='Admin Oasis', help='admin username')
parser.add_argument('-l', '--local', action='store_true', help='store images locally')
args = parser.parse_args()

server_url = args.url
admin_name = args.admin
save_images_locally = args.local
data_dir = join(sys.path[0], "dummy_data")
temp_dir = args.temp
local_images_dir = args.images

mimetypes.init()

print("Populating users...")
in_csv = join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_extra = {}
for row in reader:
    email = row[0]
    password = row[1]
    user_extra[row[2] + ' ' + row[3]] = {'email': email, 'password':password}
    raw_user_data = user_json(row)

    print("Creating user", row[2], row[3], "...")
    user_data = make_data_request(raw_user_data)
    r = requests.post(server_url + '/api/user/', data=user_data)
    if r.status_code == 400:
        print("  User already exists")
        continue
        
    if r.status_code != 201:                
        raise Exception(r.status_code, r.content)

    uid = r.json()["id"]
    print("  Created user with id", uid)

# Uploading user images
user_dict = {}
r = requests.get(server_url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    fullName = user['firstName'] + ' ' + user['lastName']
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
    if save_images_locally:
        print("Copying images for user", user["firstName"], user["lastName"])
        copy_images_from_folder(base_path, "user", uid, local_images_dir)
    else:
        print("Uploading images for user", user["firstName"], user["lastName"])
        upload_images_from_folder(base_path, "user", uid, user)

print("Populating artworks...")
in_csv = join(data_dir, "artwork_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)    
artwork_images = {}
for row in reader:
    print("Creating artwork", row[1], "...")
    print("  Logging user", row[0])    
    user = user_dict[row[0]]

    # First the host user needs to login so we have the token to use in place creation
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
    artwork_images[pid] = row[3].split(";")

    print("  Created artwork with id", pid)

    # Logout
    r = requests.delete(server_url + '/api/login/', headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)    
        
    print("  Logged out succesfully")        

# Uploading user images
r = requests.get(server_url + '/api/artwork/')
if r.status_code != 200:
    raise Exception(r.status_code)
artworks = r.json()['artworks']
for artwork in artworks:
    pid = artwork['id']
    artist = artwork['artist']
    user = user_dict[artist['firstName'] + ' ' + artist['lastName']]
    base_path = data_dir + "/images/artworks/" + user["email"]
    images = artwork_images[pid]
    if save_images_locally:
        print("Copying images for artwork", artwork["name"])
        copy_images_from_list(base_path, images, "artwork", pid, local_images_dir)
    else:
        print("Uploading images for artwork", artwork["name"])
        upload_images_from_list(base_path, images, "artwork", pid, user)

print("Populating places...")
in_csv = join(data_dir, "place_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
for row in reader:
    print("Creating place", row[1], "...")
    print("  Logging user", row[0])

    user = user_dict[row[0]]

    # First the host user needs to login so we have the token to use in place creation
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

# Uploading place images
place_dict = {}
r = requests.get(server_url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    place_dict[place['name']] = place
    pid = place['id']
    host = place['host']
    user = user_dict[host['firstName'] + ' ' + host['lastName']]
    base_path = data_dir + "/images/places/" + place["name"]
    if save_images_locally:
        print("Copying images for place", place["name"])
        copy_images_from_folder(base_path, "place", pid, local_images_dir)
    else:
        print("Uploading images for place", place["name"])
        upload_images_from_folder(base_path, "place", pid, user)

print("Populating events...")
in_csv = join(data_dir, "event_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
event_extra = {}

rows = []
first_date = None
date_format = '%Y-%m-%dT%H:%M:%S'
for row in reader:
    start_date = datetime.strptime(row[4], date_format)
    end_date = datetime.strptime(row[5], date_format)
    row[4] = start_date
    row[5] = end_date
    if not first_date: first_date = start_date
    if start_date < first_date:
        first_date = start_date
    rows.append(row)    
    
NOW = datetime.now()
diff = NOW - first_date

for row in rows:
    event_extra[row[2]] = {'image': row[7]}
    print("Creating event", row[2], "...")

    # Normalizing dates using today as reference
    start_date = row[4] + diff
    end_date = row[5] + diff
    row[4] = start_date.strftime(date_format)
    row[5] = end_date.strftime(date_format)

    place = {"id": place_dict[row[0]]['id']}
    artists = [{"id":user_dict[name.strip()]['id']} for name in row[1].split(';')]
    host = place_dict[row[0]]['host']
    hostFullName = host['firstName'] + ' ' + host['lastName']
    hostEmail = user_dict[hostFullName]['email']
    hostPassword = user_dict[hostFullName]['password']
        
    print("  Logging host", hostFullName)
        
    # First the host user needs to login so we have the token to use in place creation
    user_data = make_data_request({'email': hostEmail, 'password': hostPassword})
    r = requests.post(server_url + '/api/login/', data=user_data)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    host_header = auth_header(host_token)   

    raw_event_data = event_json(place, artists, row)
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

# Uploading event images
events_dict = {}
r = requests.get(server_url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    if not event['name'] in event_extra: continue
    eid = event['id']
    host = event['place']['host']
    user = user_dict[host['firstName'] + ' ' + host['lastName']]        
    fn = event_extra[event['name']]['image']
    if save_images_locally:
        print("Copying images for event", event["name"])
        copy_image(data_dir + "/images/events", fn, "event", eid, local_images_dir)
    else:        
        print("Uploading images for event", event["name"])
        upload_image(data_dir + "/images/events", fn, "event", eid, user)
