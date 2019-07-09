import requests
import json
import os
import csv

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

def event_json(place, artists):
    return {
        "place": place,
        "artists": artists,
        "name": "City Landscapes",
        "description": "Landscape paintings from Rob Krishna",
        "startTime": "2019-09-01T20:00:00",
        "endTime": "2019-09-10T18:00:00"
    }    

data_dir = "./dummy_data/"
load_users = True
load_places = True
load_events = True
load_artworks = False

if load_users: print("Loading users...")
in_csv = os.path.join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_dict = {}
id = 1
for row in reader:
    id += 1
    raw_user_data = user_json(row)
    user_dict[str(id)] = raw_user_data
    
    if load_users:        
        in_img = os.path.join(data_dir, row[9])
        d = data(raw_user_data, [in_img])
        f = files([in_img])        
        
        r = requests.post('http://127.0.0.1:5000/api/user/', data=d, files=f)
        if r.status_code == 400: 
            print("User already exists")
            continue
        
        if r.status_code != 201:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)

        print("Created user", row[2], row[3], "! Got the following response from server:")
        for item in r.json():
            print(item, r.json()[item])

if load_places:
    print("Loading places...")
    in_csv = os.path.join(data_dir, "place_list.csv")
    reader = csv.reader(open(in_csv, 'r'), dialect='excel')
    header = next(reader)
    for row in reader:
        user = user_dict[row[0]]

        # First the host user needs to login so we have the token to use in place creation
        d = data({'email': user['email'], 'password': user['password']})
        r = requests.post('http://127.0.0.1:5000/api/login/', data=d)
        if r.status_code != 200:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        h = auth_header(host_token)

        raw_place_data = place_json(row, host_json(row[0], user))
        p = data(raw_place_data)
        f = files([os.path.join(data_dir, fn) for fn in row[3].split(";")])
        r = requests.post('http://127.0.0.1:5000/api/place/', data=p, files=f, headers=h)

        if r.status_code != 201:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)

        print("Created place", row[1], "! Got the following response from server:")
        for item in r.json():
            print(item, r.json()[item])

        # Logout
        r = requests.delete('http://127.0.0.1:5000/api/login/', headers=h)
        if r.status_code != 200:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)    
        
        print("Logged out")

if load_events:
    print("Loading events...")

    # First the host user needs to login so we have the token to use in event creation
    d = data({'email': 'ksian@oasis.art', 'password': '123456'})
    r = requests.post('http://127.0.0.1:5000/api/login/', data=d)
    if r.status_code != 200:
        # This means something went wrong.
        raise Exception(r.status_code, r.content)
    host_token = r.json()['token']
    h = auth_header(host_token)

    raw_event_data = event_json({"id": 1}, [{"id": 3}, {"id": 8}])
    d=data(raw_event_data)

    r = requests.post('http://127.0.0.1:5000/api/event/', data=d, headers=h)

    if r.status_code != 201:
        # This means something went wrong.
        raise Exception(r.status_code, r.content)

    print("Created dummy event! Got the following response from server:")
    for item in r.json():
        print(item, r.json()[item])

    # Logout
    r = requests.delete('http://127.0.0.1:5000/api/login/', headers=h)
    if r.status_code != 200:
        # This means something went wrong.
        raise Exception(r.status_code, r.content)   

if load_artworks:
    print("Loading artworks...")