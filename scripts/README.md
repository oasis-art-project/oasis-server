# Data scripts

The scripts in this folder are meant to be load/edit/remove data from a local or remote OASIS database without having to rely on manual data entry using the webapp. This is useful when initializing a deployment of OASIS with a large number of entries.

## Install dependencies

All of of these scripts are written in Python and use the requests package to make REST requests to the OASIS server. Install all the dependencies required by the scripts with: 

`pip install -r requirements.txt`

## Populate script

The populate script will upload data to the OASIS db and copy artwork images to either the AWS bucket or to a local folder. This script can be used as follows:

`python populate.py -u <server url> -f <folder with data> [-d]` 

Here, ```<server url>``` can be either a local or remote OASIS server. The ```-d``` (or ```--debug```) flag can be used when loading a demo dataset with all dates set to the past, such as the one provided [here](https://github.com/oasis-art-project/demo-data). When calling the populate script with this flag, the earliest event is taken as a reference and made to start today, so all other events are either current or future. For more arguments, run ```python populate.py -h```

The folder data must contain the following csv files:

* user_list.csv: Contains the list of users to add to the db, both artists and hosts.
* artwork_list.csv: Contains the list of artworks from each artist.
* place_list.csv: Contains the list of all places made available by the hosts.
* event_list.csv: Contains the list of all hosted events, past, present, and future.

as well as an images folder containing all the image files referred to in the csv files.

The structure of these files and the image folder is detailed below.

### user_list.csv

This table should contain the following columns describing each user:
 
| email	| password 	| first name | last name | phone | homepage | instagram | youtube | role | chat | bio | tags |
| ------| --------- | ---------- | --------- | ----- | -------- | --------- | ------- | ---- | ---- | --- | ---- |

* email (50 characters max, required): A valid email address for the user. This email address functions as the username in OASIS. 
* password (64 characters max, required): The login password to access their account. 
* first name (50 characters max, required): The first name of the user, although it could an acronym or collective name.
* last name (50 characters max, optional): The last name of the user.
* phone (10 characters max, optional): A phone number.
* homepage (100 characters max, optional): The URL of a website.
* instagram (30 characters max, optional): The handle of an Instagram account.
* youtube (30 characters max, optional): The handle of a YouTube account.
* role (integer number, required): The role of the user, either 2 (artist), 3 (host), or 4 (visitor)
* chat (boolean value, optional): Whether this chat can be contacted by chat on the OASIS webapp, either TRUE or FALSE. If left empy, it defaults to FALSE.
* bio (2000 characters max, optional): A biography of the user.
* tags (100 characters max, optional): A list of semicolon-separated tags words.

### artwork_list.csv


