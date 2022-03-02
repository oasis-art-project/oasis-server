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

def artwork_json(row):
    year = None
    if row[5]:
        year = int(row[5])
    return {
        "name": row[1],
        "description": row[2],
        "medium": row[3],
        "size": row[4],
        "year": year,
        "link": row[6],
        "tags": row[7]
    }

def upload_image(bdir, fn, rkind, rid, user):
    upload_images_from_list(bdir, [fn], rkind, rid, user)

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

args = parser.parse_args()

server_url = args.url
admin_name = args.admin

data_dir = os.path.abspath(args.folder)

mimetypes.init()

# Loading artist info first, includign password and email, which is needed to upload artworks.
in_csv = join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_extra = {}
for row in reader:
    email = row[0].strip()
    password = row[1].strip()
    fullName = (row[2] + ' ' + row[3]).strip()
    user_extra[fullName] = {'email': email, 'password': password, 'id': None}

print("Adding artworks...")
in_csv = join(data_dir, "artwork_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
artwork_images = {}
for row in reader:
    user = user_extra[row[0]]
    
    print("Creating artwork", row[1], "...")

    # First the host user needs to login so we have the token to use in place creation
    print("  Logging user", row[0])    
    user_data = make_data_request({'email': user['email'], 'password': user['password']})
    r = requests.post(server_url + '/api/login/', data=user_data)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    host_header = auth_header(host_token)

    raw_artwork_data = artwork_json(row)
    p = make_data_request(raw_artwork_data)
    r = requests.post(server_url + '/api/artwork/', data=p, headers=host_header)

    if r.status_code != 201:
        raise Exception(r.status_code, r.content)

    pid = r.json()["id"]
    artwork_images[pid] = row[8].split(";")

    print("  Created artwork with id", pid)

    # Logout
    r = requests.delete(server_url + '/api/login/', headers=host_header)
    if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
            
    print("  Logged out succesfully")

print("Uploading artwork images...")
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
    
    if not fullName in user_extra.keys() or not pid in artwork_images:
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
    
    user = user_extra[fullName]
    base_path = data_dir + "/images/artworks/" + user["email"]
    images = artwork_images[pid]
    print("Uploading images for artwork", artwork["name"])
    upload_images_from_list(base_path, images, "artwork", pid, user)