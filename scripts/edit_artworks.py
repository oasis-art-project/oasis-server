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
import jwt

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
        "tags": row[7],
        "id": row[9]
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
        image_files += [('images', (fn, open(full_path, 'rb'), mtype))]
    r = requests.post(server_url + '/api/media/'+ str(rid) + '?resource-kind=' + rkind, files=image_files, headers=host_header)

    if r.status_code != 200:
        print(r.content)
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

data_dir = join(sys.path[0], args.folder)

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
    user_extra[fullName] = {'email': email, 'password': password}

print("Editing artworks...")
in_csv = join(data_dir, "artwork_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
artwork_images = {}
for row in reader:
    user = user_extra[row[0]]
    
    print("Editing artwork", row[1], "...")

    # First the host user needs to login so we have the token to use in place creation
    print("  Logging user", row[0])    
    user_data = make_data_request({'email': user['email'], 'password': user['password']})
    r = requests.post(server_url + '/api/login/', data=user_data)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    host_header = auth_header(host_token)
    decoded_token = jwt.decode(host_token, verify=False)
    uid = decoded_token['identity']

    raw_artwork_data = artwork_json(row)
    p = make_data_request(raw_artwork_data)
    r = requests.put(server_url + '/api/artwork/', data=p, headers=host_header)
    if r.status_code != 200:
        raise Exception(r.status_code, r.content)

    pid = row[9]
    images = row[8].split(";")

    if images:
        print("  Deleting old images")
        r = requests.get(server_url + '/api/media/' + str(pid) +'?resource-kind=artwork')
        if r.status_code != 200:
            raise Exception(r.status_code)
        j = r.json() 
        for img in j["images"]:
            fn = os.path.split(img)[1]
            r = requests.delete(server_url + '/api/media/' + str(pid) + '?resource-kind=artwork&file-name=' + fn, headers=host_header)
            if r.status_code != 200:
                raise Exception(r.status_code)
            print("  ...deleted", fn)
                
        print("  Uploading new images")
        base_path = data_dir + "/images/artworks/" + user["email"]
        upload_images_from_list(base_path, images, "artwork", pid, user)

    # Logout
    r = requests.delete(server_url + '/api/login/', headers=host_header)
    if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
            
    print("  Logged out succesfully")