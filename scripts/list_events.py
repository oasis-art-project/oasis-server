import requests
import argparse

parser = argparse.ArgumentParser(description='List events.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
args = parser.parse_args()

server_url = args.url

r = requests.get(server_url + '/api/event/')

if r.status_code != 200:
    # This means something went wrong.
    raise Exception(r.status_code)

print("Request was succesful!")
print("Got the following:")
events = r.json()['events']
for event in events:
    id = event['id']
    name = event['name']
    place = event['place']['name']
    host = event['place']['host']
    time0 = event['startTime']
    time1 = event['endTime']
    print("===> Event", id, name)
    print("  Place:", place)
    print("  Host:", host['firstName'], host['lastName'])
    print("  Starts:", time0)
    print("  Ends:", time1)
