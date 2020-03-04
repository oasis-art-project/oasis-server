import requests
import argparse

parser = argparse.ArgumentParser(description='List user and place IDs.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
args = parser.parse_args()

server_url = args.url

resp = requests.get(server_url + '/api/user/')
if resp.status_code != 200:
    raise Exception(resp.status_code)

print("Get users request was succesful!")
print("Got the following users:")
users = resp.json()['users']
for user in users:
    print(user['id'], user['firstName'], user['lastName'])

resp = requests.get(server_url + '/api/place/')
if resp.status_code != 200:
    raise Exception(resp.status_code)

print("")

print("Get places request was succesful!")
print("Got the following places:")
places = resp.json()['places']
for place in places:
    print(place['id'], place['name'])