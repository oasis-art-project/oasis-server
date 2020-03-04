import requests
import argparse

parser = argparse.ArgumentParser(description='List user dataB.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
args = parser.parse_args()

server_url = args.url

r = requests.get(server_url + '/api/user/')

if r.status_code != 200:
    # This means something went wrong.
    raise Exception(r.status_code)

print("Request was succesful!")
print("Got the following:")
json = r.json()
users = r.json()['users']
for user in users:    
    print(user)