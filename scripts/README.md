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

## user_list.csv

This table should contain the following columns:
 
| email	| password 	| first name | last name | phone | homepage | instagram | youtube | role | chat | bio | tags



