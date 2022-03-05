# Data scripts

The scripts in this folder are meant to be load/edit/remove data from a local or remote OASIS database without having to rely on manual data entry using the webapp. This is useful when initializing a deployment of OASIS with a large number of entries.

Please note that these scripts were added as the need arised, so they were never designed to be consistent or easy to use :-)

## Install dependencies

All of of these scripts are written in Python and use the requests package to make REST requests to the OASIS server. Install all the dependencies required by the scripts with: 

`pip install -r requirements.txt`

## Populate script

The populate script will upload an initial batch of data to the OASIS db and will also copy/upload artwork images to either the AWS bucket or to a local folder. This script can be used as follows:

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

This table should contain the following columns describing each artwork:
 
| artist | name | description | Medium | Size | duration | year | link | tags | images |
| ------ | ---- | ----------- | ------ | ---- | -------- | ---- | ---- | ---- | ------ |

* artist (required): Full name (first + last) of the artist who created this artwork.
* name (100 characters max, required): Name (or title) of the artwork.
* description (1000 characters max, optional): Description of the artwork.
* medium (200 characters max, optional): Medium of the artwork.
* size (200 characters max, optional): Size (dimensions) of the artwork.
* duration (200 characters max, optional): Duration for time-based artworks.
* year (integer number, optional): Year when the artwork was made.
* link (100 characters max, optional): URL of external website about artwork.
* tags (100 characters max, optional): A list of semicolon-separated tags words.
* images (no character limit, required): A list of semicolon-separated image file names (without path, how the path to the files is constructed is explained below).

### place_list.csv

This table should contain the following columns describing each place:

| host | name | address | description | homepage | instagram | facebook | matterport_link | tags |
| ---- | ---- | ------- | ----------- | -------- | --------- | -------- | --------------- | ---- |

* host (required): Full name (first + last) of the host of this place.
* name (100 characters max, required): Name of the place.
* address (300 characters max, required): Address of the place.
* description (1000 characters max, optional): Description of the place.
* homepage (100 characters max, optional): The URL of a website.
* instagram (30 characters max, optional): The handle of an Instagram account.
* facebook (30 characters max, optional): The handle of a Facebook page.
* matterport_link (15 characters max, optional): The code of a Matterport scan of the place.
* tags (100 characters max, optional): A list of semicolon-separated tags words.

### event_list.csv

This table should contain the following columns describing each event:

| place | artists | artworks | name | description | alias | link | hub_link | gather_link | youtube_link | startTime | endTime | tags | image |
| ----- | ------- | -------- | ---- | ----------- | ----- | ---- | -------- | ----------- | ------------ | --------- | ------- | ---- | ----- |

* place (required): The name of the place where the event takes place.
* artists (optional): The full name (first + last) of the artists participating in the event, semicolon-separated
* artworks (optional): The list of artworks included in the event, either as semicolon-separated names (titles). If the artwork names are not unique, they can be uniquely identified by the string ```Artist Full Name:N``` where the full name is first + last of the artist who made that piece and N is the position of the artwork among all the artworks for the artists (as listed in the artwork table).
* name (100 characters max, required): Name of the event.
* description (1000 characters max, optional): Description of the event.
* alias (50 characters max, optional): Alias of the event, it is used to generate a shortlink in the OASIS webapp of the form ```https://{OASIS URL}/alias```.
* link (100 characters max, optional): URL of external website about event.
* hub_link (50 characters max, optional): Code of virtual event on Mozilla Hubs, or full URL on a Hubs Cloud deployment.
* gather_link (10 characters max, optional): Code of virtual event on Gather.Town.
* youtube_link (15 characters max, optional): Code of live event on YouTube.
* startTime (datetime valule, required): Starting date and time of the event, as an UTC string: ```YYYY-MM-DDTHH:MM:SS```.
* endTime (datetime valule, optional): Ending date and time of the event, as an UTC string: ```YYYY-MM-DDTHH:MM:SS```. If none is provided, the event is permanently shown as current.
* tags (100 characters max, optional): A list of semicolon-separated tags words.
* image (no character limit, required): File name of one representative image of the event (without path, how the path to the files is constructed is explained below).

### Images 

The images referred in the above tables must be provided inside a subdirectory called ```images``` inside the directory where all the csv files are located. This subdirectory has the following structure:

```
images
│
└───artworks
│   │
│   └───email1@mail.com
│   │   artwork.jpg
│   │   ...
│   └───email2@mail.com
│   │   another_artork_image.png 
│   ...
│
└───events
│   event1_img.jpg
│   cover2.jpg
│   ...
│
└───places
│   │
│   └───Place Name
│   │   img1.jpg
│   │   img2.jpg
│   │   ...
│   └───Another Place
│   │   ...
│   ...
│
└───users
    │
    └───artists
    │   │
    │   └───email1@mail.com
    │   │   profile.png
    │   ...
    │
    └───hosts
        └───email2@mail.com
        │   profile.png
        ...
```

