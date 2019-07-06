import requests
import json
import os
import csv

def params(request, filenames=None):
    parameters = {"request": json.dumps(request)}

    # Prepare files for sending
    if filenames:
        # Read files from the disk, open into File instances...
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = {"files": [open(os.path.join(dir_path, fn), 'rb') for fn in filenames]}

        # ... and save it in parameters json
        parameters.update(files)

    return parameters

def auth_header(token):
    return {
        'Content-type': 'multipart/form-data',
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

def place_json(row, host):
    return {
        "host": host,
        "name": row[1],
        "address": row[2],
        "description": row[4]
    }

def host_json(id, user):
    return {
        "id": int(id),
        # "email": user["email"],
        # "password": user["password"],
        # "firstName": user["firstName"],
        # "lastName": user["lastName"],
        # "twitter": user["twitter"],
        # "flickr": user["flickr"],
        # "instagram": user["instagram"],
        # "avatar": None,
        # "role": int(user["role"]),
        # "bio": user["bio"]
    }

data_dir = "./dummy_data/"
load_users = True
load_places = True
load_events = False
load_artworks = False

if load_users: print("Loading users...")
in_csv = os.path.join(data_dir, "user_list.csv")
reader = csv.reader(open(in_csv, 'r'), dialect='excel')
header = next(reader)
user_dict = {}
id = 1
for row in reader:
    id += 1
    data = user_json(row)
    user_dict[str(id)] = data
    
    if load_users:
        in_img = os.path.join(data_dir,row[9])
        p = params(data, [in_img])
        print(p)
        
        r = requests.post('http://127.0.0.1:5000/api/user/', data=p)
        if r.status_code == 400: 
            print("User already exists")
            continue
        
        if r.status_code != 201:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)

        print("Created user! Got the following response from server:")
        for item in r.json():
            print(r.json()[item])

if load_places:
    # Data and authorization headers not working... maybe the following are relevant:
    # https://stackoverflow.com/questions/20759981/python-trying-to-post-form-using-requests
    # https://github.com/kennethreitz/requests/issues/910

    # Use session instead of requests object
    # session = requests.Session()

    print("Loading places...")
    in_csv = os.path.join(data_dir, "place_list.csv")
    reader = csv.reader(open(in_csv, 'r'), dialect='excel')
    header = next(reader)
    for row in reader:
        user = user_dict[row[0]]

        # First the host user needs to login so we have the token to use in place creation
        print("Login user", user)
        d = params({'email': user['email'], 'password': user['password']})
        print("LOGIN DATA", d)
        r = requests.post('http://127.0.0.1:5000/api/login/', data=d)
        if r.status_code != 200:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)
        host_token = r.json()['token']
        h = auth_header(host_token)

        data = place_json(row, host_json(row[0], user))    
        pics = [os.path.join(data_dir, fn) for fn in row[3].split(";")]    
        p = params(data)
        print("PAYLOAD", p)
        print("HEADER", h)

        r = requests.post('http://127.0.0.1:5000/api/place/', data=p, headers=h)

        # Setting the header in the global session?
        # with requests.Session() as s:
        #     s.headers.update(h)
        #     r = requests.post('http://127.0.0.1:5000/api/place/', data=p)

        if r.status_code != 201:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)

        print("Created place! Got the following response from server:")
        for item in r.json():
            print(r.json()[item])

        # Logout
        r = requests.delete('http://127.0.0.1:5000/api/login/', headers=h)
        if r.status_code != 200:
            # This means something went wrong.
            raise Exception(r.status_code, r.content)    
        
        print("Logged out")

if load_events:
    print("Loading events...")

if load_artworks:
    print("Loading artworks...")
