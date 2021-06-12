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

def user_json(row, confirmed):
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
        "confirmed": confirmed
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
parser.add_argument('-f', '--folder', action='store', default='new_data', help='set base data folder')
parser.add_argument('-c', '--confirmed', action='store_true', help='set if the user is confirmed')

args = parser.parse_args()

server_url = args.url
admin_name = args.admin

data_dir = join(sys.path[0], args.folder)

mimetypes.init()

print("Adding users...")
in_csv = join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_extra = {}
for row in reader:
    email = row[0].strip()
    password = row[1].strip()
    fullName = (row[2] + ' ' + row[3]).strip()
    user_extra[fullName] = {'email': email, 'password': password, 'id': None}
    raw_user_data = user_json(row, args.confirmed)

    print("Creating user", fullName, "...")
    user_data = make_data_request(raw_user_data)
    r = requests.post(server_url + '/api/user/', data=user_data)
    if r.status_code == 409:
        print("  User already exists")
        continue
            
    if r.status_code != 201:                
        raise Exception(r.status_code, r.content)

    uid = r.json()["id"]
    print("  Created user with id", uid)
    user_extra[fullName]['id'] = uid 

print("Uploading user images...")
for fullName in user_extra:
    r = requests.get(server_url + '/api/user/' + str(user_extra[fullName]['id']))
    if r.status_code != 200:
        raise Exception(r.status_code)

    user = r.json()['user']
    extra = user_extra[fullName]
    uid = user['id']
    role = user['role']
    if role == 1: continue
    if role == 2:
        base_path = data_dir + "/images/users/hosts/" + extra['email']
    elif role == 3:
        base_path = data_dir + "/images/users/artists/" + extra['email']
    print("Uploading images for user", fullName)
    upload_images_from_folder(base_path, "user", uid, extra)
