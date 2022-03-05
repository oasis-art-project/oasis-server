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