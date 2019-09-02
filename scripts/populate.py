import requests
import json
import os
import csv
import mimetypes
from os import listdir
from os.path import isfile, join

def data(dat, filenames=None):
    parameters = {"request": json.dumps(dat)}    
    # # Prepare files for sending
    # if filenames:
    #     # Read files from the disk, open into File instances...
    #     dir_path = os.path.dirname(os.path.realpath(__file__))
    #     files = {"files": [open(os.path.join(dir_path, fn), 'rb') for fn in filenames]}

    #     # ... and save it in parameters json
    #     parameters.update(files)
    return parameters

def files(filenames):
    # https://2.python-requests.org//en/latest/user/advanced/#post-multiple-multipart-encoded-files
    res = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for fn in filenames:
        ext = os.path.splitext(fn)[1][1:]
        res += [('images', (os.path.split(fn)[1], open(os.path.join(dir_path, fn), 'rb'), 'image/' + ext))]
    return res

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
        "bio": row[10]
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
        "description": row[4]
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

def send_request(meth, url, data, headers=None, files=None, print_prep=True):
    # Print raw request
    # https://stackoverflow.com/a/23816211
    prepped = requests.Request(meth, url, data=data, headers=headers, files=files).prepare()
    if print_prep:
        print("*****************")
        print(prepped)
        print("*****************")
    s = requests.Session()
    resp = s.send(prepped)
    return resp

# Local server
url = 'http://127.0.0.1:5000'

# Staging server
#url = 'https://server-oasis.herokuapp.com/'

data_dir = "./dummy_data/"
load_users = False
load_places = False
load_events = False
load_artworks = False
load_images = True

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
    if load_users:
        raw_user_data = user_json(row)

        in_img = os.path.join(data_dir, row[9])
        d = data(raw_user_data, [in_img])
        # f = files([in_img])

        # r = send_request('POST', 'http://127.0.0.1:5000/api/user/', data=d, files=f)
        r = requests.post(url + '/api/user/', data=d)
        if r.status_code == 400:
            print("User already exists")
            continue
        
        if r.status_code != 201:                
            raise Exception(r.status_code, r.content)

        print("Created user", row[2], row[3], "! Got the following response from server:")
        for item in r.json():
            print(item, r.json()[item])

# Retrieving all users
user_dict = {}
resp = requests.get(url + '/api/user/')
if resp.status_code != 200:
    raise Exception(resp.status_code)
users = resp.json()['users']
for user in users:
    fullName = user['firstName'] + ' ' + user['lastName']
    if not fullName == 'Admin Oasis':
        user['email'] = user_extra[fullName]['email']
        user['password'] = user_extra[fullName]['password']
    user_dict[fullName] = user
    if load_users and load_images:
        uid = user['id']
        urole = user['role']
        if urole == 1: continue
        file_name = "profile.jpg"
        if urole == 2:
            full_path = data_dir + "/images/users/hosts/" + user['email']
        elif urole == 3: 
            full_path = data_dir + "/images/users/artists/" + user['email']
        full_path += "/" + file_name
        f = [('images', (file_name, open(full_path, 'rb'), 'image/jpg'))]
        url = 'http://127.0.0.1:5000/api/upload/'+ str(uid) +'?resource-kind=user'
        print("Uploading profile picture for", user["firstName"], user["lastName"])
        resp = requests.post(url, files=f)
        if resp.status_code != 200:
            raise Exception(resp.status_code)
        print("Success!")
        json = resp.json()
        for item in json:
            print(item, json[item])        