Here, the images of each artwork must be placed under ```images/artworks/<artist email>``` since the email should uniquely identify each artist, so for each artwork filename listed in the artworks csv, the full path ```images/artworks/<artist email>/<image filename>``` is constructed.

Each event has its unique image indicated in the events csv, and all should be found under ```images/events```.

The places csv does not include image filenames, so all the image files found under ```images/places/<Place Name>``` are assigned to that place.

Finally, the users' profile images are loaded from wherever image files are found under ```images/users/artists/<artist email>``` and ```images/users/hosts/<host email>```, for artist and hosts, respectively.

## Scripts to add new items

Once the OASIS db has been initialized with an initial batch of data, we can still add new elements to it using the following scripts:

* add_users.py: Add new users to the db.
* add_artworks.py: Add new artworks to existing users in the db.
* add_places.py: Add new places to existing hosts in the db.
* add_events.py: Add new events using existing information in the db.

All of these scripts use some or all of the csv files we already covered, with images stored in the similar tree structure. See details in the sections below:

### add_users script

`python add_users.py -u <server url> -f <folder with data> [-c]` 

Same as with the populate script, we have to provide the URL of the local/remote server, and the folder containing the data to add. There is only one file needed in the data folder, which is ```user_list.csv``` and with the same columns as mentioned. However, the add_users script accepts an optional flag, ```-c``` or ```--confirmed```. If this argument is not provided, the user will not show up in the UI of the webapp, since it needs to be confirmed by the administrator. Adding this flag performs this confirmation upon creation.

### add_artworks script

`python add_artworks.py -u <server url> -f <folder with data>` 

This script only needs the ```artwork_list.csv``` file to be present in the data folder, with all referred image files inside the ```images``` folder as previously explained.

### add_places script

`python add_places.py -u <server url> -f <folder with data>`

The new places are provided in the ```place_list.csv``` file as before, but now, since we are adding new places for existing hosts, we need to provide a csv file with the hosts for the new places, named ```event_hosts.csv```, with the same columns as the user csv file described above. In particular, this table contains the password of the hosts, which are needed to login as each host and create a new place for them.

### add_events script

`python add_events.py -u <server url> -f <folder with data>`

In this case, in addition to the list of new events (in the ```event_list.csv```), the data folder must also contain the list of artists participating in the event (```user_list.csv```) and the list of hosts of those events (```event_hosts.csv```), all as described before as well as any necessary image files in the ```images``` subdirectory.

## Scripts to edit existing items

Finally, existing entries in the OASIS db may need to be modified. This can be done in batch using a series of corresponding scripts for each data type:

* edit_users.py: Edit existing users in the db.
* edit_artworks.py: Edit existing artworks in the db.
* edit_places.py: Edit existing places in the db.
* edit_events.py: Edit existing events in the db.

The usage details for each one of these scripts are presented below:

### edit_users script

`python edit_users.py -u <server url> -f <folder with data>` 

The same as before, this script will read the ```user_list.csv``` file and update the user in each row. It also automatically sets the edited users to confirmed. An optional addition to the csv file is an extra column called ```active```. If this column contains the ```no``` values, then the user is marked as inactive, which only affects hosts. Inactive hosts are no longer listed in the hosts tab of the webapp, although they are still in the db and can be found by opening one of the places they hosted.

### edit_artworks script

`python edit_artworks.py -u <server url> -f <folder with data>`

This script requires the ```artwork_list.csv``` file with the list of artworks to edit (which includes replacing artwork images) and ```user_list.csv``` with the artsits whose artworks are being modified (since the script logs into the db with the users' credentials to apply the edits). One extra piece of information that's required in the ```artwork_list.csv``` table is an additional column with the ```id``` of the artwork to be edited, because the name alone may not be sufficient to find the artwork in the db.

### edit_places script

`python edit_places.py -u <server url> -f <folder with data>`

This script requires two files: ```place_list.csv```, the list of places to edit, and ```place_hosts.csv```, the list of hosts of those places. The list of places can also include an additional ```active``` column to mark places as inactive if the value in that column in ```no```. Inactive places are not shown on the map in the webapp, but are still listed.

### edit_events script

Finally, this script requires the file ```event_list.csv```, holding the list of events to modify, and then two more files: ```event_artists.csv```, the list of participating artists, and ```event_hosts.csv```, the list of hosts.