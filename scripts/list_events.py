import requests
import argparse

def print_events(events):
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

parser = argparse.ArgumentParser(description='List all events, or current and upcoming given a specific date.')
parser.add_argument('-u', '--url', action='store', default='http://127.0.0.1:5000', help='set server url')
parser.add_argument('-d', '--date', action='store', default='', help='date to classify events as current and upcoming, in yyy-mm-dd format')
args = parser.parse_args()

server_url = args.url
current_date = args.date

r = requests.get(server_url + '/api/event/' + current_date)

if r.status_code != 200:
    # This means something went wrong.
    raise Exception(r.status_code)

print("Request was succesful!")
print("Got the following:")
if current_date:
    print("CURRENT EVENTS")
    current_events = r.json()['current_events']
    print_events(current_events)
    print("UPCOMING EVENTS")
    upcoming_events = r.json()['upcoming_events']
    print_events(upcoming_events)
else:
    print("ALL EVENTS")
    all_events = r.json()['events']
    print_events(all_events)