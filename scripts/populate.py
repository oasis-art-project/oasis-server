import requests
import json
import os
import csv

def params(request, filename=None):
    parameters = {"request": json.dumps(request)}

    # Prepare files for sending
    if filename:
        # Read files from the disk, open into File instances...
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = {"files": [open(os.path.join(dir_path, filename), 'rb')]}

        # ... and save it in parameters json
        parameters.update(files)

    return parameters

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

data_dir = "./dummy_data/"

print("Loading users...")
# in_csv = os.path.join(data_dir, "user_list.csv")
# reader = csv.reader(open(in_csv, 'r'), dialect='excel')
# header = next(reader)
# for row in reader:
#     data = user_json(row)
#     in_img = os.path.join(data_dir,row[9])
#     p = params(data, in_img)
#     print(p)
    
#     r = requests.post('http://127.0.0.1:5000/api/user/', data = p)
#     if r.status_code != 201:
#         # This means something went wrong.
#         raise Exception(r.status_code)

#     print("Request was succesful! Got the following response from server:")
#     for item in r.json():
#         print(item)

print("Loading places...")


print("Loading events...")
