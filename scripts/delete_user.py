import requests
import json
import argparse

def make_data_request(data):
    request = {"request": json.dumps(data)}
    return request

def auth_header(token):
    return {
        'Authorization': 'Bearer {}'.format(token)
    }

def try_post(path, data=None, files=None, headers=None):
    count = 0
    while count < 3:
        try:
            r = requests.post(path, data=data, files=files, headers=headers)
            return r
        except:
            time.sleep(10 ** (count + 1)) 
            count += 1     

parser = argparse.ArgumentParser(description='Deletes all data in the DB.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
parser.add_argument('-e', '--email', action='store', default='admin@youroasis.art', help='admin email')
parser.add_argument('-p', '--password', action='store', default='your_admin_password', help='admin password')
parser.add_argument('-id', '--user_id', action='store', default='999', help='ID of user to delete')

args = parser.parse_args()
server_url = args.url
admin_email = args.email
admin_passowrd = args.password
user_id = args.user_id

# Need to login as admin to delete stuff
print("Logging in as admin")
d = make_data_request({'email': admin_email, 'password': admin_passowrd})
r = try_post(server_url + '/api/login/', data=d)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)
host_token = r.json()['token']
h = auth_header(host_token)

resp = requests.get(server_url + '/api/user/' + user_id)
if resp.status_code != 200:
    raise Exception(resp.status_code)

user = resp.json()['user']

d = {"id": user_id}

r = requests.delete(server_url + '/api/user/', data=d, headers=h)
if r.status_code != 200:
    raise Exception(r.status_code, r.content)

print("Deleted user " + user['firstName'] + " " + user['lastName'])
