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

def place_json(row, host):
    if len(row) < 10 or row[9] == "yes":
        active = True
    else:
        active = False    
    return {
        "host": host,
        "name": row[1],
        "address": row[2],
        "description": row[3],
        "homepage": row[4],
        "instagram": row[5],
        "facebook": row[6],
        "matterport_link": row[7],
        "tags": row[8],
        "active": active
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

# Parsing command line arguments
parser = argparse.ArgumentParser(description='Upload dummy data to OASIS server.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
parser.add_argument('-a', '--admin', action='store', default='Admin Oasis', help='admin username')
parser.add_argument('-f', '--folder', action='store', default='dummy_data', help='set base data folder')
parser.add_argument('-d', '--debug', action='store_true', help='set if data is for debug purposes (it normalizes event dates)')

args = parser.parse_args()

server_url = args.url
admin_name = args.admin

data_dir = os.path.abspath(args.folder)

mimetypes.init()

# Loading the hosts
in_csv = join(data_dir, "event_hosts.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_extra = {}
for row in reader:
    email = row[0].strip()
    password = row[1].strip()
    fullName = (row[2] + ' ' + row[3]).strip()
    user_extra[fullName] = {'email': email, 'password': password}

# Getting dict with all users
user_dict = {}
r = requests.get(server_url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    fullName = (user['firstName'] + ' ' + user['lastName']).strip()
    if not fullName in user_extra: 
        continue
    if not fullName == admin_name:
        user['email'] = user_extra[fullName]['email']
        user['password'] = user_extra[fullName]['password']
    user_dict[fullName] = user

in_csv = join(data_dir, "place_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
for row in reader:
    user = user_dict[row[0]]

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

    host = raw_place_data['host']
    user = user_dict[(host['firstName'] + ' ' + host['lastName']).strip()]
    base_path = data_dir + "/images/places/" + raw_place_data["name"]
    print("Uploading images for place", raw_place_data["name"])
    upload_images_from_folder(base_path, "place", pid, user)    

    # Logout
    r = requests.delete(server_url + '/api/login/', headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)    
            
    print("  Logged out succesfully")