import os
import requests
from requests.exceptions import HTTPError

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

data_dir = "./dummy_data/"
fn = "profile.jpg"
f = os.path.join(data_dir, fn)

print("WILL TRY TO GET THE SIGNED REQUEST")

resp = requests.get('http://127.0.0.1:5000/api/upload/sign/2?resource-kind=user&file-name=' + fn +'&file-type=image/jpg')

if resp.status_code != 200:
    # This means something went wrong.
    raise Exception(resp.status_code)

print("Request was succesful!")
print("Got the following:")
print(resp)
json = resp.json()
for item in json:
    print(item, json[item])



print("")
print("WILL TRY TO UPLOAD THE FILE", f)
s3Data = json["data"]
# url = json["url"]

# for item in json:
#     print(item)
url = s3Data['url']
p = s3Data['fields']
p['file'] = open(f,'rb')
# files = {'file': open(f, 'rb')}

h  = {'x-amz-acl': 'public-read'}

print(url)
print(p)
print(h)

try:
    resp = requests.post(url, data=p, headers=h)

    # If the response was successful, no Exception will be raised
    resp.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
    print(f'Other error occurred: {err}')  # Python 3.6
else:
    print('Success!')

# http://zabana.me/notes/upload-files-amazon-s3-flask.html