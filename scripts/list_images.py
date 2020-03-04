import requests
import json
import os
import argparse

parser = argparse.ArgumentParser(description='Upload dummy data to OASIS server.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
args = parser.parse_args()

server_url = args.url

r = requests.get(server_url + '/api/user/')
if r.status_code != 200:
    raise Exception(r.status_code)
users = r.json()['users']
for user in users:
    uid = user['id']
    role = user['role']
    if role == 1: continue
    print("Images for user", user['firstName'], user["lastName"])
    r = requests.get(server_url + '/api/media/' + str(uid) +'?resource-kind=user')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json() 
    for img in j["images"]: 
        print("  ", img)

r = requests.get(server_url + '/api/place/')
if r.status_code != 200:
    raise Exception(r.status_code)
places = r.json()['places']
for place in places:
    pid = place['id']
    print("Images for place", place['name'])
    r = requests.get(server_url + '/api/media/' + str(pid) +'?resource-kind=place')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json()
    for img in j["images"]: 
        print("  ", img)

r = requests.get(server_url + '/api/event/')
if r.status_code != 200:
    raise Exception(r.status_code)
events = r.json()['events']
for event in events:
    eid = event['id']
    print("Images for event", event['name'])
    r = requests.get(server_url + '/api/media/' + str(eid) +'?resource-kind=event')
    if r.status_code != 200:
        raise Exception(r.status_code)
    j = r.json() 
    for img in j["images"]: 
        print("  ", img)