if load_places: 
    print("Loading places...")
    in_csv = os.path.join(data_dir, "place_list.csv")
    reader = csv.reader(open(in_csv, 'r'), dialect='excel')
    header = next(reader)
    for row in reader:
        print("Logging user", row[0])
        user = user_dict[row[0]]

        # First the host user needs to login so we have the token to use in place creation
        d = data({'email': user['email'], 'password': user['password']})
        r = requests.post(url + '/api/login/', data=d)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        h = auth_header(host_token)

        raw_place_data = place_json(row, host_json(row[0], user))
        p = data(raw_place_data)
        # f = files([os.path.join(data_dir, fn) for fn in row[3].split(";")])
        r = requests.post(url + '/api/place/', data=p, headers=h)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        print("Created place", row[1], "! Got the following response from server:")
        for item in r.json():
            print(item, r.json()[item])

        # Logout
        r = requests.delete(url + '/api/login/', headers=h)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
        
        print("Logged out succesfully")

# Retrieving all places
place_dict = {}
resp = requests.get(url + '/api/place/')
if resp.status_code != 200:
    raise Exception(resp.status_code)
places = resp.json()['places']
for place in places:
    place_dict[place['name']] = place
    if load_places and load_images:
        pid = place['id']
        f = []
        base_path = data_dir + "/images/places/" + place["name"]
        only_files = [f for f in listdir(base_path) if isfile(join(base_path, f))]
        for file_name in only_files:
            full_path = base_path + "/" + file_name        
            mtype = mimetypes.guess_type(full_path)[0]
            if not mtype: continue
            f += [('images', (file_name, open(full_path, 'rb'), mtype))]

        url = 'http://127.0.0.1:5000/api/upload/'+ str(pid) +'?resource-kind=place'
        print("Uploading picture for place", place["name"])
        resp = requests.post(url, files=f)
        if resp.status_code != 200:
            raise Exception(resp.status_code)
        print("Success!")
        json = resp.json()
        for item in json:
            print(item, json[item])

if load_events: print("Loading events...")
in_csv = os.path.join(data_dir, "event_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)    
event_extra = {}
for row in reader:
    event_extra[row[2]] = {'image': row[6]}
    if load_events:
        place = {"id": place_dict[row[0]]['id']}
        artists = [{"id":user_dict[name.strip()]['id']} for name in row[1].split(';')]
        host = place_dict[row[0]]['host']
        hostFullName = host['firstName'] + ' ' + host['lastName']
        hostEmail = user_dict[hostFullName]['email']
        hostPassword = user_dict[hostFullName]['password']
        
        print("Logging host", hostFullName)
        
        # First the host user needs to login so we have the token to use in place creation
        d = data({'email': hostEmail, 'password': hostPassword})
        r = requests.post(url + '/api/login/', data=d)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        h = auth_header(host_token)   

        raw_event_data = event_json(place, artists, row[2], row[3], row[4], row[5])
        d=data(raw_event_data)

        r = requests.post(url + '/api/event/', data=d, headers=h)

        if r.status_code != 201:
            raise Exception(r.status_code, r.content)

        print("Created new event! Got the following response from server:")
        for item in r.json():
            print(item, r.json()[item])

        # Logout
        r = requests.delete(url + '/api/login/', headers=h)
        if r.status_code != 200:
            raise Exception(r.status_code, r.content)    
        
        print("Logged out succesfully")

# Retrieving all events
events_dict = {}
resp = requests.get(url + '/api/event/')
if resp.status_code != 200:
    raise Exception(resp.status_code)
events = resp.json()['events']
for event in events:
    # if load_events and load_images:
    if load_images:
        if not event['name'] in event_extra: continue

        eid = event['id']
        file_name = event_extra[event['name']]['image']
        full_path = data_dir + "/images/events/" + file_name
        mtype = mimetypes.guess_type(full_path)[0]
        if not mtype: continue
        f = [('images', (file_name, open(full_path, 'rb'), mtype))]

        url = 'http://127.0.0.1:5000/api/upload/'+ str(eid) +'?resource-kind=event'
        print("Uploading picture for event", event['name'])
        resp = requests.post(url, files=f)
        if resp.status_code != 200:
            raise Exception(resp.status_code)
        print("Success!")
        json = resp.json()
        for item in json:
            print(item, json[item])

if load_artworks:
    print("Loading artworks...")